import numpy as np
import tulipy as ti
import requests
# from notifier.system_logger import config_logger
import logging

class Indicator:
    def __init__(self):
        self.indicator_base_url = 'http://api.fxhistoricaldata.com/indicators?'
        self.logger = logging.getLogger(__name__)

    def sma(self, data, period, ba, ohlc):
        series_arr = []
        for item in data[:period]:
            value = round(float(item[ba][ohlc]),5)
            series_arr.append(value)
        DATA = np.array(series_arr)
        sma = ti.sma(DATA, period=period)
        return sma

    def rsi(self, ohlc, period, pair, timeframe):
        try:
            exp = f"{ohlc},rsi({ohlc},{period})"
            params = {
                'expression' : exp,
                'instruments' : pair,
                'timeframe' : timeframe,
                'item_count' : 3
            }
            r = requests.get(self.indicator_base_url, 
                params=params 
            )
            data = r.json()

            rsi_results_array = data['results'][pair]['data']
            rsi_data = []
            for rsi_bar in rsi_results_array:
                rsi_data.append(rsi_bar[-1])
            return rsi_data
        except:
            self.logger.exception('Failed to get RSI Indicator')