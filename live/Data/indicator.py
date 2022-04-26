import numpy as np
import pandas as pd
from statistics import *

#  ------------ bolling ------------
def UpBolling(arr1: pd.Series, arr2: pd.Series) -> pd.Series:
    '''Returns up bolling line: (arr1+2arr2)'''
    return pd.Series(arr1)+2*pd.Series(arr2)

def split_decreasing(lst):  # for ohlc midbolling2/waveband2 subgraph waveband2
    ''' 
    splits the given lst into monotonically decreasing subarrays of size>=2
    see https://stackoverflow.com/questions/68367598/how-do-you-split-a-list-into-monotonically-increasing-decreasing-lists
    ''' 
    split_points = (np.where(np.diff(lst) > 0)[0] + 1).tolist()  # lst
    sub_lists = np.split(lst, split_points)
    lll = []
    for sub in sub_lists:
        if sub.size>=2:
            lll.extend(list(sub)) 
        else:
            lll.append(np.nan)
    return lll 

def DownBolling(arr1: pd.Series, arr2: pd.Series) -> pd.Series:
    '''Returns mid bolling line: (arr1+2arr2)'''
    return pd.Series(arr1)-2*pd.Series(arr2)

#  ------------ waveband ------------   
# split_decreasing()

#  ------------ oversold blue dots ------------
def OverSoldSign(arr_x: pd.Series, arr_l: pd.Series, arr_h: pd.Series, arr_b: pd.Series) -> pd.Series:
    '''
    Returns oversold blue/red dots. blue for k under downbolling 
    x: downbolling, l=low, h=high, b=waveband
    TODO: red for downbolling upcross waveband. 
    '''
    assert arr_x.size == arr_b.size
    assert arr_x.size == arr_h.size
    arr = arr_l-(arr_h-arr_l)/1  # L-(H-L)/3
    arr_blue_dot = pd.Series(arr).copy(deep=True)
    num = arr_blue_dot.size
    for _ in range(num):
        if(arr_l[_]>=arr_x[_]):
            arr_blue_dot.iat[_] = np.nan # clear up  pd convert none to nan automatically for dtype=numeric value
    return arr_blue_dot

# ------------ sub graph --------------
def GetSlope(arr: pd.Series, n:int) -> pd.Series:
    '''
    Return rolling(window=n) slopes.
    See https://stackoverflow.com/questions/59737923/computing-rolling-slope-on-a-large-pandas-dataframe for details
    '''
    from scipy.stats import linregress

    def compute_slope(_):
        output = linregress(list(range(len(_))), _)
        return output.slope

    kdott = pd.Series(arr)
    slopes = kdott.rolling(n).apply(compute_slope)
    return slopes

def GetM(arr1: pd.Series, arr2: pd.Series, n:int, m:int) -> pd.Series:
    '''Returns the M value for subgraph'''
    slope = pd.Series(arr1)
    kdott = pd.Series(arr2)
    return EMA(slope*n+kdott, m)

def GetSP(arr1: pd.Series, arr2: pd.Series, arr3: pd.Series, n:int, m:int):
    '''
    Returns the SP value for subgraph
    '''
    closing = pd.Series(arr1)
    low = pd.Series(arr2)
    high = pd.Series(arr3)
    return (closing - LLV(low, n))/(HHV(high, n)-LLV(low, n))*100

def GetQIU(arr: pd.Series, n:int) -> pd.Series:
    '''Returns the qiu value for subgraph'''
    SP = pd.Series(arr)
    return MEAN(SP, n)

def GetDONG(arr: pd.Series, n:int) -> pd.Series:
    '''Returns the dong value for subgraph'''
    QIU = pd.Series(arr)
    return MEAN(QIU, n)

def GetF1(arr1: pd.Series, arr2: pd.Series, n:int, m:int) -> pd.Series:
    '''Returns the f1 value for subgraph'''
    QIU = pd.Series(arr1)
    DONG = pd.Series(arr2)
    return n*QIU-m*DONG

def GetZC(arr: pd.Series, n:int, m:int, alpha:float) -> pd.Series:
    '''Returns the ZC value of arr'''
    kdott = pd.Series(arr)
    x = kdott-MEAN(kdott, m)
    y = alpha*AVEDEV(kdott, m)
    y = y.replace(to_replace=0, method='ffill')  # get rid of 0 dividend
    return n+x/y

def GetC4(arr: pd.Series, n:int, m:int, alpha:float, divisor:float, tail:int) -> pd.Series:
    '''Returns the C4 value of arr'''
    kdott = pd.Series(arr)
    return (n+(kdott-MEAN(kdott, m))/(alpha*AVEDEV(kdott, m)))/divisor+tail

