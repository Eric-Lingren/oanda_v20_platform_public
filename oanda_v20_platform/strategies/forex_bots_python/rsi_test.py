#################################################################################################################
#                                                                                                               #
#    This system DOES execute trades. This combines the price_printer and simple_order_test strategies.         #
#    This algo demonstrates how to use the backtrader platform in conjunction with the Oanda API to build a      #
#    custom trading robot that executes trades successfully based upon RSI indicator data combined with         #
#    with three bars of trending prices.                                                                        #
#                                                                                                               #
#          ********************************    WARNING!!!    ********************************                   #
#       DO NOT RUN THIS ON A LIVE ACCOUNT!  USE A DEMO ACCOUNT!  YOU WILL LOSE MONEY RUNNING THIS SYSTEM!       #
#      THIS IS FOR FUNCTIONALITY PROOF OF CONCEPT ONLY. I WILL NOT BE HELD RESPONSIBLE IF YOU LOOSE MONEY.      #
#                                                                                                               #
#################################################################################################################


from oanda.oanda import DataFeed
from indicators.indicators import Indicator
# from notifier.system_logger import config_logger
import logging


class rsi_test(DataFeed):
    
    def __init__(self, **kwargs):
        super(rsi_test, self).__init__(**kwargs)
        self.logger = logging.getLogger(__name__)
        # self.data0 = self.set_init_data0()
        self.profit_target = 5
        self.loss_target = -5
        self.set_indicators()
        self.logger.info('\n-------- RSI Test Strategy Initialized -----------')


    def set_indicators(self):
        # self.sma = Indicator().sma(self.data0, period=14, ba='bid', ohlc='c')
        self.rsi = Indicator().rsi(ohlc='close', period=14, pair=self.pair, timeframe='minute', )


    def __next__(self):
        self.set_indicators()
        self.logger.info('\n--------------- NEXT RUN ---------------')
        self.logger.info(f" BID Close Price: {self.data0[0]['bid']['c']}")
        self.logger.info(f" NEW RSI: {self.rsi[0]}")

        bid0 = self.data0[0]['bid']['c']
        bid1 = self.data0[1]['bid']['c']
        bid2 = self.data0[2]['bid']['c']

        matching_trades = self.find_matching_trades()
        # print(matching_trades)

        if len(matching_trades) == 0:  # No Existing Position. Evaluate Entry Criteria
            if self.rsi[0] <= 30:
                # print("RSI is less than 30")
                if (bid2 > bid1) and (bid1 > bid0):
                    # print('prices are trending down')
                    self.buy_market(5000, self.pair)
            if self.rsi[0] >= 70:
                # print("RSI is greater than than 70")
                if (bid2 < bid1) and (bid1 < bid0):
                    # print('prices are trending up')
                    self.sell_market(5000, self.pair)
        else:  # Position Exists.  Evaluate Exit Criteria.
            position_value = float(matching_trades[0]['unrealizedPL'])
            self.logger.info(f'Checking profit : {position_value}')
            if position_value >= self.profit_target or position_value <= self.loss_target:
                order_id = matching_trades[0]['id']
                self.close_trade(order_id)

if __name__=="__main__":
    rsi_test()