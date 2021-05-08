# import pytest
from oanda.oanda import Oanda, Order, Account, DataFeed

oanda = Oanda()
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