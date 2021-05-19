#################################################################################################################
#                                                                                                               #
#    This system does not execute trades.  It is a very simple barebones algo that plugs into the Oanda API     #
#   and uses that data to print the current prices of the selected asset and adds some additional indicators    #
#     Use this for the most rudimentary baseline of how the bots function within the backtrader ecosystem.      #
#                                                                                                               #
#################################################################################################################

from oanda.oanda import DataFeed
from indicators.indicators import Indicator
import logging
class price_printer(DataFeed):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.logger = logging.getLogger(__name__)
        # self.data0 = self.set_init_data0()
        self.set_indicators()
        self.logger.info('\n-------- Price Printer Strategy Initialized -----------')


    def set_indicators(self):
        self.sma1 = Indicator().sma(self.data0, period=14, ba='bid', ohlc='c')
        self.sma2 = Indicator().sma(self.data0, period=7, ba='bid', ohlc='c')
        self.rsi = Indicator().rsi(ohlc='close', period=14, pair=self.pair, timeframe='minute', )


    def __next__(self):
        self.set_indicators()
        print('\n--------------------------- NEXT RUN ---------------\n')
        self.logger.info(f" BID CLOSE: {self.data0[0]['bid']['c']}")
        self.logger.info(f" ASK CLOSE: {self.data0[0]['ask']['c']}")
        self.logger.info(f" SMA1: {self.sma1}")
        self.logger.info(f" RSI: {self.rsi}")
        print('\n--------------------------- END OF NEXT --------------- \n')



