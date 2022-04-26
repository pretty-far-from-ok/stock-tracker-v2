from pytdx.params import TDXParams

class MINCONFIG:  # stock
    # 1min
    TDX_PARAMS = TDXParams.KLINE_TYPE_1MIN
    START = 0
    NUM_INFORMATIONS = 1
    NUM_INFORMATIONSv2 = 2

class minconfig:  # future 
    # 1min
    TDX_PARAMS = TDXParams.KLINE_TYPE_1MIN
    START = 0
    NUM_INFORMATIONS = 1
    NUM_INFORMATIONSv2 = 2

class DAYCONFIG:  # stock
    # 1day
    TDX_PARAMS = TDXParams.KLINE_TYPE_DAILY
    START = 0
    NUM_INFORMATIONS = 1
    NUM_INFORMATIONSv2 = 2

class dayconfig:  # future
    # 1day 
    TDX_PARAMS = TDXParams.KLINE_TYPE_DAILY
    START = 0
    NUM_INFORMATIONS = 1
    NUM_INFORMATIONSv2 = 2

