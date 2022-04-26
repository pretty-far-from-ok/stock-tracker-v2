import React, {Component} from "react";
import PropTypes from "prop-types";

import LineSeries from "./LineSeries";
import AreaOnlySeries from "./AreaOnlySeries";

class BollingerSeriesv1 extends Component {
	constructor(props) {
		super(props);
		this.yAccessorForTop = this.yAccessorForTop.bind(this);
		this.yAccessorForMiddle1 = this.yAccessorForMiddle1.bind(this);
		this.yAccessorForMiddle = this.yAccessorForMiddle.bind(this);
		this.yAccessorForBottom = this.yAccessorForBottom.bind(this);
		this.yAccessorForScalledBottom = this.yAccessorForScalledBottom.bind(this);
	}
	yAccessorForTop(d) {
		const { yAccessor } = this.props;
		return yAccessor(d) && yAccessor(d).top;
	}
	yAccessorForMiddle(d) {
		const { yAccessor } = this.props;
		return yAccessor(d) && yAccessor(d).middle0;
	}
	yAccessorForMiddle1(d) {
		const { yAccessor } = this.props;
		return yAccessor(d) && yAccessor(d).middle1;
	}
	yAccessorForBottom(d) {
		const { yAccessor } = this.props;
		return yAccessor(d) && yAccessor(d).bottom;
	}
	yAccessorForScalledBottom(scale, d) {
		const { yAccessor } = this.props;
		return scale(yAccessor(d) && yAccessor(d).bottom);
	}
	render() {
		const { areaClassName, className, opacity } = this.props;
		const { stroke, fill } = this.props;

		return (
			<g className={className}>
				<LineSeries yAccessor={this.yAccessorForTop} stroke={stroke.top} fill="none" />
				<LineSeries yAccessor={this.yAccessorForMiddle} stroke={stroke.middle0} fill="none" />
				<LineSeries yAccessor={this.yAccessorForMiddle1} stroke={stroke.middle1} fill="none" strokeWidth="1"/>
				<LineSeries yAccessor={this.yAccessorForBottom} stroke={stroke.bottom} fill="none" />
				<AreaOnlySeries className={areaClassName} yAccessor={this.yAccessorForTop} base={this.yAccessorForScalledBottom}
					stroke="none" fill={fill} opacity={opacity} />
			</g>
		);
	}
}

BollingerSeriesv1.propTypes = {
	yAccessor: PropTypes.func.isRequired,
	className: PropTypes.string,
	areaClassName: PropTypes.string,
	opacity: PropTypes.number,
	type: PropTypes.string,
	stroke: PropTypes.shape({
		top: PropTypes.string.isRequired,
		middle0: PropTypes.string.isRequired,
		middle1: PropTypes.string.isRequired,
		bottom: PropTypes.string.isRequired,
	}).isRequired,
	fill: PropTypes.string.isRequired,
};

BollingerSeriesv1.defaultProps = {
	className: "react-stockcharts-bollinger-band-seriesv1",
	areaClassName: "react-stockcharts-bollinger-band-series-area",
	opacity: 0.1 
};

export default BollingerSeriesv1;
