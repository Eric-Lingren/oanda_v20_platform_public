
import json 
import datetime
from sqlite3.dbapi2 import connect
import numpy as np
import pandas as pd 
from pandas import json_normalize
import sqlalchemy as sq
import requests
from oanda_v20_platform.oanda.oanda import Account
import os.path

# TODO add updated to the database and have a check to update each day
class MarketData(Account):
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # setup connection to the database
        self.engine = sq.create_engine('sqlite:///../data/marketdata.db')
        # does the db exist if not create it by connecting
        if not os.path.isfile('../data/marketdata.db'):
            conn =  self.engine.connect()
            conn.execute("commit")
            conn.close()
#         # get a list of available instruments and relevent data
#         self.core = pd.read_sql_table('core', con=self.engine)
#         self.core_list = self.core['Instrument'].to_list()
#         self.core_list.remove('USDX')

        self.instruments = self.get_instruments()

        # add data to the instruments
        for i in self.instruments['instruments']:
            ix = i['name']
            # add the spread data for each instrument
            i['avgSpread'] = self.avg_spread(self.spreads(ix))
            # get the price data
            df = self.make_dataframe(self.get_daily_candles(ix))
            i['volume']     = df.iloc[0, 0]
            i['open']       = df.iloc[0, 1]
            i['high']       = df.iloc[0, 2]
            i['low']        = df.iloc[0, 3]
            i['close']      = df.iloc[0, 4]
            i['True Range'] = df.iloc[0, 5]
            i['N']          = df.iloc[0, 6]
            i['55DayHigh']  = df.iloc[0, 7]
            i['20DayHigh']  = df.iloc[0, 8]
            i['10DayHigh']  = df.iloc[0, 9]
            i['55DayLow']   = df.iloc[0, 10]
            i['20DayLow']   = df.iloc[0, 11]
            i['10DayLow']   = df.iloc[0, 12]

        tags = pd.DataFrame()
        for n, i in enumerate(self.instruments['instruments']):
            x = i['tags']
            for l in x:
                tags.loc[n, 'Asset Class'] = l['name']
        
        fDayWeek = pd.DataFrame()
        for n, i in enumerate(self.instruments['instruments']):
            x = i['financing']['financingDaysOfWeek']
            for d in x:
                fDayWeek.loc[n, d['dayOfWeek'] + '-financing'] = d['daysCharged']
     
        tags = tags.merge(fDayWeek, left_index=True, right_index=True)

        df = json_normalize(self.instruments['instruments'])

        df.drop(['tags', 'financing.financingDaysOfWeek'], inplace=True, axis=1)

        df = df.merge(tags, left_index=True, right_index=True)
        
        df['Spread % N'] = round(((df['avgSpread'] * 10.00**df['pipLocation']) / df['N'])*100, 2)
        
        df['Nper100spread'] = df['N'] / ((df['avgSpread'] * 10.00**df['pipLocation']) * 100) 
        
        df['Base Currency'] = df.apply(lambda x: self.base(x), axis=1)
        
        df['Asset'] = df.apply(lambda x: self.asset(x), axis=1)
        
        df.to_sql('marketdata', con=self.engine, if_exists='replace')
        
        self.marketdata = df[['name', 'type', 'marginRate', 'N', 'avgSpread', 
                              'financing.longRate', 'financing.shortRate',
                               'Spread % N']].sort_values(by='Spread % N')
       
    
    def base(self, x):
        return x['name'].split('_')[1]


    def asset(self, x):
        return x['name'].split('_')[0]

    
    def get_instruments(self, params=None):
        """Get instruments and there associated static data.
        By default gets the core instruments stored in a csv. These core
        instruments are the unique available instruments. 
        Returns:
            json: contains data that describes the available instruments
        """
        url = self.base_url + '/v3/accounts/' + self.account + '/instruments'
        r = requests.get(url, headers=self.headers)
        data = r.json()
        return data


    def avg_spread(self, spreads_json):
        """Calculate the average spread from the json returned by spreads

        Args:
            spreads_json: json produced by spreads function

        Returns:
            float: average of the average spreads
        """
        spreads = []
        for li in spreads_json['avg']:
            spreads.append(li[1])
        return np.mean(spreads)


    
    def spreads(self, instrument, period=86400):
        """Returns a json with timestamps for every 15min
        with the min, max and average spread.
        Args:
            instrument: str, required, e.g. "EUR_USD"
            period: int, time period in seconds e.g. 86400 for day
        
        Returns:
            json: { "max": [[1520028000, 6], .....],
                    "avg": [[1520028000, 3.01822], ......],
                    "min": [[1520028000, 1.7], ......]
                    }
        """
        params = {
                "instrument": instrument,
                "period": period
                }

        url = self.base_url + '/labs/v1/spreads/'
        r = requests.get(url, headers=self.headers, params=params)
        data = r.json()
        return data



    def get_daily_candles(self, instrument):
        """Request the daily candle data from the API
            get 60 candles from yesterday
        Args:
            instrument: string describing the instrument in API

        Returns:
            json: candle data
        """

        yesterday = (datetime.datetime.now() - pd.DateOffset(days=1)).strftime("%Y-%m-%d")
        last_candle = yesterday + 'T22:00:00.000000000Z'
        params = {
                "to": last_candle,
                "count": 60,
                "granularity": "D",
                # "includeFirst": True,
                }
        url =  self.base_url +  f'/v3/instruments/{instrument}/candles/'
        r = requests.get(url, headers=self.headers, params=params)
        data = r.json()
        return data


    def make_dataframe(self, candles_data):
        """Take a json of candle data - 
        convert to a dataframe, calculate volatility, 
        max and min prices

        Args:
            candles_data ([json]): takes the json returned from get_candles

        Returns:
            sends data to sql table
            pandas df: the last line of data
        """

        df = json_normalize(candles_data.get('candles'))
        df.rename(columns={'mid.c': 'close', 'mid.h': 'high', 
                            'mid.l': 'low', 'mid.o': 'open'}, 
                            inplace=True)
        df.set_index('time', inplace=True)
        # the API returns strings these need to be converted to floats
        df.volume = pd.to_numeric(df.volume)
        df.close  = pd.to_numeric(df.close)
        df.high   = pd.to_numeric(df.high)
        df.low    = pd.to_numeric(df.low)
        df.open   = pd.to_numeric(df.open)
        # max() doesn't play well with shift so break out into columns
        df['R1'] = df['high'] - df['low']
        df['R2'] = df['high'] - df['close'].shift(1) 
        df['R3'] = df['close'].shift(1) - df['low']
        # get the turtle True Range
        df['True Range'] = df[['R1', 'R2', 'R3']].max(axis=1)
        # Get the turtle N like ATR(20)
        df['N'] = df['True Range'].rolling(window=20, min_periods=20).mean()
        # Get the latest highs and lows
        df['55DayHigh'] = df['high'].rolling(window=55, min_periods=55).max()
        df['20DayHigh'] = df['high'].rolling(window=20, min_periods=20).max()
        df['10DayHigh'] = df['high'].rolling(window=10, min_periods=10).max()
        df['55DayLow']  = df['low'].rolling(window=55, min_periods=55).min()
        df['20DayLow']  = df['low'].rolling(window=20, min_periods=20).min()
        df['10DayLow']  = df['low'].rolling(window=10, min_periods=10).min()

        df = df[['volume', 'open', 'high', 'low', 'close', 'True Range', 
                'N', '55DayHigh', '20DayHigh', '10DayHigh', '55DayLow',
                '20DayLow', '10DayLow']]

        # TODO sort index out to tidy up date string
        df.to_sql(candles_data.get('instrument') ,con=self.engine, 
                 if_exists='replace', index_label='time', index=True)

        df_ex = df.tail(1).reset_index(drop=True)
        return df_ex.tail(1)



    def json_to_dataframe(self, candles_data):
        """Take a json of candle data - 
        convert to a df
        Args:
            candles_data ([json]): takes the json returned from get_candles
        Returns:
            pandas df: the last line of data
        """
        df = json_normalize(candles_data.get('candles'))
        return df


    def format_df(self, df):
        df.rename(columns={'mid.c': 'close', 
                            'mid.h': 'high', 
                            'mid.l': 'low', 
                            'mid.o': 'open'}, 
                            inplace=True)

        df['time'] = pd.to_datetime(df['time'])
        df.set_index('time', inplace=True)
        # the API returns strings these need to be converted to floats
        df.volume = pd.to_numeric(df.volume)
        df.close  = pd.to_numeric(df.close)
        df.high   = pd.to_numeric(df.high)
        df.low    = pd.to_numeric(df.low)
        df.open   = pd.to_numeric(df.open)
        return df


    def usdx(prices):
        """calculate the U.S. dollar index
        Args: 
        prices: dataframe, required
        A single column df of prices indexed 
        to the instrument code - run for o, h, l ,c
        """
        c = 50.14348112
        euro  = prices.loc['EUR_USD']**-0.576
        yen   = prices.loc['USD_JPY']**0.136
        pound = prices.loc['GBP_USD']**-0.119
        cad   = prices.loc['USD_CAD']**0.091
        sek   = prices.loc['USD_SEK']**0.042
        swiss = prices.loc['USD_CHF']**0.036

        return c * euro * yen * pound * cad * sek * swiss


# %%
market = MarketData()


# %%
