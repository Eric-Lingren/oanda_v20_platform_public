########## set up logging ###########################
import logging
from datetime import datetime
from oanda_v20_platform.data.marketdata import MarketData
import os
from utils.fileops import get_abs_path

from decouple import Config
# get todays date
datestamp = datetime.now().strftime('%Y%m%d')

# append date to logfile name
log_name = f'log-{datestamp}.txt'
# path = './logs/'
log_filename = get_abs_path(['oanda_v20_platform', 'logs', log_name])
print(log_filename)
# create log if it does not exist
# if not log_filename.exists():
log_filename.touch(exist_ok=True)


# create logger
logger = logging.getLogger()
# set minimum output level
logger.setLevel(logging.DEBUG)
# Set up the file handler
file_logger = logging.FileHandler(log_filename)
# create console handler and set level to debug
ch = logging.StreamHandler()
# set minimum output level
ch.setLevel(logging.INFO)
# create formatter
formatter = logging.Formatter('[%(levelname)s] - %(asctime)s - %(name)s : %(message)s')
# add formatter
file_logger.setFormatter(formatter)
ch.setFormatter(formatter)
# add a handler to logger
logger.addHandler(file_logger)
logger.addHandler(ch)
# mark the run
logger.info('Oanda_v20_platform Started')

####################################################################################

try:
    # import python modules and packages
    import sys
    import time
    import schedule
    import importlib
    import subprocess
    from io import StringIO
    from decouple import config
except:
    logger.exception('Failed to import python modules, is the environment correctly setup?')

try:
    # import local modules
    from config.args import parse_args
    from notifier.sms import TwilioSMS
    from notifier.email import send_email_notification
    from utils.hardware_usage import check_memory_usage, check_cpu_usage
    from data.marketdata import MarketData
except:
    logger.exception('Failed to import local modules, have the paths been changed?')

try:
    # import config ini 
    import configparser
    config_local = configparser.ConfigParser()
    config_local.read(get_abs_path(['oanda_v20_platform', 'config', 'config.ini']))
except:
    logger.exception('Failed to import config file, has it been moved or edited?')



def run_strategy():
    args = parse_args()

    # SETS UP BROKER CONFIGURATIONS:
    systemkwargs = dict(
        token              = config('PRACTICE_TOKEN'), 
        account            = config('PRACTICE_ACCOUNT'),
        practice           = config_local.getboolean('Account', 'practice', fallback=False), 
        pair               = args.pair, 
        backfill           = config_local.getboolean('Trading', 'backfill', fallback=True),
        text_notifications = config_local.getboolean('Twilio', 
                            'text_notifications', fallback=False), 
        recipient_number   = config_local.getint('Twilio', 'recipient_number', fallback=None),
        twilio_number      = config_local.getint('Twilio', 
                            'twilio_number', fallback=None),
        twilio_sid         = config_local.get('Twilio', 
                             'twilio_sid', fallback=None),
        twilio_token       = config_local.get('Twilio', 
                             'twilio_token', fallback=None),
                        )

    # IMPORTS THE TRADING STRATEGY DYNAMICALLY BASED UPON THE ROBOT FILE NAME PASSED IN THE ARGS
    try:
        bot_system = getattr(importlib.import_module('strategies'), args.bot)
    except:
        logger.exception('Failed to load bot, check its name is correct')

    # SETS THE BOT TRADING STRATEGY TO RUN WITH OANDA:
    strategy = bot_system(**systemkwargs)

    # PREPARES AND BUNDLES THE TRADING ACTION JOBS FOR EXECUTION (GET DATA / RUN STRATEGY):
    def job():
        # For localhost hardware performance testing - DigitalOcean does this natively
        check_cpu_usage() 
        check_memory_usage()
        first_data_object = strategy.data0[0]
        strategy.refresh_data()
        updated_first_data_object = strategy.data0[0]
        if first_data_object != updated_first_data_object:
            strategy.__next__()


    # SETS SCHEDULER TO FETCH NEW DATA AND RUN STRATEGY INTERVALS:
    schedule.every(30).seconds.do(job)


    # KEEPS THE SYSTEM ONLINE INDEFINITELY WHILE MINIMIZING RESOURCE CONSUMPTION:
    while True:
        schedule.run_pending()
        # Comment this line out if you want to test server overloading and torture testing
        time.sleep(1) 
        

# INITIALIZES ROBOT AND SCRIPTS  
if __name__ == '__main__':
    
    #################################################################################
    # update market data 
    try:
        md = MarketData()
    except:
        logger.exception("Failed to update market data")


    try:
        args = parse_args()
        if config.get('Email', 'email_to', fallback=None):
            email_subject = f'Python Bot Stared --- {args.pair} --- {args.bot}' 
            email_body = 'System is online'
            send_email_notification(
                config.get('Email','gmail_server_account', fallback=None),
                config.get('Email','gmail_server_password', fallback=None),
                config.get('Email', 'email_to', fallback=None), 
                email_subject, 
                email_body
            )

        run_strategy()
        

# GRACEFUL EXIT ON PROGRAM CRASH WITH EMAIL NOTIFICATION OF FAILURE REASON
    except:
        logger.exception('Failed to run strategy')

    if config.get('Email', 'email_to', fallback=None):
        args = parse_args()
        log_stream = StringIO()
        email_subject = f'Python Bot STOPPED! --- {args.pair} --- {args.bot}'
        email_body = log_stream.getvalue()
        send_email_notification(
            config.get('Email','gmail_server_account', fallback=None),
            config.get('Email','gmail_server_password', fallback=None),
            config.get('Email', 'email_to', fallback=None),  
            email_subject, 
            email_body
        )
    logger.info('Strategy Run finished')
