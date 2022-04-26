// https://github.com/ScottLogic/d3fc/blob/master/src/indicator/algorithm/calculator/macd.js
import ema from "./ema";
import {isDefined, zipper} from "../utils";
import {MACD as defaultOptions} from "./defaultOptionsForComputation";

export default function() {
	let options = defaultOptions;

	function calculator(data) {
		const {fast, slow, signal, sourcePath} = options;

		const fastEMA = ema().options({windowSize: fast, sourcePath});
		const slowEMA = ema().options({windowSize: slow, sourcePath});
		const signalEMA = ema().options({ windowSize: signal, sourcePath: undefined });

		const macdCalculator = zipper()
			.combine((fastEMA, slowEMA) => (isDefined(fastEMA) && isDefined(slowEMA)) ? fastEMA - slowEMA : undefined);

		const macdArray = macdCalculator(fastEMA(data), slowEMA(data));

		const undefinedArray = new Array(slow);
		const signalArray = undefinedArray.concat(signalEMA(macdArray.slice(slow)));

		const zip = zipper().combine((macd, signal) => ({macd, signal, divergence: (isDefined(macd) && isDefined(signal))? macd - signal : undefined,}));

		const macd = zip(macdArray, signalArray);

		return macd;
	}

	calculator.undefinedLength = function() {
		const {slow, signal} = options;
		return slow + signal - 1;
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
