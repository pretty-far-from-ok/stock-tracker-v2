// https://github.com/ScottLogic/d3fc/blob/master/src/indicator/algorithm/calculator/bollingerBands.js
import {mean, deviation} from "d3-array";
import ema from "./ema";
import {last, slidingWindow, zipper, path} from "../utils";
import {BollingerBand as defaultOptions} from "./defaultOptionsForComputation";

export default function() {
	let options = defaultOptions;

	function calculator(data) {
		const {windowSize, multiplier, movingAverageType, sourcePath} = options;

		const source = path(sourcePath);
		const meanAlgorithm = movingAverageType === "ema"? ema().options({windowSize, sourcePath})
			: slidingWindow().windowSize(windowSize).accumulator(values => mean(values)).sourcePath(sourcePath);

		const bollingerBandAlgorithm = slidingWindow().windowSize(windowSize).accumulator((values) => {
				const avg = last(values).mean;
				const stdDev = deviation(values, (each) => source(each.datum));
				return {
					top: avg + multiplier * stdDev,
					middle: avg,
					bottom: avg - multiplier * stdDev
				};
			});

		const zip = zipper().combine((datum, mean) => ({ datum, mean }));

		const tuples = zip(data, meanAlgorithm(data));
		return bollingerBandAlgorithm(tuples);
	}
	calculator.undefinedLength = function() {
		const { windowSize } = options;
		return windowSize - 1;
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
