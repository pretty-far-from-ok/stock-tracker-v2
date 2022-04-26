import {format} from "d3-format";
import React, {Component} from "react";
import PropTypes from "prop-types";

import displayValuesFor from "./displayValuesFor";
import GenericChartComponent from "../GenericChartComponent";

import ToolTipText from "./ToolTipText";
import ToolTipTSpanLabel from "./ToolTipTSpanLabel";
import {functor} from "../utils";

class LineGroupTooltips extends Component {
	constructor(props) {
		super(props);
		this.renderSVG = this.renderSVG.bind(this);
	}
	renderSVG(moreProps) {
		const {textFill, labelFill, options, displayFormat} = this.props;
		const {chartConfig: {width, height}} = moreProps;
		const currentItem = displayValuesFor(this.props, moreProps);
		const {origin: originProp} = this.props;
		const origin = functor(originProp);
		const [x, y] = origin(width, height);

        // line 1
        // const yValue0 = currentItem && this.props.options[0].yAccessor(currentItem);
        // const tooltipLabel0 = `${this.props.options[0].type} (${this.props.options[0].windowSize})`;
        // const color0 = this.props.options[0].stroke;
        // const yDisplayValue0 = yValue0 ? displayFormat(yValue0) : "n/a";
        const yValue0 = currentItem && this.props.options[0].yAccessor(currentItem);
        const tooltipLabel0 = `${this.props.options[0].type}`;
        const color0 = this.props.options[0].stroke;
        const yDisplayValue0 = yValue0 ? displayFormat(yValue0) : "n/a";
        // line 2
        // const yValue1 = currentItem && this.props.options[1].yAccessor(currentItem);
        // const tooltipLabel1 = `${this.props.options[1].type}`;
        // const color1 = this.props.options[1].stroke;
        // const yDisplayValue1 = yValue1 ? displayFormat(yValue1) : "n/a";
		return (
			<g transform={`translate(${ x }, ${ y })`} >
				<ToolTipText x={0} y={11}
					fontFamily={this.props.fontFamily} fontSize={this.props.fontSize}>
					<ToolTipTSpanLabel fill={labelFill}>{tooltipLabel0}: </ToolTipTSpanLabel>
					<tspan fill={textFill}>{yDisplayValue0} </tspan>
				</ToolTipText>
			</g>
		);
	}
	render() {
		return <GenericChartComponent clip={false} svgDraw={this.renderSVG} drawOn={["mousemove"]}/>;
	}
}

LineGroupTooltips.propTypes = {
	className: PropTypes.string,
	displayFormat: PropTypes.func.isRequired,
	origin: PropTypes.array.isRequired,
	displayValuesFor: PropTypes.func,
	textFill: PropTypes.string,
	labelFill: PropTypes.string,
	fontFamily: PropTypes.string,
	fontSize: PropTypes.number,
	width: PropTypes.number,
	options: PropTypes.arrayOf(PropTypes.shape({
		yAccessor: PropTypes.func.isRequired,
		type: PropTypes.string.isRequired,
		stroke: PropTypes.string.isRequired,
		windowSize: PropTypes.number.isRequired,
		echo: PropTypes.any,
	})),
};

LineGroupTooltips.defaultProps = {
	className: "react-stockcharts-tooltip react-stockcharts-line-group-tooltip",
	displayFormat: format(".2f"),
	displayValuesFor: displayValuesFor,
	origin: [0, 10],
	width: 90,
};

export default LineGroupTooltips;
