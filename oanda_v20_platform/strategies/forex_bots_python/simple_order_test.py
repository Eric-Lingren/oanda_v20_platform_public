#################################################################################################################
#                                                                                                               #
#   This system DOES execute trades. This is very similar to Backtraders example code documentation.            #
#   This is used to demonstrate a proof of concept of order execution within this platform. It simply          #
#   looks for 2 consecutive rising or falling bars and executes a position if there are no open positions      #
#                                                                                                               #
#          ********************************    WARNING!!!    ********************************                   #
#       DO NOT RUN THIS ON A LIVE ACCOUNT!  USE A DEMO ACCOUNT!  YOU WILL LOSE MONEY RUNNING THIS SYSTEM!       #
#      THIS IS FOR FUNCTIONALITY PROOF OF CONCEPT ONLY. I WILL NOT BE HELD RESPONSIBLE IF YOU LOOSE MONEY.      #
#                                                                                                               #
#################################################################################################################

from oanda.oanda import DataFeed
from indicators.indicators import Indicator
import logging
class simple_order_test(DataFeed):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.logger = logging.getLogger(__name__)
        self.logger.info('\n-------- Simple Test Strategy Initialized -----------')
        self.data0 = self.set_init_data0()
        self.profit_target = 1
        self.loss_target = -1
        self.set_indicators()

    def set_indicators(self):
        self.sma1 = Indicator().sma(self.data0, period=14, ba='bid', ohlc='c')
    

    def __next__(self):
        self.set_indicators()
        self.logger.info('\n--------------- NEXT RUN ---------------\n')
        self.logger.info(f" BID Close Price: {self.data0[0]['bid']['c']}")

        bid0 = self.data0[0]['bid']['c']
        bid1 = self.data0[1]['bid']['c']

        matching_trades = self.find_matching_trades()

        if len(matching_trades) == 0:  # No Existing Position. Evaluate Entry Criteria
            if bid0 > bid1:  # Prices are Rising
                self.buy_market(5000, self.pair)
            if bid0 < bid1:  # Prices Are Falling
                self.sell_market(5000, self.pair)
        else:  # There is an existing position.  Evaluate Exit Criteria.
            position_value = float(matching_trades[0]['unrealizedPL'])
            if position_value >= self.profit_target or position_value <= self.loss_target:
                order_id = matching_trades[0]['id']
                self.close_trade(order_id)
