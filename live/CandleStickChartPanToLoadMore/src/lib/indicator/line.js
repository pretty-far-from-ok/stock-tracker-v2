import {rebind, merge} from "../utils";
import {line} from "../calculator";
import baseIndicator from "./baseIndicator";

const ALGORITHM_TYPE = "LINE";

export default function() {

	const base = baseIndicator().type(ALGORITHM_TYPE).accessor(d => d.line);
	const underlyingAlgorithm = line();
	const mergedAlgorithm = merge().algorithm(underlyingAlgorithm).merge((datum, indicator) => { datum.line = indicator; });

	const indicator = function(data, options = {merge: true}) {
		if (options.merge) {
			if (!base.accessor()) throw new Error(`Set an accessor to ${ALGORITHM_TYPE} before calculating`);
            const merged_data = mergedAlgorithm(data)
            // get rid of ""(0 in javasript) -> undefined
            const res = merged_data.map((obj)=>{
                if(obj.underlay_waveband==""){obj.underlay_waveband=undefined;}
                if(obj.waveband2==""){obj.waveband2=undefined;}
                if(obj.d_down==""){obj.d_down=undefined;}
                if(obj.d_underlay==""){obj.d_underlay=undefined;}
                // if(obj.oversold==""){obj.oversold=undefined;}
                return obj;
            });
			return res;
		}
		return underlyingAlgorithm(data);
	};
	rebind(indicator, base, "id", "accessor", "stroke", "fill", "echo", "type");
	rebind(indicator, underlyingAlgorithm, "undefinedLength");
	rebind(indicator, underlyingAlgorithm, "options");
	rebind(indicator, mergedAlgorithm, "merge", "skipUndefined");

	return indicator;
}
