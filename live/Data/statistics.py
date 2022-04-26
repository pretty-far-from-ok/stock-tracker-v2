import pandas as pd

# ------------ statistics func ---------- 
def LLV(arr: pd.Series, n:int):
    '''Returns the lowest value in window n'''
    return pd.Series(arr).rolling(n).min()

def HHV(arr: pd.Series, n:int):
    '''Returns the highest value in window n'''
    return pd.Series(arr).rolling(n).max()

def MEAN(arr: pd.Series, n: int) -> pd.Series:
    '''Returns n-period mean value of arr'''
    return pd.Series(arr).rolling(n).mean()

def STD(arr: pd.Series, n: int) -> pd.Series:
    '''Returns n-period standard deviation of arr'''
    return pd.Series(arr).rolling(n).std()

def SMA(arr: pd.Series, n: int) -> pd.Series:
    '''Returns n-period simple moving average of array arr.'''
    return pd.Series(arr).rolling(n).mean()

def EMA(arr: pd.Series, n:int) -> pd.Series:
    '''
    Returns exponential moving average value of arr
    Set adjust=False for computing EMA
    https://blog.csdn.net/weixin_41494909/article/details/99670246
    '''
    return pd.Series(arr).ewm(span=n, adjust=False, ignore_na=False).mean()

def AVEDEV(arr: pd.Series, n: int) -> pd.Series:
    '''Returns the average deviation value of arr'''
    def compute_AVEDEV(_):
        diff = _ - sum(_)/n
        return sum(abs(diff))/n
    return pd.Series(arr).rolling(n).apply(compute_AVEDEV)

