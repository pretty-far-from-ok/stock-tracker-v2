### Stock-Tracker-v2
A live stock tracker for `live price` + `OHLCV chart` + `live trading signals` monitoring / prompting.

The demo is based on tkinter with requirements as in ./requirements.txt. <br>

Thanks to ref: [briantam/Stock-Tracker](https://github.com/briantam/Stock-Tracker), for simply borrow the main frame of it.

Thanks to ref: [react-stock-chart](https://github.com/rrag/react-stockcharts), for simply borrow the main frame of it.

### Overview
<center><img src="./overview.png" width="60%"></center>

### Usage
##### Environment
- Use `virtualenv` for projection environment isolation:
    - 1. `python3 -m venv myvenv` create virtual env in 'myvenv'.
    - 2. `source myvenv/bin/activate` activate venv shell.
    - 3. `pip3 install -r /path/to/requirements.txt` to install all depedencies in myvenv.
    - 4. `deactivate` to exit myvenv.
- Try `pip3 freeze > requirements.txt` to get the requirements list needed in this project.

##### Main
- Use `python3 main.py` to Start the tkinter app mainloop.
