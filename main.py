import os
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

# SETS THE STRATEGIES FOLDER AVAILBLE FOR USE BY PYTHON TO PULL ALL BOT SCRIPTS IN DYNAMICALLY
sys.path.append(os.getcwd() + '/strategies/forex_bots_python')


def run_strategy():
    args = parse_args()

    # SETS UP BROKER CONFIGURATIONS:
    systemkwargs = dict(
        token = args.oanda_token,
        account = args.oanda_account,
        practice = not args.live,
        pair = args.pair, 
        backfill = True,
        text_notifications = args.recipient_number is not None
    )


    # SETS UP SMS NOTIFIER CONFIGURATIONS:
    twiliokwargs = dict(
        recipient_number = args.recipient_number,
        twilio_number = args.twilio_number,
        twilio_sid = args.twilio_sid,
        twilio_token = args.twilio_token
    )
    

    # PREPARES BROKER FOR USAGE:
    oanda = Oanda(**systemkwargs, **twiliokwargs)


    # IMPORTS THE TRADING STRATGEY DYNAMICALLY BASED UPON THE ROBOT FILE NAME PASSED IN THE ARGS
    bot_system = getattr(importlib.import_module(args.bot), args.bot)


    # SETS THE BOT TRADING STRATGEY TO RUN WITH OANDA:
    stratgey = bot_system(oanda)


    # PREPARES AND BUNDLES THE TRADING ACTION JOBS FOR EXECUTION (GET DATA / RUN STRATGEY): 
    def job():
        # check_sys_usage()   # For localhost hardware performance testing - DigitalOcean does this natively
        first_data_object = oanda.DataFeed.data0[0]
        oanda.DataFeed.refresh_data()
        updated_first_data_object = oanda.DataFeed.data0[0]
        if first_data_object != updated_first_data_object:
            stratgey.__next__()


    # SETS SCHEDULER TO FETCH NEW DATA AND RUN STRATGEY INTERVALS:
    schedule.every(30).seconds.do(job)


    # KEEPS THE SYSTEM ONLINE INDEFINATELY WHILE MINIMIZING RESOURCE CONSUMPTION:
    while True:
        schedule.run_pending()
        # time.sleep(1) # Remove if you want to test server overloading


# INITIALIZES ROBOT AND SCRIPTS 
try: 
    # for i in range(3):
    #     print(3/i)
    if __name__ == '__main__':
        args = parse_args()
        email_subject = f'Python Bot Stared --- {args.pair} --- {args.bot}' 
        email_body = 'System is online'
        send_email_notification(
            args.gmail_server_account, 
            args.gmail_server_password, 
            args.email_to, 
            email_subject, 
            email_body
        )
        run_strategy()

# GRACEFUL EXIT ON PROGRAM CRASH WITH EMAIL NOTIFICATION OF FAILURE REASON
except Exception as e:
    print(e)
    args = parse_args()
    log_stream = StringIO()
    logging.basicConfig(stream=log_stream, level=logging.INFO)
    logging.error("Exception occurred", exc_info=True)
    email_subject = f'Python Bot CRASHED! --- {args.pair} --- {args.bot}'
    # email_body = log_stream.getvalue()
    email_body = e
    send_email_notification(
        args.gmail_server_account, 
        args.gmail_server_password, 
        args.email_to, 
        email_subject, 
        email_body
    )