import {format} from "d3-format";
import {timeFormat} from "d3-time-format";

import React from "react";
import PropTypes from "prop-types";

import ZoomButtons from "./lib/ZoomButtons";
import Chart from "./lib/Chart";
import ChartCanvas from "./lib/ChartCanvas";

import BarSeries from "./lib/series/BarSeries";
import CandlestickSeries from "./lib/series/CandlestickSeries";
import LineSeries from "./lib/series/LineSeries";
import MACDSeries from "./lib/series/MACDSeries";
import VolumeProfileSeries from "./lib/series/VolumeProfileSeries";
// import BollingerSeries from "./lib/series/BollingerSeries";
import BollingerSeries from "./lib/series/BollingerSeriesv1";

import XAxis from "./lib/axes/XAxis"
import YAxis from "./lib/axes/YAxis";

import CrossHairCursor from "./lib/coordinates/CrossHairCursor"
import EdgeIndicator from "./lib/coordinates/EdgeIndicator"
import MouseCoordinateX from "./lib/coordinates/MouseCoordinateX" 
import MouseCoordinateY from "./lib/coordinates/MouseCoordinateY";

import {discontinuousTimeScaleProvider, discontinuousTimeScaleProviderBuilder} from "react-stockcharts/lib/scale";

import OHLCTooltip from "./lib/tooltip/OHLCTooltip"
// import MovingAverageTooltip from "./lib/tooltip/MovingAverageTooltip"
import LineGroupTooltips from "./lib/tooltip/LineGroupTooltips"
import MACDTooltip from "./lib/tooltip/MACDTooltip";
// import BollingerBandTooltip from "./lib/tooltip/BollingerBandTooltip";
import BollingerBandTooltipv1 from "./lib/tooltip/BollingerBandTooltipv1";

import ema from "./lib/indicator/ema"
// import sma from "./lib/indicator/sma"
import line from "./lib/indicator/line"
import macd from "./lib/indicator/macd" 
import change from "./lib/indicator/change";
// import bollingerBand from "./lib/indicator/bollingerBand";
import bollingerBand from "./lib/indicator/bollingerBandv1";

import {fitWidth} from "react-stockcharts/lib/helper";
import {last} from "react-stockcharts/lib/utils";


function getMaxUndefined(calculators){return calculators.map(each => each.undefinedLength()).reduce((a, b) => Math.max(a, b));}

const LENGTH_TO_SHOW = 100;
const macdAppearance = {stroke: {macd: "#FF0000", signal: "#00F300"}, fill: {divergence: "#4682B4"}};
const bbStroke = {top: "#386EA5", middle0: "#386EA5", middle1: "#CC6666", bottom: "#386EA5"};
const bbFill = "#E6E6FA";

