# import pytest
from oanda.oanda import Oanda, Order, Account, DataFeed

oanda = Oanda()
oanda_live = Oanda(practice=False)
oanda_gbp = Oanda(pair='GBP_USD')
order = Order()
acc = Account()
data = DataFeed()

class TestOanda:

    def test_token(self):
        message1 = "Does the token str exist" 
        message2 = "Is the token the expected length"
        x = oanda.token
        assert isinstance(x, str), message1
        assert len(x) > 60, message2

    def test_account_number(self):
        "Does the account str exist and is it the correct type and length"
        x = oanda.account
        assert isinstance(x, str)
        assert len(x) >= 10

    def test_set_base_url(self):
        if oanda.practice == True:
            message = f"Practice account url not set correctly - {oanda.base_url}"
            assert oanda.base_url == 'https://api-fxpractice.oanda.com', message
        elif oanda_live.practice == False:
            message = f"Live account url not set correctly - {oanda_live.base_url}"
            assert oanda_live.base_url == 'https://stream-fxtrade.oanda.com', message

    def test_default_pair(self):
        message = f"Default pair should be 'EUR_USD - It's {oanda.pair}!"
        assert oanda.pair == 'EUR_USD', message

    def test_pair_switching(self):
        message = f"Pair should have changed to 'GBP_USD' - It's {oanda_gbp.pair}"
        assert oanda_gbp.pair == 'GBP_USD', message

    def test_set_headers(self):
        message = f"Authorizarion Header not set correctly, it does not contain the API token!"
        assert oanda.token in oanda.headers['Authorization'], message
    
class TestAccount():

    def test_get_account(self):
        x = acc.account_info
        message = "Account info did not return the correct data structure"
        assert isinstance(x, dict), message
        message2 = "Account info does not contain any information"
        assert len(x) >= 2, message2
        account_id = x['account']['id']
        message3 = ("The account info returned is not for the "
        f"correct account! - acc:{oanda.account} - returned{account_id}")
        assert oanda.account == account_id, message3

    def test_account_balance(self):
        message = f"There is no money in the account!! - balance returned = {acc.account_balance}"
        assert float(acc.account_balance) > 0, message

class TestOrder():
    pass

class TestDataFeed():

    def test_data0(self):
        if data.backfill == True:
            data_length = len(data.data0)
            message = f"We should have got 500 candle back - got {data_length} instead"
            assert  data_length == 500, message

        message2 = f"We did not get a list back fro data0 as expected"
        assert isinstance(data.data0, list), message2

        message3 = ("We did not get the expected keys 'complete', 'volume', "
        "'time', 'bid', 'ask' back in the data")
        assert 'complete' in data.data0[0].keys(), message3
        assert 'volume' in data.data0[0].keys(), message3
        assert 'time' in data.data0[0].keys(), message3
        assert 'bid' in data.data0[0].keys(), message3
        assert 'ask' in data.data0[0].keys(), message3

    def test_ohlc_in_data0(self):
        bid = data.data0[0]['bid']
        message = "o, h, l, c data not returned in data0!"
        assert 'o' in bid, message
        assert 'h' in bid, message
        assert 'l' in bid, message
        assert 'c' in bid, message
        