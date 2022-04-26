import numpy as np
import pandas as pd
import asyncio
import random
import datetime
import websockets
import json

from pytdx.exhq import TdxExHq_API
from pytdx.hq import TdxHq_API

from utils import datarequest, reform, datainitializer, addv5, addv6, check_for_1130
from utils import switch, period
from initializer import initializer

# import configparser
# config = configparser.ConfigParser()
# config.read('../../config/default.ini')
# switch = int(config['DEFAULT']['switch'])

# connnect
API = TdxExHq_API(heartbeat=True) if switch else TdxHq_API(heartbeat=True)
CONNECT_TIMEOUT = 5.000

# todo: fix the bugs when on 11:29 -> 11:30, the pytdx api returns 13:00 timestamp as returns
if __name__ == '__main__':

    # connect 
    if(switch):
        API.connect(ip='119.97.142.130', port=7721, time_out=CONNECT_TIMEOUT)
    else:
        API.connect(ip='119.147.212.81', port=7709, time_out=CONNECT_TIMEOUT)
    # init
    print("initializing...")
    initdata, initdatatime = datarequest(API, switch)
    source_dict = initializer(initdata, 0, 800)  # compute
    source_df = pd.DataFrame(source_dict)
    source_df = addv5(source_df)
    source_df = addv6(source_df)
    source_df = check_for_1130(source_df)
    datainitializer(source_df)
    print(f"data of date {initdatatime} writen to init file for react app.")
    # disconnect
    API.disconnect()

    # exit(0)

    # update
    print("updating...")
    try:
        async def handler(websocket):
            # connect
            if(switch):
                API.connect(ip='119.97.142.130', port=7721, time_out=CONNECT_TIMEOUT)
            else:
                API.connect(ip='119.147.212.81', port=7709, time_out=CONNECT_TIMEOUT)
            while True:
                data, datatime = datarequest(API, switch)
                print(datatime)
                update_dict = initializer(data, 0, 800)  # compute
                update_df = pd.DataFrame(update_dict)
                update_df = addv5(update_df)
                update_df = addv6(update_df)
                update_df = check_for_1130(update_df)
                # https://stackoverflow.com/questions/15228651/how-to-parse-json-string-containing-nan-in-node-js
                # json cannot handle nan, replace by ''(null str)
                update_df = update_df.replace(np.nan, '', regex=True)
                datadict = update_df.iloc[-1].to_dict()  # -> series
                # datadict = data.iloc[-1].to_dict()  # -> series
                dumps = json.dumps(datadict)
                # check client socket connection: https://stackoverflow.com/questions/63683332/python-websockets-onclose
                try:
                    await websocket.send(dumps)
                except websockets.exceptions.ConnectionClosed:
                    print("client server on safari closed.")
                    break
                await asyncio.sleep(1)
        start_server = websockets.serve(handler, host='127.0.0.1', port=5000)
        asyncio.get_event_loop().run_until_complete(start_server)
        asyncio.get_event_loop().run_forever()

    finally:
        # disconnect
        API.disconnect()
        print("updating to react app end.")


