# %%
import os
import strategies
import sys
import time
import schedule
import importlib
import subprocess
from oanda.oanda import Oanda
from setup.args import parse_args
from notifier.sms import TwilioSMS
from notifier.email import send_email_notification
from utils.hardware_usage import check_sys_usage
import logging
from io import StringIO
# import account details
from auth.auth import Tokens
t = Tokens()
# %%
# SETS THE STRATEGIES FOLDER AVAILABLE FOR USE BY PYTHON TO PULL ALL BOT SCRIPTS IN DYNAMICALLY
# sys.path.append(os.getcwd() + '/strategies/forex_bots_python')

# %%
def run_strategy():
    # args = parse_args()

    # SETS UP BROKER CONFIGURATIONS:
    # TODO change back to command line inputs
    systemkwargs = dict(
        token = t.token,  # args.oanda_token,
        account = t.account, # args.oanda_account,
        practice = True, # not args.live,
        pair = 'EUR_USD', # args.pair, 
        backfill = True,
        text_notifications = False, # args.recipient_number is not None
    )


    # SETS UP SMS NOTIFIER CONFIGURATIONS:
    twiliokwargs = dict(
        recipient_number = None, # args.recipient_number,
        twilio_number = None, # args.twilio_number,
        twilio_sid = None, # args.twilio_sid,
        twilio_token = None, # args.twilio_token
    )
    

    # PREPARES BROKER FOR USAGE:
    oanda = Oanda(**systemkwargs, **twiliokwargs)


    # IMPORTS THE TRADING STRATEGY DYNAMICALLY BASED UPON THE ROBOT FILE NAME PASSED IN THE ARGS
    # bot_system = getattr(importlib.import_module(args.bot), args.bot)
    # from strategies.forex_bots_python import price_printer
    from strategies.forex_bots_python import rsi_test
    # from strategies.forex_bots_python import simple_order_test

    # SETS THE BOT TRADING STRATEGY TO RUN WITH OANDA:
    # strategy = price_printer.price_printer(oanda)
    strategy = rsi_test.rsi_test(oanda)
    # strategy = simple_order_test.simple_order_test(oanda)



    # PREPARES AND BUNDLES THE TRADING ACTION JOBS FOR EXECUTION (GET DATA / RUN STRATGEY): 
    def job():
        # check_sys_usage()   # For localhost hardware performance testing - DigitalOcean does this natively
        first_data_object = oanda.DataFeed.data0[0]
        oanda.DataFeed.refresh_data()
        updated_first_data_object = oanda.DataFeed.data0[0]
        if first_data_object != updated_first_data_object:
            strategy.__next__()


    # SETS SCHEDULER TO FETCH NEW DATA AND RUN STRATEGY INTERVALS:
    schedule.every(30).seconds.do(job)


    # KEEPS THE SYSTEM ONLINE INDEFINITELY WHILE MINIMIZING RESOURCE CONSUMPTION:
    while True:
        schedule.run_pending()
        time.sleep(1) # Comment this line out if you want to test server overloading and torture testing

# %%
# INITIALIZES ROBOT AND SCRIPTS  
if __name__ == '__main__':
    try:
        # args = parse_args()
        # if args.email_to:
        #     email_subject = f'Python Bot Stared --- {args.pair} --- {args.bot}' 
        #     email_body = 'System is online'
        #     send_email_notification(
        #         args.gmail_server_account, 
        #         args.gmail_server_password, 
        #         args.email_to, 
        #         email_subject, 
        #         email_body
        #     )

        run_strategy()

# GRACEFUL EXIT ON PROGRAM CRASH WITH EMAIL NOTIFICATION OF FAILURE REASON
    except Exception as e:
        print(e)
    # if args.email_to:
    #     args = parse_args()
        log_stream = StringIO()
        logging.basicConfig(stream=log_stream, level=logging.INFO)
        logging.error("Exception occurred", exc_info=True)
    #     email_subject = f'Python Bot CRASHED! --- {args.pair} --- {args.bot}'
    #     # email_body = log_stream.getvalue()
    #     email_body = e
    #     send_email_notification(
    #         args.gmail_server_account, 
    #         args.gmail_server_password, 
    #         args.email_to, 
    #         email_subject, 
    #         email_body
    #     )
# %%
