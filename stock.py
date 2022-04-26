class Stock(object):
    def __init__(self, switch, market, ticker, prev, rawInfo=None):  # str str str str
        # if creating stocks via the initialization file, only assign ticker/market/switch/prev
        if rawInfo is None:
            self.__ticker = ticker
            self.__market = market 
            self.__switch = switch 
            self.__prev = prev
            self.__signal = "-"
            return

        # store all the finalized versions of the attributes (rounded #'s too)
        self.__ticker = ticker
        self.__market = market
        self.__switch = switch 
        self.__prev = prev
        self.__name = rawInfo[0]
        self.__open = rawInfo[1]
        self.__high = rawInfo[2]
        self.__low = rawInfo[3]
        self.__close = rawInfo[4]
        self.__volume = rawInfo[5]
        self.__changeNum = str(float(self.__close) - float(self.__prev))
        self.__signal = "-"
        # figure out the status (gain/loss/neutral)
        if float(self.__changeNum) > 0:
            self.__changeNum = '+' + self.__changeNum
            self.__status = "gain"
        elif float(self.__changeNum) < 0:
            self.__status = "loss"
        else:
            self.__status = "neutral"

        self.__status1 = self.__status

    # for convenient printing/debugging
    def __str__(self):
        ret = "Switch: " + self.__switch + " | Market: " + self.__market + " | Name: " + self.__name + " | Ticker: " + self.__ticker + " | Price: " \
            + self.__open + " | ∆: " + self.__changeNum + " | Status: " + self.__status + " | Signal: " + self.__signal
        return ret

    # for constructing the string displayed in the portfolio: (display str, display status)
    def stringify(self):
        # ('code open high low close volume', 'gain/loss/neutral')
        display = self.__ticker.ljust(9) + self.__open.ljust(10) + self.__high.ljust(10) + self.__low.ljust(10) + \
            self.__close.ljust(10) + self.__volume.ljust(9)
        ret = (display, self.__status)		
        return ret

    # for constructing the string displayed in the portfolio1: (display str, display status)
    def stringify1(self):
        # ('signal', 'gain/loss/neutral')
        display = self.__signal.ljust(9) 
        ret = (display, self.__status1)
        return ret

    # used to update all the stock attributes during a refresh, operates the same as the constructor/init method
    def update(self, rawInfo):
        # update all the values again
        self.__name = rawInfo[0]
        self.__open = rawInfo[1]
        self.__high = rawInfo[2]
        self.__low = rawInfo[3]
        self.__close = rawInfo[4]
        self.__volume = rawInfo[5]
        # compute changes
        self.__changeNum = str(float(self.__close) - float(self.__prev))
        # update prev
        self.__prev = rawInfo[6]

        # figure out the status (gain/loss/neutral)
        if float(self.__changeNum) > 0:
            self.__changeNum = '+' + self.__changeNum
            self.__status = "gain"
        elif float(self.__changeNum) < 0:
            self.__status = "loss"
        else:
            self.__status = "neutral"
   
    # update signal by a separate threading pipeline (data-request for a bulk of data, then do some analysis)
    def updateSignal(self, sig):
        self.__signal = sig
        # figure out the status (gain/loss/neutral) according to the signal -> todo
        if float(self.__changeNum) > 0:
            self.__changeNum = '+' + self.__changeNum
            self.__status1 = "gain"
        elif float(self.__changeNum) < 0:
            self.__status1 = "loss"
        else:
            self.__status1 = "neutral"

    # getters
    def getTicker(self):
        return self.__ticker
    def getMarket(self):
        return self.__market
    def getSwitch(self):
        return self.__switch
    def getPrev(self):
        return self.__prev
    def getName(self):
        return self.__name	
    def getPrice(self):
        return self.__open
    def getChangeNum(self):
        return self.__changeNum	
    def getSignal(self):
        return self.__signal

    # setters
    def setTicker(self, ticker):
        self.__ticker = ticker
    def setMarket(self, market):
        self.__market = market 
    def setSwitch(self, switch):
        self.__switch = switch 
    def setPrev(self, prev):
        self.__prev = prev 
    def setName(self, name):
        self.__name = name
    def setPrice(self, price):
        self.__open = price
    def setChangeNum(self, changeNum):
        self.__changeNum = changeNum
    def setSignal(self, sig):
        self.__signal = sig 


if __name__ == '__main__':
    main()

