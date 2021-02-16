#################################################################################################################
#                                                                                                               #
#    This system does not execute trades.  It is a very simple barebones algo that plugs into the Oanda API     #
#   and uses that data to print the current prices of the selected asset and adds some additional indicators    #
#     Use this for the most rudamentary baseline of how the bots function within the backtrader ecosystem.      #
#                                                                                                               #
#################################################################################################################

import datetime
from oanda.oanda import Oanda
from indicators.indicators import Indicator

class price_printer(Oanda):
    def __init__(self, oanda):
        self.data0 = oanda.DataFeed.data0
        self.pair = oanda.pair
        print('-------- Price Printer Strategy Initialized -----------')
        self.set_indicators()


    def set_indicators(self):
        self.sma1 = Indicator().sma(self.data0, period=14, ba='bid', ohlc='c')
        self.sma2 = Indicator().sma(self.data0, period=7, ba='bid', ohlc='c')
        self.rsi = Indicator().rsi(ohlc='close', period=14, pair=self.pair, timeframe='minute', )


    def log(self, txt, dt=None):
        dt = dt or self.data0[0]['time']
        print(f'{dt} {txt}')


    def __next__(self):
        self.set_indicators()
        print('\n--------------------------- NEXT RAN ---------------\n')
        self.log(f" BID CLOSE: {self.data0[0]['bid']['c']}")
        self.log(f" ASK CLOSE: {self.data0[0]['ask']['c']}")
        self.log(f" SMA1: {self.sma1}")
        self.log(f" RSI: {self.rsi}")
        print('\n--------------------------- END OF NEXT --------------- \n')



