import os
from oanda.marketdata import MarketData
md = MarketData()

class TestMarketData():

    def test_db_exists(self):
        message = "Marketdata database does not exist"
        assert os.path.isfile('./oanda_v20_platform/data/marketdata.db'), message

    def test_get_instruments(self):
        x = md.instruments
        message = "MarketData did not collect the instruments form Oanda"
        assert isinstance(x, dict), message
        assert len(x) ==2, message

    def test_spreads(self):
        x = md.spreads('GBP_USD')
        message = "The spread data was not returned correctly, check the spreads function "
        assert isinstance(x, dict), message
        assert 'avg' in x.keys(), message
