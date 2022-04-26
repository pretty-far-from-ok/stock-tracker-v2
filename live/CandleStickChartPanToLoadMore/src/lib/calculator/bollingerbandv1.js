// https://github.com/ScottLogic/d3fc/blob/master/src/indicator/algorithm/calculator/bollingerBands.js
import {mean, deviation} from "d3-array";
import ema from "./ema";
import {last, slidingWindow, zipper, path} from "../utils";
import {BollingerBandv1 as defaultOptions} from "./defaultOptionsForComputation";

// V5:=(LOW+HIGH+CLOSE)/3; S:MA(V5,18)+2*STD(V5,21); X:MA(V5,13)-2*STD(V5,13);
export default function() {
	let options = defaultOptions;

	function calculator(data) {
        // options
		const {windowSize1, windowSize2, windowSize3, windowSize4, multiplier, movingAverageType, sourcePath1, sourcePath2, sourcePath3} = options;
        // v5
        const source = path(sourcePath1);
        // set mean up bollinger
		const meanAlgorithm1 = movingAverageType === "ema"? ema().options({windowSize1, sourcePath1})
			: slidingWindow().windowSize(windowSize1).accumulator(values => mean(values)).sourcePath(sourcePath1);
        // set mean down bollinger
		const meanAlgorithm2 = movingAverageType === "ema"? ema().options({windowSize2, sourcePath1})
			: slidingWindow().windowSize(windowSize2).accumulator(values => mean(values)).sourcePath(sourcePath1);
        // set mean mid bollinger
		const meanAlgorithm3 = slidingWindow().windowSize(windowSize3).accumulator(values => mean(values)).sourcePath(sourcePath2);
		const meanAlgorithm4 = slidingWindow().windowSize(windowSize3).accumulator(values => values).sourcePath(sourcePath3);
        // set bollinger algorithm
		const bollingerBandAlgorithm1 = slidingWindow().windowSize(windowSize1).accumulator((values) => {
            const avg = last(values).mean;
            const stdDev = deviation(values, (each) => source(each.datum));
            return {top: avg + multiplier * stdDev};
        });
		const bollingerBandAlgorithm2 = slidingWindow().windowSize(windowSize2).accumulator((values) => {
            const avg = last(values).mean;
            const stdDev = deviation(values, (each) => source(each.datum));
            return {bottom: avg - multiplier * stdDev};
        });
		const bollingerBandAlgorithm3 = slidingWindow().windowSize(windowSize3).accumulator((values) => {
            const avg = last(values).mean;
            return {middle0: avg};
        });
		const bollingerBandAlgorithm4 = slidingWindow().windowSize(windowSize3).accumulator((values) => {
            const avg = last(values).mean;
            return {middle1: avg};
        });

		const zip = zipper().combine((datum, mean) => ({datum, mean}));
		const tuples1 = zip(data, meanAlgorithm1(data));
		const tuples2 = zip(data, meanAlgorithm2(data));
		const tuples3 = zip(data, meanAlgorithm3(data));
        // get rid of ""(0 in javascript) -> undefined
		const tuples4 = zip(data, data.map((obj)=>{if(obj.midbolling2==""){return undefined} else{return obj.midbolling2}}));
        const obj1 = bollingerBandAlgorithm1(tuples1);  // up bollinger
        const obj2 = bollingerBandAlgorithm2(tuples2);  // down bollinger
        const obj3 = bollingerBandAlgorithm3(tuples3);  // mid bollinger
        const obj4 = bollingerBandAlgorithm4(tuples4);  // mid bollinger decline segment
        const res = obj1.map((o, i) => {return {...o, ...obj2[i], ...obj3[i], ...obj4[i]}})  // combine
		return res;
	}
	calculator.undefinedLength = function() {
        // use maximum of windowsize for undefinedLength computing
		const {windowSize1} = options;
		return windowSize1 - 1;
	};
	calculator.options = function(x) {
		if (!arguments.length) {
			return options;
		}
		options = { ...defaultOptions, ...x };
		return calculator;
	};

	return calculator;
}
