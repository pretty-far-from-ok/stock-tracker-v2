from query import datarequestv2
from signals import k_under_downbollinger, upwards


def signalAnalyze(switch, marketcode, stockcode, siglst, _):
    data = datarequestv2(switch, marketcode, stockcode, siglst, _)  # derive >=1 df each stock 
    # check return none data ->
    if(data is None):
        siglst[_] = "xxx"
    else:
        # check indicator
        if(upwards(data)):
            siglst[_] = "up"
        else:
            siglst[_] = "down"