def GetCH(arr1: pd.Series, arr2: pd.Series, n:int) -> pd.Series:
    '''Returns the CH value of arr'''
    C4 = pd.Series(arr1)
    ZC = pd.Series(arr2)
    return (C4+ZC)/n

def GetW(arr: pd.Series, n:int, m:int, o:int) -> pd.Series:
    '''Returns the W value of arr'''
    closing = pd.Series(arr)
    x = closing - LLV(closing, n) 
    xx = HHV(closing, n) - LLV(closing, n)
    w = x/xx*m+o
    w = w.fillna(15)
    return w 

def GetVE(arr1: pd.Series, arr2: pd.Series, arr3: pd.Series, arr4: pd.Series, n:int, m:int) -> pd.Series:
    '''Returns the VR value of arr.'''
    opening = pd.Series(arr1)
    closing = pd.Series(arr2)
    high = pd.Series(arr3)
    low = pd.Series(arr4)
    return n/((high-low)*m-abs(closing-opening))

def GetLIURU(arr1: pd.Series, arr2: pd.Series, arr3: pd.Series, arr4: pd.Series, arr5: pd.Series, n:int) -> pd.Series:
    '''Returns the LIURU value of arr.'''
    opening = pd.Series(arr1)
    closing = pd.Series(arr2)
    high = pd.Series(arr3)
    low = pd.Series(arr4)
    ve = pd.Series(arr5)
    a = ve*(high-low)
    b = ve*((high-opening)+(closing-low))
    for idx, val in b.items():
        if(closing[idx]>=opening[idx]):
            b[idx] = n 
    for idx, val in a.items():
        if(closing[idx]<=opening[idx]):
            a[idx] = b[idx] 
    return a

def GetLIUCHU(arr1: pd.Series, arr2: pd.Series, arr3: pd.Series, arr4: pd.Series, arr5: pd.Series, n:int, m:int) -> pd.Series:
    '''Returns the LIUCHU value of arr.'''
    opening = pd.Series(arr1)
    closing = pd.Series(arr2)
    high = pd.Series(arr3)
    low = pd.Series(arr4)
    ve = pd.Series(arr5)
    a = n*ve*((high-closing)+(opening-low))
    b = n*ve*(high-low)
    for idx, val in b.items():
        if(closing[idx]>=opening[idx]):
            b[idx] = m
    for idx, val in a.items():
        if(closing[idx]<=opening[idx]):
            a[idx] = b[idx] 
    return a
    
def GetCHAE(arr1: pd.Series, arr2: pd.Series) -> pd.Series:
    '''Returns the CHAE value of arr.'''
    liuru = pd.Series(arr1)
    liuchu = pd.Series(arr2)
    return liuru+liuchu 

def GetJL(arr1: pd.Series, arr2: pd.Series, n:int, m:int, p:int) -> pd.Series:
    '''Returns the JL value of arr.'''
    chae = pd.Series(arr1)
    w = pd.Series(arr2)
    return (chae*n+w)*m+p

def GetSANHU(arr1: pd.Series, arr2: pd.Series, arr3: pd.Series, n:int, m:int, o:int) -> pd.Series:
    '''Returns the SANHU value of arr.'''
    kdott = pd.Series(arr1)
    low = pd.Series(arr2)
    high = pd.Series(arr3)
    return EMA((kdott-LLV(low,n))/(HHV(high,n)-LLV(low,n))*m, o)

def GetSL(arr: pd.Series, n:int) -> pd.Series:
    '''Returns the SL value of arr.'''
    sanhu = pd.Series(arr) 
    return sanhu.rolling(n).mean()

def GetD(arr1: pd.Series, arr2: pd.Series, arr3: pd.Series, n:float, m:int, o:int) -> pd.Series:
    '''Returns the waveband line for subgraph.'''
    # d
    f1 = pd.Series(arr1)
    d = pd.Series(n*MEAN(f1,m)-o)
    # aux index
    dong = pd.Series(arr2)
    sl = pd.Series(arr3)
    return d 

def GetRefLine(n:int, m:int, p:int, q:int, o:int) -> pd.Series:
    '''Returns the refline for subgraph.'''
    import numpy as np
    a = np.ones(o, dtype=int)*n
    b = np.ones(o, dtype=int)*m
    c = np.ones(o, dtype=int)*p
    d = np.ones(o, dtype=int)*q
    return pd.Series(a), pd.Series(b), pd.Series(c), pd.Series(d)

