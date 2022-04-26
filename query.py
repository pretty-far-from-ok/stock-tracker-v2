import numpy as np
import pandas as pd
from collections import OrderedDict

from pytdx.exhq import TdxExHq_API
from pytdx.hq import TdxHq_API

from query_config import minconfig, MINCONFIG


def rename(df):
    if 'vol' in df:
        df = df.rename(columns={'vol':'volume'})
    if 'trade' in df:
        df = df.rename(columns={'trade':'volume'})
    if 'datetime' in df:
        df = df.rename(columns={'datetime':'date'})
    return df 

def exchange_drop_col(df):
    cols = ["date", "open", "high", "low", "close", "volume"]
    df=df.reindex(columns=cols)
    return df

def get_kline_stock_bars(switch, API, marketcode, stockcode):  # 1stock 
    datalst = []
    num = 1
    cfg = minconfig if switch else MINCONFIG
    for _ in range(num):
        if(switch):
            # [OrderedDict([('open', 5068.0), ('high', 5069.0), ('low', 5065.0), ('close', 5066.0), ('position', 437158), ('trade', 1397), ('price', 0.0), ('year', 2022), ('month', 4), ('day', 25), ('hour', 2), ('minute', 30), ('datetime', '2022-04-25 02:30'), ('amount', 6.125888340673084e-40)])]
            data = API.get_instrument_bars(category=cfg.TDX_PARAMS, market=marketcode, code=stockcode, start=(num-1-_)*cfg.NUM_INFORMATIONS, count=cfg.NUM_INFORMATIONS)
            if(data is None):  # invalid
                datalst += [OrderedDict([('open', 0), ('high', np.nan), ('low', 0), ('close', 0), ('position', 0), ('trade', 0), ('price', 0), ('year', 0), ('month', 0), ('day', 0), ('hour', 0), ('minute', 0), ('datetime', 'xxxx-xx-xx xx:xx'), ('amount', 0)])]
            else:  # valid
                datalst += data
        else:
            data = API.get_security_bars(category=cfg.TDX_PARAMS, market=marketcode, code=stockcode, start=(num-1-_)*cfg.NUM_INFORMATIONS, count=cfg.NUM_INFORMATIONS)
            if(data is None):  # invalid
                datalst += [OrderedDict([('open', 0), ('high', np.nan), ('low', 0), ('close', 0), ('position', 0), ('trade', 0), ('price', 0), ('year', 0), ('month', 0), ('day', 0), ('hour', 0), ('minute', 0), ('datetime', 'xxxx-xx-xx xx:xx'), ('amount', 0)])]
            else:  # valid
                datalst += data
    data = API.to_df(datalst)
    data = exchange_drop_col(rename(data))
    return data

def get_kline_stock_barsv2(switch, API, marketcode, stockcode):  # 1stock 
    datalst = []
    num = 1
    cfg = minconfig if switch else MINCONFIG
    for _ in range(num):
        if(switch):
            # [OrderedDict([('open', 5068.0), ('high', 5069.0), ('low', 5065.0), ('close', 5066.0), ('position', 437158), ('trade', 1397), ('price', 0.0), ('year', 2022), ('month', 4), ('day', 25), ('hour', 2), ('minute', 30), ('datetime', '2022-04-25 02:30'), ('amount', 6.125888340673084e-40)])]
            data = API.get_instrument_bars(category=cfg.TDX_PARAMS, market=marketcode, code=stockcode, start=(num-1-_)*cfg.NUM_INFORMATIONSv2, count=cfg.NUM_INFORMATIONSv2)
            if(data is None):  # invalid
                datalst += [OrderedDict([('open', 0), ('high', np.nan), ('low', 0), ('close', 0), ('position', 0), ('trade', 0), ('price', 0), ('year', 0), ('month', 0), ('day', 0), ('hour', 0), ('minute', 0), ('datetime', 'xxxx-xx-xx xx:xx'), ('amount', 0)])]
            else:  # valid
                datalst += data
        else:
            data = API.get_security_bars(category=cfg.TDX_PARAMS, market=marketcode, code=stockcode, start=(num-1-_)*cfg.NUM_INFORMATIONSv2, count=cfg.NUM_INFORMATIONSv2)
            if(data is None):  # invalid
                datalst += [OrderedDict([('open', 0), ('high', np.nan), ('low', 0), ('close', 0), ('position', 0), ('trade', 0), ('price', 0), ('year', 0), ('month', 0), ('day', 0), ('hour', 0), ('minute', 0), ('datetime', 'xxxx-xx-xx xx:xx'), ('amount', 0)])]
            else:  # valid
                datalst += data
    data = API.to_df(datalst)
    data = exchange_drop_col(rename(data))
    return data

