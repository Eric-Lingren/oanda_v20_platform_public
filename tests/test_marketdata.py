
import os
from oanda_v20_platform.data.marketdata import MarketData
# TODO breaks when running on CI - need to remove the ../
md = MarketData()
class TestMarketData():

    def test_db_exists(self):
        message = "Marketdata database does not exist"
        assert os.path.isfile(md.db_path), message

    def test_get_instruments(self):
        x = md.get_instruments()
        message = "MarketData did not collect the instruments form Oanda"
        assert isinstance(x, dict), message
        assert len(x) ==2, message

    def test_spreads(self):
        x = md.spreads('GBP_USD')
        message = "The spread data was not returned correctly, check the spreads function "
        assert isinstance(x, dict), message
        assert 'avg' in x.keys(), message

    def test_get_daily_candles(self):
        x = md.get_daily_candles(instrument='GBP_USD')
        message = "MarketData did not collect the candle data form Oanda"
        assert isinstance(x, dict), message
        assert len(x) >1, message
