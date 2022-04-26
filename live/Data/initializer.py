import pandas as pd
import numpy as np
import os

from collections import OrderedDict
from indicator import *


# init
# def initializer(initdata, initdata5, start, end):  # for multi period data on one graph
def initializer(initdata, start, end):
    # interested: open high low close volume datetime
    # stock: open close high low volume amount year month day hour minute datetime  
    # future: open close high low position volume price year month day hour minute datetime amount
    # --- basics --- 
    data = initdata
    data = data[start:end]
    opening = data.open  # idx=date
    closing = data.close  # idx=date
    high = data.high  # idx=date
    low = data.low  # idx=date
    volume = data.volume  # idx=date
    # volume
    mdot = (high+low+closing)/3  # 1min v5 ohlc idx=date 
    sdot = (high+low+3*closing)/5  # 1min v5 subgraph idx=date

    # --- main graph ---
    # 1min
    sma18 = SMA(mdot, 18)  # (18)
    std21 = STD(mdot, 21)  # (21)
    sma13 = SMA(mdot, 13)  # (13)
    std13 = STD(mdot, 13)  # (13)
    ema3 = EMA(mdot, 3)  # (0)
    ema33 = EMA(ema3, 3)  # (0)
    ema337 = EMA(ema33, 7)  # (0)
    mean4 = MEAN(mdot, 4)  # (4)
    mean8 = MEAN(mdot, 8)  # (8)

    # bolling(21) 
    upbolling = UpBolling(sma18, std21)  # series(2148,) index=datetime
    # midbolling(>=3)
    midbolling2 = split_decreasing(ema337)
    underlay_midbolling = ema337
    # downbolling(13)
    downbolling = DownBolling(sma13, std13)  # series(2148,) index=datetime
    # waveband(8)
    waveband0 = 3*mean4-2*mean8
    waveband2 = split_decreasing(waveband0)
    underlay_waveband0 = waveband0
    # oversold sign(=downbolling=13)
    # oversold = OverSoldSign(downbolling, low, high, waveband0)  # series(2148,) index=datetime

    # --- sub graph ---
    slope = GetSlope(sdot, 18)
    m = GetM(slope, sdot, 20, 49)
    sp = GetSP(closing, low, high, 5, 100)
    qui = GetQIU(sp, 3)
    dong = GetDONG(qui, 2)
    f1 = GetF1(qui, dong, 3, 2)  # series(2148,) index=datetime
    # shallow blue(4)
    avedev = AVEDEV(sdot, 3)
    zc = GetZC(sdot, 50, 3, 0.03)  # nan
    c4 = GetC4(sdot, 50, 4, 0.03, 1.18, 8)  # nonan
    ch = GetCH(c4, zc, 2)  # series(2148,) index=datetime  # nan
    # deep blue(2)
    w = GetW(closing, 2, 65, 15)
    ve = GetVE(opening, closing, high, low, 1, 2)
    liuru = GetLIURU(opening, closing, high, low, ve, -1/2)
    liuchu = GetLIUCHU(opening, closing, high, low, ve, -1, -1/2)
    chae = GetCHAE(liuru, liuchu)
    jl = GetJL(chae, w, 40, 0.8, 12)  # series(2148,) index=datetime
    # refline grey(0)
    ref0, ref20, ref80, ref100 = GetRefLine(0, 20, 80, 100, sdot.size)  # tuple(ref0, ref20, ref80, ref100) series(2148,) index=numeric
    ref0.index, ref20.index, ref80.index, ref100.index = sdot.index, sdot.index, sdot.index, sdot.index  # convert index = datetime
    # D line: waveband subgraph(>=12)
    sanhu = GetSANHU(sdot, low, high, 5, 100, 4)
    sl = GetSL(sanhu, 2)
    d = GetD(f1, dong, sl, 1.3, 5, 15)
    d_down = split_decreasing(d)
    underlay_subgraphwaveband = d
    subgraphwaveband2 = d_down

    # -------------------------------------------------------------
    # ----------------DATA AJUSTMENT-------------------------------
    # -------------------------------------------------------------

    # --- data concerned keys ---
    # open high low close amount datetime
    ohlc_keys = ['open', 'high', 'low', 'close', 'volume', 'date']
    data = data[ohlc_keys].copy(deep=False)

    # --- datetime index conversion for stock ---
    source = data
    # source_inc = (closing >= opening).values.astype(np.uint8).astype(str)  # np.arr(2148,) index=None

    # --- ohlc extreme value (for plot ajustment) ---
    # ohlc_extreme_values = data[['high', 'low']].copy(deep=False)  #  pd [numeric_index, high, low]
    # ohlc_extreme_values['upbolling'] = np.array(upbolling)
    # ohlc_extreme_values['downbolling'] = np.array(downbolling)
    # ohlc_extreme_values['waveband0'] = np.array(waveband0)
    # ohlc_extreme_values['oversold'] = np.array(oversold)
    # source_ohlc_extreme_min, source_ohlc_extreme_max = ohlc_extreme_values.min(1), ohlc_extreme_values.max(1)  # series(2148,) numeric index

    # -------------------------------------------------------------
    # --------------CONFIG COMPONENT FOR DATA DICT-----------------
    # -------------------------------------------------------------

    # --- config component for source dict ---
    source_component = source  # df(2148,6) index=numeric
    # source_inc_component = source_inc  # np.arr(2148,) index=None
    # main graph
    source_upbolling_component = upbolling  # series(2148,) index=datetime
    source_midbolling2_component = midbolling2 # lst (2148,)
    source_underlay_midbolling_component = underlay_midbolling  # lst (2148,)
    source_downbolling_component = downbolling  # series(2148,) index=datetime
    source_waveband_down_component = waveband2  # list(2148,) index=numeric
    source_underlay_waveband_component = underlay_waveband0
    # source_oversold_component = oversold  # series(2148,) index=datetime
    # sub graph
    source_ch_component = ch  # series(2148,) index=datetime
    source_jl_component = jl  # series(2148,) index=datetime
    source_ref_0_component = ref0  # series(2148,) index=datetime
    source_ref_20_component = ref20  # series(2148,) index=datetime
    source_ref_80_component = ref80  # series(2148,) index=datetime
    source_ref_100_component = ref100  # series(2148,) index=datetime
    source_d_underlay_component = underlay_subgraphwaveband
    source_d_down_component =  subgraphwaveband2 
    # ohlc extreme
    # source_ohlc_extreme_min_component = source_ohlc_extreme_min  # series(2148,) numeric index
    # source_ohlc_extreme_max_component = source_ohlc_extreme_max  # series(2148,) numeric index

    # -------------------------------------------------------------
    # --------------CONFIG COMPONENT FOR DATA DICT-----------------
    # -------------------------------------------------------------

    # --- config data list: sc:source_component ---
    # base info
    sc_index_lst = source_component.index.to_list()
    sc_open_lst = source_component['open'].to_list()
    sc_close_lst = source_component['close'].to_list()
    sc_high_lst = source_component['high'].to_list()
    sc_low_lst = source_component['low'].to_list()
    sc_volume_lst = source_component['volume'].to_list()
    sc_datetime_lst = source_component['date'].to_list()
    # maingraph indicator
    # sc_inc_lst = source_inc_component.tolist()
    sc_upbolling_lst = source_upbolling_component.to_list()
    sc_midbolling2_lst = source_midbolling2_component  # lst (2148,)
    sc_underlay_midbolling_lst = source_underlay_midbolling_component  # lst (2148,)
    sc_downbolling_lst = source_downbolling_component.to_list()
    sc_waveband_down_lst = source_waveband_down_component
    sc_underlay_waveband_lst = source_underlay_waveband_component
    # sc_oversold_lst = source_oversold_component.to_list()
    # subgraph indicator
    sc_ch_lst = source_ch_component.to_list()  # 16_1
    sc_jl_lst = source_jl_component.to_list()  # 16_2
    sc_ref_0_lst = source_ref_0_component.to_list()  # 16_3
    sc_ref_20_lst = source_ref_20_component.to_list()  # 16_4
    sc_ref_80_lst = source_ref_80_component.to_list()  # 16_5
    sc_ref_100_lst = source_ref_100_component.to_list()  # 16_6
    sc_d_underlay_lst = source_d_underlay_component
    sc_d_down_lst = source_d_down_component
    # ohlc scale factor for scale js
    # sc_ohlc_low_lst = source_ohlc_extreme_min_component.to_list()
    # sc_ohlc_high_lst = source_ohlc_extreme_max_component.to_list()

    # -------------------------------------------------------------
    # ------------------------CONFIG DICT--------------------------
    # -------------------------------------------------------------

    # --- config source dict ---
    source_dict = {}
    # base info
    # 0   ['date\topen\thigh\tlow\tclose\tvolume\tsplit\tdividend\tabsoluteChange\tpercentChange']  
    source_dict['date'] = sc_datetime_lst
    source_dict['open'] = sc_open_lst
    source_dict['high'] = sc_high_lst
    source_dict['low'] = sc_low_lst
    source_dict['close'] = sc_close_lst
    source_dict['volume'] = sc_volume_lst
    # maingraph indicator
    # source_dict['inc'] = sc_inc_lst
    source_dict['upbolling'] = sc_upbolling_lst
    source_dict['midbolling2'] = sc_midbolling2_lst 
    source_dict['underlay_midbolling'] = sc_underlay_midbolling_lst
    source_dict['downbolling'] = sc_downbolling_lst 
    source_dict['waveband2'] = sc_waveband_down_lst 
    source_dict['underlay_waveband'] = sc_underlay_waveband_lst
    # source_dict['oversold'] = sc_oversold_lst 
    # subgraph indicator
    source_dict['ch'] = sc_ch_lst  # 16_1
    source_dict['jl'] = sc_jl_lst  # 16_2
    source_dict['ref_0'] = sc_ref_0_lst  # 16_3
    source_dict['ref_20'] = sc_ref_20_lst  # 16_4
    source_dict['ref_80'] = sc_ref_80_lst   # 16_5
    source_dict['ref_100'] = sc_ref_100_lst   # 16_6
    source_dict['d_underlay'] = sc_d_underlay_lst  # 16_7
    source_dict['d_down'] = sc_d_down_lst  # 16_8
    # ohlc scale factor for scale js
    # source_dict['ohlc_low'] = sc_ohlc_low_lst 
    # source_dict['ohlc_high'] = sc_ohlc_high_lst 

    return source_dict

