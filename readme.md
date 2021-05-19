[![Build Status](https://travis-ci.com/ant358/oanda_v20_platform_public.svg?branch=master)](https://travis-ci.com/ant358/oanda_v20_platform_public)
[![codecov](https://codecov.io/gh/ant358/oanda_v20_platform_public/branch/master/graph/badge.svg)](https://codecov.io/gh/ant358/oanda_v20_platform_public)
# Automated Trading Platform that runs on Oanda  

## Changes on fork ahead of the upstream remote  

* added the marketdata.py module and database to collect and store market data for use developing and running trading strategies.  
  
    DB Browser https://sqlitebrowser.org/ can be used for easy viewing and querying of the database.  Focused on daily data it incudes a table for every tradable instrument with:
    * The Last 60 days of data
    * Yesterdays Volume, Open, High, Low, and Close
    * The 55 day Vol, O, H, L, C
    * The 20 day Vol, O, H, L, C
    * The 10 day Vol, O, H, L, C
    * True Range for each day - a volatility measure that captures gaps
    * N the 20 day average True Range - like ATR(20)

    And a summary table of market data (called marketdata) useful for trading effectively, 
    It includes the following information:
    * Trading costs such as financing rates and the days they are applied.
    * Pip positions (decimal points) for each instrument 
    * Margin rates
    * Max and Min Trailing stop distances
    * Maximum order sizes
    * The average spread
    * The volatility (as N)
    * The spread percentage of N - enabling the selection of a trading range where trade costs are minimised.  
    * The N per 100X spread provides a quick way to get the target trading range where the spread cost will be ~1% 
    * The asset class and base currency

* reduced the command line args so now only --bot and --pair are needed    
  ```python main.py --bot "rsi_test" --pair "EUR_USD"```
* stored account number and token as environment variables in a file called oanda_v20_platform_public/.env (ignored via .gitignore)
```
PRACTICE_ACCOUNT=XXX-XXX-XXXXXXXX-XXX
PRACTICE_TOKEN=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx  
```
Then used:
```pip install python-decouple```
```from decouple import config```
```token = config('PRACTICE_TOKEN)```

* added config.ini file to hold standard args  
* changed the name of setup folder to config so it does not clash with setup.py file
* changed the class inheritance so the kwargs can be passed straight to the bot instance  
* changed the class inheritance so subclasses are no longer called in the parent class
* added import statements to the the strategies ```__init__.py``` to make bot import simpler  
* changed the logging to update a file and report to the console with different levels of information  
  and removed the logging function and added the setup logging script to the start of main.py  
  so its the first code to run   
* added a datestamp to the log filenames   
* added requirements.txt for local environment setup  
* directory structure changed for pytest setup
* added some tests
* added Travis CI and Codecov for build monitoring  
* added setup.py and an .egg file starting to work towards easy deployment as a package    


# Oanda v20 Platform - Public Version - Readme from upstream remote

This is a fully custom forex robot algorithm library built using the python Backtrader framework as reference, with full integration into the Oanda version 20 API schema. I built this platform after dissatisfactory results with other Python/Oanda platforms I was able to find on the market.  Due to this fact, it does not natively support all Oanda API calls you may need for your use case, but it is easily scalable to suit your individual needs.

## General Information:   

This contains sample robots which will evaluate prices, indicators, and execute orders.   

This can be run with a live or demo Oanda account based upon the arguments you pass into the initialization script.   

This is intended to run in a live environment in real time.  If you would like to view my backtesting version optimized to work with historically loaded data in hd5, excel, or pandas data frames with a full Backtrader integration [you can view the repo for that project here. ](https://github.com/Eric-Lingren/bt_oanda)    

You can run this locally or on a deployed linux server.  If you wish to use my server deployment library that works in conjunction with this Oanda platform, [you can view that repo here.](https://github.com/Eric-Lingren/oanda_server_scripts)    

As part of the functionality and high availability intended for trading ecosystems, this platform includes automated email notifications auto sent for each up and down occurrence of the platform.  If you wish to enable this, you will need pass those arguments into your startup script.  This also means you will need to configure a gmail account to use an application password to use for the email sending options if you keep those enabled. There are optional Twilio SMS notifications you can configure as well.

If you would like more information about the Oanda API architecture used within this repo or have more questions on obtaining your Oanda tokens and credentials, you can view the full Oanda v20 developer documentation [here](https://developer.oanda.com/rest-live-v20/introduction/)

## Usage:

To run the platform in terminal on localhost you can start it up with the following script from the root of the project making sure you substitute varibles for your own:   

```python3 main.py --oanda_account <account-number> --oanda_token <oanda-api-token> --pair <currency-pair> --bot <bot-name>```   

The arguments listed above are all required for operation but there are optional ones available also for email and sms notifications.  To view the full list of all arguments the python script will accept, you can check the args.py file contained within the setup folder [here](./setup/args.py)   

Currency pairs passed in must adhere to Oandas v20 schema - capital letters separated by an underscore. I.E. You must use ```EUR_USD``` rather than ```eur_usd``` or ```eurusd``` or ```EURUSD``` or some other variation. If you would like more information on this, you can view the Oanda Instrument developer docs [here.](https://developer.oanda.com/rest-live-v20/instrument-ep/)     

## Dependencies:

The list of required external 3rd party dependencies is: wheel, twilio, schedule, datetime, requests, json, time, argparse, numpy, tulipy & psutil.    

To install dependencies run:   

```sudo pip3 install wheel twilio schedule datetime requests argparse numpy tulipy psutil```

## Included Robots:

This is a sample repo. As such, everything is fully functional, but this contains no profitable robot algorithms.  You can view the included robot algorithms in the strategies/forex_bots_python folder [here.](https://github.com/Eric-Lingren/oanda_v20_platform_public/tree/master/strategies/forex_bots_python) 

Included is a simple price printer, a basic order execution bot and a simple RSI execution bot.   

Feel free to use this as a platform for your own usage and development of your own robots or contact me if you have ideas of things you would like to see built.   

**None of these bots are profitable! They are for demonstration purposes only. I will not be responsible if you run them on a live account.**

### Indicators:

All indicators are custom built. If you need more than those included, you will need to build your own into the framework.
### Here are some example method calls for reference:
    # print(oanda.Account.get_account())
    # print(oanda.Account.get_account_balance())
    # print(oanda.Account.get_open_positions())
    # print(oanda.Account.get_open_trades())
    # print(oanda.Account.Order.get_orders())
    # print(oanda.Account.Order.get_pending_orders())
    # print(oanda.Account.Order.buy_market(100, 'EUR_USD'))
    # oanda.Account.Order.sell_market(150, 'EUR_USD')
    # print(oanda.Account.get_open_positions())
    # oanda.DataFeed.stream()
### Check All Running Script Processes on a Linux Server:
``` ps -ef | egrep "python|PID" ```   
``` ps -u {user} | egrep "python|PID" ```

### Kill Running Script Processes on a Linux Server: 
``` kill -9 <pid> ```

## Disclaimer:

_Trading foreign exchange carries a high level of risk, and may not be suitable for all investors. Past performance is not indicative of future results. Leverage can work against you as well as for you. Before deciding to invest in foreign exchange you should carefully consider your investment objectives, level of experience, and risk appetite. The possibility exists that you could sustain a loss of some or all of your initial investment and therefore you should not invest money that you cannot afford to lose. You should be aware of all the risks associated with foreign exchange trading, and seek advice from an independent financial advisor if you have any doubts._   
\
_I take no responsibility for any losses or gains you may incur from using my software. I also take no responsibility for any architecture, security, or server configurations._   
\
_This software is provided as is. No warranties or guarantees will be provided for its accuracy, completeness, reliability, or security if used within your own environment._
