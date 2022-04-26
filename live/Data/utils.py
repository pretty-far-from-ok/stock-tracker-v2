import pandas as pd

import configparser
config = configparser.ConfigParser()
config.read('../../config/default.ini')
switch = int(config['DEFAULT']['switch'])
period = int(config['DEFAULT']['period'])
marketcode = int(config['DEFAULT']['marketcode'])
stockcode = config['DEFAULT']['stockcode']
start = int(config['DEFAULT']['start'])
num = int(config['DEFAULT']['num'])

# print(switch, " ", period," ", marketcode, " ", stockcode, " ", start, " ", num)

def rename(df):
    if 'vol' in df:
        df = df.rename(columns={'vol':'volume'})
    if 'trade' in df:
        df = df.rename(columns={'trade':'volume'})
    if 'datetime' in df:
        df = df.rename(columns={'datetime':'date'})
    return df 

def drop_unused_cols(df):
    # open close high low volume (amount year month day hour minute) datetime
    df = df.drop(df.columns[[5, 6, 7, 8, 9, 10]], axis=1)
    return df

def exchange_drop_col(df):
    cols = ["date", "open", "high", "low", "close", "volume"]
    df=df.reindex(columns=cols)
    return df

def get_kline_stock_bars(API, switch):  # 1stock 
    if(switch):
        data = API.get_instrument_bars(category=period, market=marketcode, code=stockcode, start=0, count=num)
    else:
        data = API.get_security_bars(category=period, market=marketcode, code=stockcode, start=0, count=num)
    data = API.to_df(data)
    data = exchange_drop_col(rename(data))
    return data

def datarequest(API, switch):
    data = get_kline_stock_bars(API, switch)  # df: date open high low close volume
    time = data['date'].to_list()[-1]
    return data, time  # df, str

def reform(update_data):
    # reform update data
    lst = update_data.to_list()
    lst = [str(_) for _ in lst]
    delimiter = '\t'
    strlst = []
    strlst.append(delimiter.join(lst)+'\t\t')  # ['2022-04-07 15:00\t16.29\t16.29\t16.29\t16.29\t798400.0\t\t']
    return strlst[0]

def addv5(df):
    # V5:=(LOW+HIGH+CLOSE)/3;
    df['v5'] = (df['high']+df['low']+df['close'])/3
    return df

def addv6(df):
    # V5:=(HIGH+LOW+3*CLOSE)/5;
    df['v6'] = (df['high']+df['low']+3*df['close'])/5
    return df

def check_for_1130(df):
    # fix bugs pytdx return wrong date value:
    # 798  2022-04-19 11:29 ...
    # 799  2022-04-19 13:00 ...
    datestr = df.iloc[-1].date
    s = datestr[:-5] + '11:30' if datestr.endswith('13:00') else datestr
    df.iloc[-1, df.columns.get_loc('date')] = s 
    return df

def datainitializer(df):
    df.to_csv('../CandleStickChartPanToLoadMore/public/data/test.tsv', mode='w', index=False, header=True, sep="\t")

def append_tsv(df):
    df.to_csv('../CandleStickChartPanToLoadMore/public/data/test.tsv', mode='a', index=False, header=False, sep="\t")


