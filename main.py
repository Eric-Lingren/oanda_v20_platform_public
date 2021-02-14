import os
import sys
import time
import schedule
import importlib
import subprocess
from oanda.oanda import Oanda
from setup.args import parse_args
from notifier.sms import TwilioSMS
from utils.hardware_usage import check_sys_usage

# SETS THE STRATEGIES FOLDER AVAILBLE FOR USE BY PYTHON TO PULL ALL BOT SCRIPTS IN DYNAMICALLY
sys.path.append(os.getcwd() + '/strategies/forex_bots_python')



def run_strategy():
    args = parse_args()


    # SETS UP BROKER CONFIGURATIONS:
    systemkwargs = dict(
        token = args.token,
        account = args.account,
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
        # check_sys_usage()   # For localhost testing - DigitalOcean does this natively
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
        time.sleep(1)


if __name__ == '__main__':
    run_strategy()