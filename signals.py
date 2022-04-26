def k_under_downbollinger(data):
    pass

def upwards(data):
    if(data.iloc[0].close < data.iloc[-1].close):
        return True
    else:
        return False
    
