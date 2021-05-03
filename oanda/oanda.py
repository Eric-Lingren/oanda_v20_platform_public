
import requests
import json
import time
from notifier.sms import TwilioSMS
from notifier.system_logger import config_logger
from auth.auth import Tokens
t = Tokens()

class Oanda(object):
    """Base class to access account"""
    def __init__(self, token=t.token, account=t.account, practice=True, pair='EUR_USD', 
                text_notifications=False, **kwargs):

        super().__init__(**kwargs)
        self.token = token
        self.account = account
        self.practice = practice
        self.pair = pair
        self.text_notifications = text_notifications

        self.global_logger = config_logger()
        self.base_url = self.set_base_url()
        self.headers = self.set_headers()


    def set_base_url(self):
        if self.practice:
            return 'https://api-fxpractice.oanda.com'
        else:    
            return 'https://stream-fxtrade.oanda.com'

    
    def set_headers(self):
        return {'Authorization': 'Bearer ' + self.token}

    def print_details(self):
        print(f'Token: {self.token}')
        print(f'Account Number: {self.account}')
        print(f'Base Url: {self.base_url}')
        print(f'Headers: {self.headers}')


class Account(Oanda):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.account_info = self.get_account()
        self.account_balance = self.get_account_balance()
        self.open_positions = self.get_open_positions()
        self.open_trades = self.get_open_trades()

    
    def get_account(self):
        try:
            url = self.base_url + '/v3/accounts/' + self.account
            r = requests.get(url, headers=self.headers)
            data = r.json()
            if data:
                print(f"Account connected ok!")
            else:
                self.global_logger.error(f"OANDA API ERROR - Account.get_account - failed to retrieve data ")
            return data

        except Exception as e:
            self.global_logger.error(f"OANDA API ERROR - Account.get_account - failed to retrieve data ")
            print(e.message, e.args) 
            


    def get_account_balance(self):
        try:
            balance = self.account_info['account']['balance']
            return balance
        except Exception as e:
            self.global_logger.error(f"OANDA API ERROR - Account.get_balance - failed to retrieve data ")
            print(e.message, e.args) 

    
    def get_open_positions(self):
        try:
            url = self.base_url + '/v3/accounts/' + self.account + '/openPositions'
            r = requests.get(url, headers=self.headers)
            data = r.json()
            return data
        except Exception as e:
            self.global_logger.error(f"OANDA API ERROR - Account.get_open_positions failed to get any data")
            print(e.message, e.args) 
            

    def get_open_trades(self):
        try:
            url = self.base_url + '/v3/accounts/' + self.account + '/openTrades'
            r = requests.get(url, headers=self.headers)
            data = r.json()
            return data['trades']
        except Exception as e:
            self.global_logger.error(f"OANDA API ERROR - Account.get_open_trades failed to get any data")
            print(e.message, e.args) 


    def find_matching_trades(self):
        new_list = []
        for item in self.open_trades:
            if item['instrument'] == self.pair:
                new_list.append(item)
        sorted_list = sorted(new_list, key = lambda i: i['id'])
        return sorted_list