class CandleStickChartPanToLoadMore extends React.Component{
    // for init data/state
	constructor(props){
		super(props);
		const {data: inputData} = props;
        // volume profile
		const changeCalculator = change();
        // ema 
        // const ema20 = ema().options({windowSize: 20, sourcePath: "close"}).skipUndefined(true).merge((d, c) => {d.ema20 = c;}).accessor(d => d.ema20).stroke("blue");
        // const ema20 = ema().options({windowSize: 1, sourcePath: "underlay_waveband"}).skipUndefined(true).merge((d, c) => {d.ema20 = c;}).accessor(d => d.ema20).stroke("#000000");
        // ohlc waveband
        const waveband1 = line().options({type:"waveband", windowSize: 1, sourcePath: "underlay_waveband"}).merge((d, c) => {d.waveband1 = c;}).accessor(d => d.waveband1).stroke("#4682B4");
        const waveband2 = line().options({windowSize: 1, sourcePath: "waveband2"}).skipUndefined(true).merge((d, c) => {d.waveband2 = c;}).accessor(d => d.waveband2).stroke("#CC6666");
        // subgraph lines
        const subch = line().options({windowSize: 1, sourcePath: "ch"}).skipUndefined(true).merge((d, c) => {d.subch = c;}).accessor(d => d.subch).stroke("#33f8ff");
        const subjl = line().options({windowSize: 1, sourcePath: "jl"}).skipUndefined(true).merge((d, c) => {d.subjl = c;}).accessor(d => d.subjl).stroke("#287cf2");
        const subref0 = line().options({windowSize: 1, sourcePath: "ref_0"}).skipUndefined(true).merge((d, c) => {d.subref0 = c;}).accessor(d => d.subref0).stroke("#000000");
        const subref20 = line().options({windowSize: 1, sourcePath: "ref_20"}).skipUndefined(true).merge((d, c) => {d.subref20 = c;}).accessor(d => d.subref20).stroke("#000000");
        const subref80 = line().options({windowSize: 1, sourcePath: "ref_80"}).skipUndefined(true).merge((d, c) => {d.subref80 = c;}).accessor(d => d.subref80).stroke("#000000");
        const subref100 = line().options({windowSize: 1, sourcePath: "ref_100"}).skipUndefined(true).merge((d, c) => {d.subref100 = c;}).accessor(d => d.subref100).stroke("#000000");
        const subd1 = line().options({windowSize: 1, sourcePath: "d_down"}).skipUndefined(true).merge((d, c) => {d.subd1 = c;}).accessor(d => d.subd1).stroke("#FB0006");
        const subd2 = line().options({windowSize: 1, sourcePath: "d_underlay"}).skipUndefined(true).merge((d, c) => {d.subd2 = c;}).accessor(d => d.subd2).stroke("#28f29E");
        // macd
		const macdCalculator = macd().options({fast: 12, slow: 26, signal: 9}).merge((d, c) => {d.macd = c}).accessor(d => d.macd);
        // bollingerband
        const bollingerbandCalculator = bollingerBand().merge((d, c) => {d.bollingerbandCalculator = c}).accessor(d => d.bollingerbandCalculator);

		/* SERVER - START */
		const maxWindowSize = getMaxUndefined([waveband1, waveband2, subch, subjl, subd1, subd2, macdCalculator]);
		const dataToCalculate = inputData.slice(-LENGTH_TO_SHOW - maxWindowSize); // init data
		const calculatedData = changeCalculator(waveband1(waveband2(subd1(subd2(subch(subjl(subref0(subref20(subref80(subref100(macdCalculator(bollingerbandCalculator(dataToCalculate)))))))))))));
		const indexCalculator = discontinuousTimeScaleProviderBuilder().indexCalculator(); // for index calculation
		const {index} = indexCalculator(calculatedData); // computed index
		/* SERVER - END */

		const xScaleProvider = discontinuousTimeScaleProviderBuilder().withIndex(index);
		const {data: linearData, xScale, xAccessor, displayXAccessor} = xScaleProvider(calculatedData.slice(-LENGTH_TO_SHOW));

        // def pan update data state 
		this.state = {waveband1, waveband2, subd1, subd2, subch, subjl, subref0, subref20, subref80, subref100, 
            macdCalculator, bollingerbandCalculator, linearData, data: linearData, xScale, xAccessor, displayXAccessor, initialIndex: 0};
        // bind cur state above to download more
		this.handleDownloadMore = this.handleDownloadMore.bind(this);
        // for zoom button
        this.saveNode = this.saveNode.bind(this);
		this.resetYDomain = this.resetYDomain.bind(this);
		this.handleReset = this.handleReset.bind(this);
	}


    saveCanvas = node => {this.canvas = node;};

