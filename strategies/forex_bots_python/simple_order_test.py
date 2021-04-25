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

import datetime
from oanda.oanda import Oanda
from indicators.indicators import Indicator

class simple_order_test(Oanda):
    def __init__(self, oanda):
        print('-------- Simple Test Strategy Initialized -----------')
        self.data0 = oanda.DataFeed.data0
        self.oanda = oanda
        self.pair = oanda.pair
        self.profit_target = 1
        self.loss_target = -1
        self.set_indicators()

    def set_indicators(self):
        self.sma1 = Indicator().sma(self.data0, period=14, ba='bid', ohlc='c')
    
    def log(self, txt, dt=None):
        dt = dt or self.data0[0]['time']
        print(f'{dt} {txt}\n')

    def __next__(self):
        self.set_indicators()
        print('\n--------------- NEXT RAN ---------------\n')
        self.log(f" BID Close Price: {self.data0[0]['bid']['c']}")

        bid0 = self.data0[0]['bid']['c']
        bid1 = self.data0[1]['bid']['c']

        open_trades = self.oanda.Account.get_open_trades()['trades']
        matching_trades = self.oanda.Account.find_matching_trades(open_trades, self.pair)

        if len(matching_trades) == 0:  # No Existing Position. Evaluate Entry Criteria
            if bid0 > bid1:  # Prices are Rising
                self.oanda.Account.Order.buy_market(5000, self.pair)
            if bid0 < bid1:  # Prices Are Falling
                self.oanda.Account.Order.sell_market(5000, self.pair)
        else:  # There is an existing position.  Evaluate Exit Criteria.
            position_value = float(matching_trades[0]['unrealizedPL'])
            if position_value >= self.profit_target or position_value <= self.loss_target:
                order_id = matching_trades[0]['id']
                self.oanda.Account.Order.close_trade(order_id)
