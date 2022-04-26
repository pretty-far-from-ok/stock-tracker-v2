### Live-Stock-Visualizer
A Live visualizer for stock/future web app, which supports self-designed indicators/highly cusomized chart layout/appearance features.

Thanks to [react-stock-chart](https://rrag.github.io/react-stockcharts/index.html) for simplely borrow the main lib frame of it.

### Overview
<center><img src="./overview.png" width="100%"></center>

### Usage
##### Environment
- Use `virtualenv` for projection environment isolation:
    - 1. `python3 -m venv myvenv` create virtual env in 'myvenv'.
    - 2. `source myvenv/bin/activate` activate venv shell.
    - 3. `pip3 install -r /path/to/requirements.txt` to install all depedencies in myvenv.
    - 4. `deactivate` to exit myvenv.
- Try `pip3 freeze > requirements.txt` to get the requirements list needed in this project.

##### Data
- `config` data request pytdx api parameters setting.
- `statistics` some statistical compuation base functions: SMA, EMA, etc.
- `indicator` self-designed indicator computations.
- `initializer` data post-processing, to generate all the data need for react-stock-chart plot.
- `send` build a live data send server for react app, using websockets.
- `utils` some auxilary functions.

##### React Graphd Visualizer 
- `public`
    - `data` startup data csv/tsv holder.
    - `index.html/manifest` created by `Create React App`.
- `src`
    - `lib` a self-organized react-stock-chart lib used for chart plottings.
    - `Chart.js` main chart react js wrapper file.
    - `Chartinit` main chart react chart js file - <b>CORE</b>.
    - `index` websocket data receiver, use react `setState` to update the chart when live data comes.
    - `updatingDataWrapper` a wrapper for <b>STATIC</b> data dynamic backtesting playback.
    - `utils` some data parse / preprocessing functions.

##### RUN the Programme
- `cd ./Data` and run with `python3 send.py` to start data send server.
- `cd ./CandleStickChartPanToLoadMore` and use with `npm start` to start react web-app server.
- Go `localhost:3000` for live price chart.

##### TODO
The react webserver should work in a <b>BLOCK WAY</b> to accepting the data sent from sender.

