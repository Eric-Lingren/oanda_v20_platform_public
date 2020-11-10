from oanda.oanda import Oanda
from indicators.indicators import Indicator
import datetime

class PricePrinter(Oanda):
    def __init__(self, oanda):
        self.data0 = oanda.DataFeed.data0
        print('-------- Price Printer Strategy Initialized -----------')
        self.set_indicators()

    def set_indicators(self):
        self.sma1 = Indicator().sma(self.data0, period=14, ba='bid', ohlc='c')
        self.sma2 = Indicator().sma(self.data0, period=7, ba='bid', ohlc='c')
        self.smma = Indicator().smma(self.data0, period=14, ba='bid', ohlc='c')

    
    def log(self, txt, dt=None):
        dt = dt or self.data0[0]['time']
        print(f'{dt} {txt}')

    def __next__(self):
        self.set_indicators()
        print('\n--------------------------- NEXT RAN ---------------\n')
        self.log(f" BID CLOSE: {self.data0[0]['bid']['c']}")
        self.log(f" ASK CLOSE: {self.data0[0]['ask']['c']}")
        self.log(f" SMA1: {self.sma1}")
        self.log(f" SMMA: {self.smma}")
        print('\n--------------------------- END OF NEXT --------------- \n')



