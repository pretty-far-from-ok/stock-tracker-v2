# from pytdx.params import TDXParams

# ------------------ tdx params --------------------
# TDX_PARAMS.KLINE_TYPE_5MIN = 0
# TDX_PARAMS.KLINE_TYPE_15MIN = 1
# TDX_PARAMS.KLINE_TYPE_30MIN = 2
# TDX_PARAMS.KLINE_TYPE_1HOUR = 3
# TDX_PARAMS.KLINE_TYPE_DAILY = 4
# TDX_PARAMS.KLINE_TYPE_WEEKLY = 5
# TDX_PARAMS.KLINE_TYPE_MONTHLY = 6
# TDX_PARAMS.KLINE_TYPE_EXHQ_1MIN = 7
# TDX_PARAMS.KLINE_TYPE_1MIN = 8
# TDX_PARAMS.KLINE_TYPE_RI_K = 9
# TDX_PARAMS.KLINE_TYPE_3MONTH = 10
# TDX_PARAMS.KLINE_TYPE_YEARLY = 11

# ----------------- market code ---------------------
#     market    category      name         short_name
#          0                深圳指数       SZ
#          1                上证指数       SH
# 0        1         1       临时股        TP
# 1        4        12    郑州商品期权     OZ
# 2        5        12    大连商品期权     OD
# 3        6        12    上海商品期权     OS
# 4        8        12    上海个股期权     QQ
# 5       27         5      香港指数       FH
# 6       28         3      郑州商品       QZ
# 7       29         3      大连商品       QD
# 8       30         3      上海期货       QS
# 9       31         2      香港主板       KH
# 10      32         2      香港权证       KR
# 11      33         8     开放式基金      FU
# 12      34         9     货币型基金      FB
# 13      35         8    招商理财产品     LC
# 14      36         9    招商货币产品     LB
# 15      37        11      国际指数       FW
# 16      38        10    国内宏观指标     HG
# 17      40        11     中国概念股      CH
# 18      41        11    美股知名公司     MG
# 19      43         1     B股转H股        HB
# 20      44         1      股份转让       SB
# 21      47         3      股指期货       CZ
# 22      48         2     香港创业板      KG
# 23      49         2    香港信托基金     KT
# 24      54         6     国债预发行      GY
# 25      60         3    主力期货合约     MA
# 26      62         5      中证指数       ZZ
# 27      71         2       港股通        GH

# ------------------ request limitation ------------------------
# ref : https://github.com/rainx/pytdx/issues/7
# MAX_TRANSACTION_COUNT = 2000
# MAX_KLINE_COUNT = 800

# 板块相关参数
# BLOCK_SZ = "block_zs.dat"
# BLOCK_FG = "block_fg.dat"
# BLOCK_GN = "block_gn.dat"
# BLOCK_DEFAULT = "block.dat"

from pytdx.params import TDXParams


class CONFIG(object):  # future 
    def __init__(self, sw, tdx, m_c, s_c, st, num):
        self.switch = sw
        self.TDX_PARAMS = tdx  # 
        self.MARKET_CODE = m_c  # use api.to_df(api.get_markets()) to return market list of certain server
        self.STOCK_CODE = s_c 
        self.START = st 
        self.NUM_INFORMATIONS = num

# ------------------ tdx params --------------------
# TDX_PARAMS.KLINE_TYPE_5MIN = 0
# TDX_PARAMS.KLINE_TYPE_15MIN = 1
# TDX_PARAMS.KLINE_TYPE_30MIN = 2
# TDX_PARAMS.KLINE_TYPE_1HOUR = 3
# TDX_PARAMS.KLINE_TYPE_DAILY = 4
# TDX_PARAMS.KLINE_TYPE_WEEKLY = 5
# TDX_PARAMS.KLINE_TYPE_MONTHLY = 6
# TDX_PARAMS.KLINE_TYPE_EXHQ_1MIN = 7
# TDX_PARAMS.KLINE_TYPE_1MIN = 8
# TDX_PARAMS.KLINE_TYPE_RI_K = 9
# TDX_PARAMS.KLINE_TYPE_3MONTH = 10
# TDX_PARAMS.KLINE_TYPE_YEARLY = 11

# ----------------- market code ---------------------
#     market    category      name         short_name
#          0                深圳指数       SZ
#          1                上证指数       SH
# 0        1         1       临时股        TP
# 1        4        12    郑州商品期权     OZ
# 2        5        12    大连商品期权     OD
# 3        6        12    上海商品期权     OS
# 4        8        12    上海个股期权     QQ
# 5       27         5      香港指数       FH
# 6       28         3      郑州商品       QZ
# 7       29         3      大连商品       QD
# 8       30         3      上海期货       QS
# 9       31         2      香港主板       KH
# 10      32         2      香港权证       KR
# 11      33         8     开放式基金      FU
# 12      34         9     货币型基金      FB
# 13      35         8    招商理财产品     LC
# 14      36         9    招商货币产品     LB
# 15      37        11      国际指数       FW
# 16      38        10    国内宏观指标     HG
# 17      40        11     中国概念股      CH
# 18      41        11    美股知名公司     MG
# 19      43         1     B股转H股        HB
# 20      44         1      股份转让       SB
# 21      47         3      股指期货       CZ
# 22      48         2     香港创业板      KG
# 23      49         2    香港信托基金     KT
# 24      54         6     国债预发行      GY
# 25      60         3    主力期货合约     MA
# 26      62         5      中证指数       ZZ
# 27      71         2       港股通        GH

# ------------------ request limitation ------------------------
# ref : https://github.com/rainx/pytdx/issues/7
# MAX_TRANSACTION_COUNT = 2000
# MAX_KLINE_COUNT = 800

# 板块相关参数
# BLOCK_SZ = "block_zs.dat"
# BLOCK_FG = "block_fg.dat"
# BLOCK_GN = "block_gn.dat"
# BLOCK_DEFAULT = "block.dat"

