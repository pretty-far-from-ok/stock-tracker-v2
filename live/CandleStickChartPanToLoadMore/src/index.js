// --------------------------  for backtesting (config ./Chart.js) ----------------------------
// import React from 'react';
// import {render, ReactDOM} from 'react-dom';
// import Chart from './Chart';
// import {getData} from "./utils"
// import { TypeChooser } from "react-stockcharts/lib/helper";
// 
// // when chart component is instantiated, func below are called by order
// // 1 constructor()
// // 2 static getDerivedStateFromProps()
// // 3 render()
// // 4 componentDidMount()
// 
// class ChartComponent extends React.Component {
// 	componentDidMount() {
// 		getData().then(data => {this.setState({data})})
// 	}
// 	render() {
// 		if (this.state == null) {
// 			return <div>Loading...</div>
// 		}
// 		return (
//             <Chart type={"hybrid"} data={this.state.data} />
// 			// <TypeChooser>
// 			// 	{type => <Chart type={type} data={this.state.data} />}
// 			// </TypeChooser>
// 		)
// 	}
// }
// render(<ChartComponent />, document.getElementById("root"));

// --------------------------  for realtime stocking (config Chart.js) ----------------------------
// ref https://github.com/ivailop7/LiveStreamingWithWebsockets
// ref https://websockets.readthedocs.io/en/stable/reference/server.html?highlight=serve#websockets.server.serve
import React from "react";
import ReactDOM from "react-dom";
import Chart from "./Chart";
import {initData, handlejson} from "./utils";
import * as d3 from "d3";

class App extends React.Component {
    constructor(props) {
        super(props);
        this.dataIndex = 0;
        this.prevtime;
        this.curtime;
        // set supervision:
        this.supervisionInterval = 1000;
        this.supervisionDuration = 10;
        this.supervisionEnd = d3.timeMinute.offset(new Date(), this.supervisionDuration);
        // set socket
        this.socket = new WebSocket("ws://127.0.0.1:5000/");
    }

    componentDidMount() {
        // todo: set static/dynamic chart state according to the data server existense
        // see -> https://stackoverflow.com/questions/38732639/accessing-object-in-returned-promise-using-fetch-w-react-js
        // initData().then(data => {this.setState({data});});
        initData().then(data => {this.setState({data}, this.updateData());});
        // connect
        this.socket.onopen = () => {console.log('opened connection!')};
        // set state: json.parse(data)->currentdata
        this.socket.onmessage = (event) => {
            this.setState({updatedata: handlejson(JSON.parse(event.data))});
        };
    }

    componentWillUnmount() {
        clearInterval(this.intervalId);
        // disconnect
        this.socket.onclose = () => {console.log('closed connection!')};
    }

    // todo: update data in a block way
    updateData() {
        this.intervalId = setInterval(() => {
            // derive current data arr
            var {data} = this.state;
            const {updatedata} = this.state;
            this.prevtime = data[data.length-1].date;
            this.curtime = updatedata.date;
            // console.log(this.prevtime, this.curtime)
            // derive new datapoint => by websocket
            let dataPoint;
            dataPoint = {...updatedata};
            // console.log(dataPoint);
            // derive lastbar
            const lastBar = data[data.length-1];
            // check -> see https://stackoverflow.com/questions/4587060/determining-date-equality-in-javascript
            if(this.curtime.getTime() === this.prevtime.getTime()){
                dataPoint.date = lastBar.date;
                // del last item in data
                data = data.slice(0, data.length-1);
                // add new
                data.push(dataPoint);
            }
            else{
                // dataPoint.date = d3.timeDay.offset(lastBar.date, 1);
                dataPoint.date = d3.timeMinute.offset(lastBar.date, 1);
                // append new datapoint into existing data arr
                data.push(dataPoint);
                this.prevtime = this.curtime;
            }
            // render
            this.setState({ data });
            // end the supervision
            // if(new Date() > this.supervisionEnd) {
            //     clearInterval(this.intervalId);
            // }
        }, this.supervisionInterval);
    };

    render() {
        if (this.state == null) {
            return <div>Loading...</div>;
        }
        return (
            <Chart type={"hybrid"} data={this.state.data} />
            // <TypeChooser>
            // {type => <Chart type={type} data={this.state.data} />}
            // </TypeChooser>
        );
    }
}

const rootElement = document.getElementById("root");
ReactDOM.render(<App />, rootElement);