class Order(Account):
    def __init__(self, twilio_sid=None, twilio_token=None, 
                twilio_number=None , recipient_number=None, **kwargs):
        super().__init__(**kwargs)
        self.order = None
        self.twilio_sid = twilio_sid
        self.twilio_token = twilio_token 
        self.twilio_number = twilio_number 
        self.recipient_number = recipient_number


    def get_orders(self):
        try:
            url = self.base_url + '/v3/accounts/' + self.account + '/orders'
            r = requests.get(url, headers=self.headers)
            data = r.json()
            return data
        except Exception as e:
            self.global_logger.error(f"OANDA DATA ERROR - Order.get_orders failed to return any orders")
            print(e.message, e.args) 


    def get_pending_orders(self):
        try:
            url = self.base_url + '/v3/accounts/' + self.account + '/pendingOrders'
            r = requests.get(url, headers=self.headers)
            data = r.json()
            return data
        except Exception as e: 
            self.global_logger.error(f"OANDA DATA ERROR - Order.get_pending_orders failed to return any pending orders")
            print(e.message, e.args) 


    def buy_market(self, units, instrument):
        try:
            url = self.base_url + '/v3/accounts/' + self.account + '/orders'
            data = {
                "order": {
                    "units": units,
                    "instrument": instrument,
                    "timeInForce": "FOK",
                    "type": "MARKET",
                    "positionFill": "DEFAULT"
                }
            }
            r = requests.post(url, headers=self.headers, json=data)
            self.notify_order(r.json())
        except Exception as e:
            self.global_logger.error(f"OANDA DATA ERROR - Order.buy_market failed to send the order")
            print(e.message, e.args) 


    def sell_market(self, units, instrument):
        try:
            url = self.base_url + '/v3/accounts/' + self.account + '/orders'
            data = {
                "order": {
                    "units": -units,
                    "instrument": instrument,
                    "timeInForce": "FOK",
                    "type": "MARKET",
                    "positionFill": "DEFAULT"
                }
            }
            r = requests.post(url, headers=self.headers, json=data)
            self.notify_order(r.json())
        except Exception as e:
            self.global_logger.error(f"OANDA DATA ERROR - Order.sell_market failed to send the order")
            print(e.message, e.args) 
            

    def notify_order(self, order):
        self.order = order
        if 'orderCancelTransaction' in self.order:
            print('Order Transaction Canceled:')
            msg = f"{order['orderCancelTransaction']['type']}, {order['orderCancelTransaction']['reason']}"
            print(msg)
            if self.text_notifications:
                TwilioSMS(self.twilio_sid, self.twilio_token, self.twilio_number, 
                            self.recipient_number).send_text(msg)

            self.global_logger.error(f"OANDA ORDER ERROR - {msg}")
        print('\n')
        if 'orderFillTransaction' in self.order:
            time = order["orderFillTransaction"]["time"]
            orderID = order["orderFillTransaction"]["orderID"]
            instrument = order["orderFillTransaction"]["instrument"]
            units = order["orderFillTransaction"]["units"]
            price = order["orderFillTransaction"]["price"]
            reason = order["orderFillTransaction"]["reason"]
            pl = order["orderFillTransaction"]["pl"]
            msg = f'*** ORDER FULFILLED ***\nTime: {time}\nType: {reason}\nOrder Id: {orderID}\nInstrument: {instrument}\nUnits: {units}\nPrice: {price}\nP/L: ${pl}'
            print(msg)
            if self.text_notifications:
                TwilioSMS(self.twilio_sid, self.twilio_token, self.twilio_number, self.recipient_number).send_text(msg)
            self.global_logger.info(f"OANDA ORDER SUCCESSFUL - {msg}")


    def close_trade(self, order_id):
        try:
            url = self.base_url + '/v3/accounts/' + self.account + '/trades/' + order_id + '/close'
            r = requests.put(url, headers=self.headers)
            self.notify_order(r.json())
        except Exception as e:
            self.global_logger.error(f"OANDA DATA ERROR - Order.close_trade failed to send the order")
            print(e.message, e.args) 



class DataFeed(Oanda):

    def __init__(self, backfill=True, **kwargs):
        super().__init__(**kwargs)
        self.backfill= backfill
        self.data0 = self.set_init_data0()
        self.stream_url = self.set_stream_url()
    
    def set_init_data0(self):
        try:
            # TODO allow the setting of different params
            params = { 'granularity': 'M1', 'count': 1, 'price' : 'BA' }
            if self.backfill:
                params['count'] = 500
            url = self.base_url + '/v3/instruments/' + self.pair + '/candles?'
            r = requests.get(url, headers=self.headers, params=params)
            data = r.json()
            bars = data['candles'][::-1]
            return bars
        except Exception as e:
            self.global_logger.error(f"OANDA DATA ERROR - Datastream.set_init_data0 - did not get any data")
            print(e.message, e.args) 


    def rebuild_data(self, latest_bar):
        latest_bar_time = latest_bar['time']
        last_bar_time = self.data0[0]['time']
        if latest_bar_time != last_bar_time:
            self.data0.insert(0, latest_bar)
            if len(self.data0) > 500 :  # Only keeps the last 500 bars in memory
                self.data0.pop()

    def refresh_data(self):
        try:
            url = self.base_url + '/v3/instruments/' + self.pair + '/candles?count=1&price=BA'
            # TODO allow the setting of different params
            params = { 'granularity': 'M1' }
            r = requests.get(url, headers=self.headers, params=params)
            data = r.json()
            latest_bar = data['candles'][::-1][0]
            self.rebuild_data(latest_bar)
        except Exception as e:
            self.global_logger.error(f"OANDA DATA ERROR - Datastream.refresh_data - did not get any data")
            print(e.message, e.args) 


    def set_stream_url(self): # Does Work, Not currently used.
        if self.practice:
            return 'https://stream-fxpractice.oanda.com/v3/accounts/' + self.account + "/pricing/stream"
        else:
            return 'https://stream-fxtrade.oanda.com/v3/accounts/' + self.account + "/pricing/stream"

    
    def connect_to_stream(self): # Does Work, Not currently used.
        try:
            s = requests.Session()
            params = {'instruments' : self.pair}
            req = requests.Request('GET', self.stream_url, headers = self.headers, params = params)
            pre = req.prepare()
            resp = s.send(pre, stream = True, verify = True)
            return resp
        except Exception as e:
            print(e.message, e.args) 
            

    def stream(self):  # Does Work, Not currently used.
        response = self.connect_to_stream()
        print(response.status_code)
        if response.status_code != 200:
            return None
        for line in response.iter_lines(1):
            if line:
                try:
                    line = line.decode('utf-8')
                    msg = json.loads(line)
                except Exception as e:
                    print(e.message, e.args) 
        
                if "instrument" in msg or "tick" in msg:
                    print('\n' + line)

if __name__=="__main__":

    test = Oanda()
# %%
