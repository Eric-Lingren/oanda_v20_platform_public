To run the platform in terminal enter:   

```python3 main.py --account xxx-xxx-xxxxxxx-xxx --token xxxxxxxxxxx-xxxxxxxxxxxxxxx --pair EUR_USD```


Setup --

Dependencies: 
wheel
twilio 
schedule
datetime
requests
json
time
argparse
numpy
tulipy


Install Dependencies: 

sudo pip3 install wheel twilio schedule datetime requests argparse numpy tulipy

#### Some example method calls for reference:
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