# mainloop thread version for datarequest -> when requesting data, will block mainloop thread
def datarequest(switch, marketcode, stockcode):
    # connect 
    CONNECT_TIMEOUT = 5.000
    try:
        if(switch):
            API = TdxExHq_API(heartbeat=True)
            API.connect(ip='119.97.142.130', port=7721, time_out=CONNECT_TIMEOUT)
        else:
            API = TdxHq_API(heartbeat=True)
            API.connect(ip='119.147.212.81', port=7709, time_out=CONNECT_TIMEOUT)
    except TimeoutError:
        lastdata = ['xxxx-xx-xx xx:xx', np.nan, 0, 0, 0, 0]
        return lastdata
    else:
        # get
        data = get_kline_stock_bars(switch, API, marketcode, stockcode)  # df: date open high low close volume
        if(data.empty):
            lastdata = ['xxxx-xx-xx xx:xx', 0, np.nan, 0, 0, 0]
        else:
            lastdata = data.iloc[-1].to_list()
        # disconnect
        API.disconnect()
        return lastdata  # lst[strdate, o, h, l, c, v]

# multithread version for datarequest
# ref https://stackoverflow.com/questions/6893968/how-to-get-the-return-value-from-a-thread-in-python
def datarequestv1(switch, marketcode, stockcode, datalst, _):
    try:
        # connect 
        CONNECT_TIMEOUT = 5.000
        if(switch):
            API = TdxExHq_API(heartbeat=True)
            API.connect(ip='119.97.142.130', port=7721, time_out=CONNECT_TIMEOUT)
        else:
            API = TdxHq_API(heartbeat=True)
            API.connect(ip='119.147.212.81', port=7709, time_out=CONNECT_TIMEOUT)
    except TimeoutError:  # connection timeout
        datalst[_] = ['xxxx-xx-xx xx:xx', np.nan, 0, 0, 0, 0]
    except:  # other error
        datalst[_] = ['xxxx-xx-xx xx:xx', 0, 0, 0, 0, np.nan]
    else:  # if no error occur
        # get
        data = get_kline_stock_bars(switch, API, marketcode, stockcode)  # df: date open high low close volume
        if(data.empty):
            lastdata = ['xxxx-xx-xx xx:xx', 0, 0, np.nan, 0, 0]
        else:
            lastdata = data.iloc[-1].to_list()
        datalst[_] = lastdata # lst[strdate0, o1, h2, l3, c4, v5]
        # disconnect
        API.disconnect()

# multithread version for datarequest -> for signal.py to derive a certain num of dots
def datarequestv2(switch, marketcode, stockcode, datalst, _,):
    try:
        # connect 
        CONNECT_TIMEOUT = 5.000
        if(switch):
            API = TdxExHq_API(heartbeat=True)
            API.connect(ip='119.97.142.130', port=7721, time_out=CONNECT_TIMEOUT)
        else:
            API = TdxHq_API(heartbeat=True)
            API.connect(ip='119.147.212.81', port=7709, time_out=CONNECT_TIMEOUT)
    except TimeoutError:  # connection timeout error sign
        datalst[_] = 'x' 
    except:  # other connection error sign
        datalst[_] = 'xx' 
    else:  # if connect succeed 
        data = get_kline_stock_barsv2(switch, API, marketcode, stockcode)  # df: date open high low close volume
        if(data.empty):  # invalid data sign
            datalst[_] = 'xxx' 
        else:  # valid data
            pass
        # disconnect
        API.disconnect()
        return data

# if __name__ == '__main__':
#     # init
#     switch=1
#     data, time = datarequest(switch, 28, "CF2205")
#     print(type(data[0]))



# disconnect
# API.disconnect()


