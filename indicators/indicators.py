import numpy as np
import tulipy as ti
import requests


class Indicator:
    def __init__(self):
        self.indicator_base_url = 'http://api.fxhistoricaldata.com/indicators?'

    def sma(self, data, period, ba, ohlc):
        series_arr = []
        for item in data[:period]:
            value = round(float(item[ba][ohlc]),5)
            series_arr.append(value)
        DATA = np.array(series_arr)
        sma = ti.sma(DATA, period=period)
        return sma

    def rsi(self, ohlc, period, pair, timeframe):
        exp = f"{ohlc},rsi({ohlc},{period})"
        params = {
            'expression' : exp,
            'instruments' : pair,
            'timeframe' : timeframe,
            'item_count' : 3
        }
        r = requests.get(self.indicator_base_url, params=params)
        data = r.json()
        rsi_results_array = data['results'][pair]['data']
        rsi_data = []
        for rsi_bar in rsi_results_array:
            rsi_data.append(rsi_bar[-1])
        return rsi_data




