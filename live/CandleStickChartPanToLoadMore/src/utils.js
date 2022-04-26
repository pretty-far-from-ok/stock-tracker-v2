import {tsvParse, csvParse} from  "d3-dsv";
import {timeParse} from "d3-time-format";
import axios from 'axios';

// 1
function parse_for_init(parse) {
	return function(d) {
		d.date = parse(d.date);
		d.open = +d.open;
		d.high = +d.high;
		d.low = +d.low;
		d.close = +d.close;
		d.volume = +d.volume;
		return d;
	};
}
export function initData() {
    // const parseDate = timeParse("%Y-%m-%d");
    const parseDate = timeParse("%Y-%m-%d %H:%M");
	// const promiseMSFT = fetch("https://cdn.rawgit.com/rrag/react-stockcharts/master/docs/data/MSFT.tsv")
    // const initdata = fetch("./data/MSFT.tsv").then(response => response.text()).then(data => tsvParse(data, parse_for_init(parseDate)))
    const initdata = fetch("./data/test.tsv").then(response => response.text()).then(data => tsvParse(data, parse_for_init(parseDate)))
    // console.log(initdata)
	return initdata;
}
// 2
function parse_for_update(d, parse) {
    d.date = parse(d.date);
    d.open = +d.open;
    d.high = +d.high;
    d.low = +d.low;
    d.close = +d.close;
    d.volume = +d.volume;
    return d;
}
// convert json date str to d3 timeformat
export function handlejson(updatedata) {
    const parseDate = timeParse("%Y-%m-%d %H:%M");
    const data = parse_for_update(updatedata, parseDate);
    // console.log(data) 10:06
    return data;
}

