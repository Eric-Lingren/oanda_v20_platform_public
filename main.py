import schedule
from oanda.oanda import Oanda
from setup.args import parse_args
from strategies.price_printer import PricePrinter
from strategies.simple_order_test import SimpleOrderTest
from strategies.rsi_test import RsiTest


def run_strategy():
    print('\n***** System Initialized *****\n')
    args = parse_args()

    systemkwargs = dict(
        token = args.token,
        account = args.account,
        practice = not args.live,
        pair = args.pair, 
        backfill=True
    )
    
    oanda = Oanda(**systemkwargs)
    # stratgey = PricePrinter(oanda)
    # stratgey = SimpleOrderTest(oanda)
    stratgey = RsiTest(oanda)

    def job():
        first_data_object = oanda.DataFeed.data0[0]
        oanda.DataFeed.refresh_data()
        updated_first_data_object = oanda.DataFeed.data0[0]
        if first_data_object != updated_first_data_object:
            stratgey.__next__()

    schedule.every(10).seconds.do(job)

    while True:
        schedule.run_pending()


if __name__ == '__main__':
    run_strategy()