    // called when current component receiving new data
    append = newData => {
        const {data: inputData} = newData;
        const {waveband1, waveband2, subd1, subd2, subch, subjl, subref0, subref20, subref80, subref100, 
            macdCalculator, bollingerbandCalculator, initialIndex} = this.state;
        const maxWindowSize = getMaxUndefined([waveband1, waveband2, subd1, subd2, subch, subjl, macdCalculator]);
        /* SERVER - START */
        const dataToCalculate = newData.slice(-this.canvas.fullData.length - maxWindowSize);
        const calculatedData = waveband1(waveband2(subd1(subd2(subch(subjl(subref0(subref20(subref80(subref100(macdCalculator(bollingerbandCalculator(dataToCalculate))))))))))));
        const indexCalculator = discontinuousTimeScaleProviderBuilder().initialIndex(initialIndex).indexCalculator();
        const {index} = indexCalculator(calculatedData);
        /* SERVER - END */
        const xScaleProvider = discontinuousTimeScaleProviderBuilder().initialIndex(initialIndex).withIndex(index);
        const {data: linearData, xScale, xAccessor, displayXAccessor} = xScaleProvider(calculatedData.slice(-this.canvas.fullData.length));
        this.setState({waveband1, waveband2, subd1, subd2, subch, subjl, subref0, subref20, subref80, subref100, 
            macdCalculator, bollingerbandCalculator, linearData, data: linearData, xScale, xAccessor, displayXAccessor});
    };
    componentWillReceiveProps(nextProps){this.append(nextProps.data);}
    
    // for pan to load more
	handleDownloadMore(start, end){
		if (Math.ceil(start) === end) return;
		const {data: prevData, waveband1, waveband2, subd1, subd2, subch, subjl, subref0, subref20, subref80, subref100, 
            macdCalculator, bollingerbandCalculator} = this.state; // init data
		const {data: inputData} = this.props;// update data

		if (inputData.length === prevData.length) return;
		const rowsToDownload = end - Math.ceil(start);
		const maxWindowSize = getMaxUndefined([waveband1, waveband2, subd1, subd2, subch, subjl, macdCalculator]);

		/* SERVER - START */
		const dataToCalculate = inputData.slice(-rowsToDownload - maxWindowSize - prevData.length, - prevData.length);
		const calculatedData = waveband1(waveband2(subd1(subd2(subch(subjl(subref0(subref20(subref80(subref100(macdCalculator(bollingerbandCalculator(dataToCalculate))))))))))));
		const indexCalculator = discontinuousTimeScaleProviderBuilder().initialIndex(Math.ceil(start)).indexCalculator();
		const {index} = indexCalculator(calculatedData.slice(-rowsToDownload).concat(prevData));
		/* SERVER - END */
        
        // xscale idx for update data
		const xScaleProvider = discontinuousTimeScaleProviderBuilder().initialIndex(Math.ceil(start)).withIndex(index);
		const {data: linearData, xScale, xAccessor, displayXAccessor} = xScaleProvider(calculatedData.slice(-rowsToDownload).concat(prevData));

        // simulate a lag for ajax
		setTimeout(() => {
			this.setState({
				data: linearData,
				xScale,
				xAccessor,
				displayXAccessor,
                initialIndex: Math.ceil(start),//
			});
		}, 50);
	}

    // for reset & zoom button
    componentWillMount(){
        this.setState({
            suffix: 1
        });
    }
    saveNode(node){
        this.node = node;
    }
    resetYDomain(){
        this.node.resetYDomain();
    }
    handleReset(){
        this.setState({
            suffix: this.state.suffix + 1
        });
    }

	render() {
        // init
		const {type, width, ratio} = this.props;
		const {data, waveband1, waveband2, subd1, subd2, subch, subjl, subref0, subref20, subref80, subref100, 
            macdCalculator, bollingerbandCalculator, xScale, xAccessor, displayXAccessor} = this.state;
        // for zoom reset
        const {mouseMoveEvent, panEvent, zoomEvent, zoomAnchor} = this.props;
        const {clamp} = this.props;
        const xScaleProvider = discontinuousTimeScaleProvider.inputDateAccessor(d => d.date);
        const start = xAccessor(last(data));
		const end = xAccessor(data[Math.max(0, data.length - 100)]);
		const xExtents = [start+10, end];
        // for chart grid
		const showGrid = true;
        const height = 603;
		const margin = {left: 70, right: 70, top: 0, bottom: 20};
        const gridHeight = height - margin.top - margin.bottom;
		const gridWidth = width - margin.left - margin.right;
		const xGrid = showGrid? {innerTickSize:-1*gridHeight, tickStrokeOpacity:0.2, tickStrokeDasharray:'ShortDot', tickStrokeWidth:0.5} : {};
		const yGrid = showGrid? {innerTickSize:-1*gridWidth, tickStrokeOpacity:0.2, tickStrokeDasharray:'ShortDot', tickStrokeWidth:0.5} : {};

        // react render the following html module
					// <LineSeries yAccessor={waveband2.accessor()} stroke={waveband2.stroke()}/>
					// <LineSeries yAccessor={ema12.accessor()} stroke={ema12.stroke()}/>
		return (
			<ChartCanvas ratio={ratio} width={width} height={height} margin={margin} type={type} 
                    mouseMoveEvent={mouseMoveEvent} panEvent={panEvent} zoomEvent={zoomEvent} clamp={clamp} zoomAnchor={zoomAnchor}
                    xExtents={xExtents}
                    seriesName={`MSFT_${this.state.suffix}`}
					data={data}
					xScale={xScale} xAccessor={xAccessor} displayXAccessor={displayXAccessor}
					onLoadMore={this.handleDownloadMore}
                    ref={node => {this.saveCanvas(node);}}>

				<Chart id={1} height={400} yExtents={[d => [d.high, d.low], bollingerbandCalculator.accessor(), waveband1.accessor(), 
                    waveband2.accessor()]} padding={{top:10, bottom:10}}>

					<XAxis axisAt="bottom" orient="bottom" showTicks={false} outerTickSize={0} zoomEnabled={zoomEvent} 
                        tickFormat={d => timeFormat('%Y-%m-%d %H:%M')(data[d].date)}/>
					<YAxis axisAt="right" orient="right" ticks={5} {...yGrid} zoomEnabled={zoomEvent} />
					<MouseCoordinateY at="right" orient="right" displayFormat={format(".2f")} />

					<VolumeProfileSeries opacity={0.10} stroke={"#E6E6FA"} fill={d => d.close > d.open ? "#535A64" : "#535A64"} 
                        maxProfileWidthPercent={80}/>

					<EdgeIndicator itemType="last" orient="right" edgeAt="right" yAccessor={d => d.close} 
                        fill={d => d.close > d.open ? "#6BA583" : "#FF0000"}/>
                    
                    <LineSeries yAccessor={waveband1.accessor()} stroke={waveband1.stroke()} strokeWidth="24" strokeOpacity="0.1"/>
                    <LineSeries yAccessor={waveband2.accessor()} stroke={waveband2.stroke()} strokeWidth="24" strokeOpacity="0.3"/>

                    <ZoomButtons onReset={this.handleReset}/>

                    <BollingerSeries yAccessor={d => d.bollingerbandCalculator} stroke={bbStroke} fill={bbFill} />

                    <CandlestickSeries
						stroke={d => d.close > d.open ? "#6BA583" : "#DB0000"}
						wickStroke={d => d.close > d.open ? "#6BA583" : "#DB0000"}
						fill={d => d.close > d.open ? "#6BA583" : "#DB0000"} 
                    />

					<OHLCTooltip origin={[7, 10]}/>

					<BollingerBandTooltipv1 origin={[7, 30]} yAccessor={d => d.bollingerbandCalculator}
						options={bollingerbandCalculator.options()}/> 

					<LineGroupTooltips origin={[7, 34]}
						options={[
                            {yAccessor: waveband1.accessor(), type: waveband1.type(), stroke: waveband1.stroke(), ...waveband1.options(),},
                            {yAccessor: waveband2.accessor(), type: waveband2.type(), stroke: waveband2.stroke(), ...waveband2.options(),},
						]}
				    />
				</Chart>

				<Chart id={2} height={50} yExtents={[d => d.volume]} origin={(w, h)=>[0, h-233]}>
					<XAxis axisAt="bottom" orient="bottom" showTicks={false} outerTickSize={0} zoomEnabled={zoomEvent} />
					<YAxis axisAt="left" orient="left" showTicks={false} zoomEnabled={zoomEvent} />
					<MouseCoordinateY at="left" orient="left" displayFormat={format(".4s")} />
					<BarSeries yAccessor={d => d.volume} opacity="0.2" fill={d => d.close > d.open ? "#6BA583" : "#FF0000"} />
				</Chart>

				<Chart id={3} height={80} yExtents={[-30, subd1.accessor(), subd2.accessor(), subch.accessor(), subjl.accessor(), 
                    subref0.accessor(), subref20.accessor(), subref80.accessor(), subref100.accessor(), 100]} 
                    origin={(w, h) => [0, h-170]}>
					<XAxis axisAt="bottom" orient="bottom" showTicks={false} outerTickSize={0} zoomEnabled={zoomEvent} />
					<YAxis axisAt="left" orient="left" showTicks={true} ticks={2} zoomEnabled={zoomEvent} />
					<MouseCoordinateY at="right" orient="right" displayFormat={format(".4s")} />
                    <LineSeries yAccessor={subref0.accessor()} stroke={subref0.stroke()} strokeDasharray="ShortDash" strokeWidth="0.5" strokeOpacity="0.2"/>
                    <LineSeries yAccessor={subref20.accessor()} stroke={subref20.stroke()} strokeDasharray="ShortDash" strokeWidth="0.5" strokeOpacity="0.2"/>
                    <LineSeries yAccessor={subref80.accessor()} stroke={subref80.stroke()} strokeDasharray="ShortDash" strokeWidth="0.5" strokeOpacity="0.2"/>
                    <LineSeries yAccessor={subref100.accessor()} stroke={subref100.stroke()} strokeDasharray="ShortDash" strokeWidth="0.5" strokeOpacity="0.2"/>
                    <LineSeries yAccessor={subch.accessor()} stroke={subch.stroke()} strokeWidth="4" strokeOpacity="0.2"/>
                    <LineSeries yAccessor={subjl.accessor()} stroke={subjl.stroke()} strokeWidth="4" strokeOpacity="0.2"/>
                    <LineSeries yAccessor={subd2.accessor()} stroke={subd2.stroke()} strokeWidth="2" strokeOpacity="0.5"/>
                    <LineSeries yAccessor={subd1.accessor()} stroke={subd1.stroke()} strokeWidth="2" strokeOpacity="0.6"/>
				</Chart>

				<Chart id={4} height={60} yExtents={macdCalculator.accessor()} origin={(w, h) => [0, h-80]} padding={{top:0, bottom:2}} >
					<XAxis axisAt="bottom" orient="bottom" showTicks={true} outerTickSize={0} {...xGrid} zoomEnabled={zoomEvent} />
					<YAxis axisAt="left" orient="left" ticks={2} zoomEnabled={zoomEvent} />
					<MouseCoordinateX at="bottom" orient="bottom" rectWidth={10} rectHeight={18} displayFormat={timeFormat("%Y-%m-%d %H:%M")} />
					<MouseCoordinateY at="right" orient="right" displayFormat={format(".2f")} />
					<MACDSeries yAccessor={d => d.macd} {...macdAppearance} />
					<MACDTooltip origin={[7, 2]} yAccessor={d => d.macd} options={macdCalculator.options()} />
				</Chart>

				<CrossHairCursor />
			</ChartCanvas>
		);
	}
}

CandleStickChartPanToLoadMore.propTypes = {
	data: PropTypes.array.isRequired,
	width: PropTypes.number.isRequired,
	ratio: PropTypes.number.isRequired,
	type: PropTypes.oneOf(["svg", "hybrid"]).isRequired,
    mouseMoveEvent: true,
    panEvent: true,
    zoomEvent: true,
    clamp: false,
};

CandleStickChartPanToLoadMore.defaultProps = {
	type: "svg",
	mouseMoveEvent: true,
	panEvent: true,
	zoomEvent: true,
	clamp: false,
};

CandleStickChartPanToLoadMore = fitWidth(CandleStickChartPanToLoadMore);
export default CandleStickChartPanToLoadMore;

