
import json 
import datetime
import numpy as np
import pandas as pd 
from pandas import json_normalize
import sqlalchemy as sq
import requests
from oanda.oanda import Account # oanda_v20_platform.
import os.path
import logging
from utils.fileops import get_abs_path 


# TODO add updated to the database and have a check to update each day
class MarketData(Account):
    """Creates a sqlite database of current market information - for use by the trading strategies.
        DB Browser https://sqlitebrowser.org/ can be used for easy viewing and filtering.
        Focused on daily data it incudes for every tradable instrument in a table with:
        The Last 60 days of data
        Yesterdays Volume, Open, High, Low, and Close
        The 55 day Vol, O, H, L, C
        The 20 day Vol, O, H, L, C
        The 10 day Vol, O, H, L, C
        True Range for each day - a volatility measure that captures gaps
        N the 20 day average True Range - like ATR(20)
        
        And a summary table of market data (called marketdata) required for trading effectively, 
        which includes the following information:
        Trading costs such as financing rates and the days they are applied.
        Pip positions (decimal points) for each instrument 
        Margin rates
        Max and Min Trailing stop distances
        Maximum order sizes
        The average spread
        The volatility (as N)
        The spread percentage of N - enabling the selection of a trading range where trade costs are minimised
            e.g. if spread is 20 and stop loss (SP) and take profit (TP) are 100 your trading edge has 
            to be able to overcome that ~20% cost to have any chance of succeeding - some of the instruments 
            with high spread % N are very hard (impossible) to trade profitably without a crystall ball.

        The N per 100X spread provides a quick way to get the target trading range where the spread cost will 
        be ~1% e.g. US30_USD currently has a Nper100Spread of 1.92 and an N of 380 so if TP and SP are set to
        380/1.92=198 pips you will only lose ~1% in spread cost and with the daily range at 380 you should 
        hit one of the targets in a day or so. Compared to say USD_JPY which currently has a N of 0.60 and 
        a Nper100Spread of 0.4 so if spread cost is kept to ~1% it will be a move of 1.5 (0.6/0.4) more like 
        3-4 days before a target will be hit. This column can be sorted to get a top 10 of instruments that 
        are efficeint to trade.

        The asset class and base currency

    Args:
        db_path str, default='data/marketdata.db': 
            The path to the database from the directory where this class is being run.
    """
    def __init__(self, db_path=get_abs_path(['oanda_v20_platform','data', 'marketdata.db']), **kwargs):
        super().__init__(**kwargs)
        self.logger = logging.getLogger(__name__)
        # setup connection to the database
        self.db_path=db_path
        self.engine = sq.create_engine(f'sqlite:///{self.db_path}')

        # does the db exist if not create it by connecting
        if not os.path.isfile(self.db_path):
            conn =  self.engine.connect()
            conn.execute("commit")
            conn.close()
            self.logger.info(f"Empty MarketData database created at: {self.db_path}")

        # get todays date
        self.today = datetime.datetime.now().strftime('%Y-%m-%d')
        
        try: # do we need to update marketdata?
            sql = """SELECT DISTINCT(Updated) FROM marketdata;"""
            data_date= pd.read_sql_query(sql, con=self.engine)

        except: # only an empty db exists - build db
            self.instruments = self.get_instruments()
            self.build_db()
            self.logger.info("Market data added to the database")

        # is marketdata out of date?
        if data_date.loc[0].item() != self.today:
            self.instruments = self.get_instruments()
            self.build_db()
            self.logger.info("Market data updated in the database")
        
        else: # get the marketdata
            df = pd.read_sql_query(sql="""SELECT name, type, marginRate, N, avgSpread, 
                                                "financing.longRate", "financing.shortRate",
                                                "Spread % N"
                                            FROM marketdata """,
                                            con=self.engine)
                        
            self.marketdata = df[['name', 'type', 'marginRate', 'N', 'avgSpread', 
                                 'financing.longRate', 'financing.shortRate',
                                 'Spread % N']].sort_values(by='Spread % N')

    def get_core_assets(self):
        pass
        self.core = pd.read_sql_query(sql="""SELECT DISTINCT Base Currency, Asset FROM marketdata""", con=self.engine)
        self.core_list = self.core['Instrument'].to_list()


    def build_db(self):
            # add data to the instruments
            for i in self.instruments['instruments']:
                ix = i['name']
                self.logger.info(f"Collecting market data for {ix}")
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

            df['Updated'] = self.today
            
            df.to_sql('marketdata', con=self.engine, if_exists='replace')

       
    
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
        self.logger.debug(f"Get Instruments returned {r} status code")
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
        self.logger.debug(f"Spreads function returned {r} status code")
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
        self.logger.debug(f"Get daily candles returned {r} status code")
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

        # Calculate the recent volatility (True Range) taking account of gaps
        # As in the Turtle trading methodology
        # NOTE max() doesn't play well with shift so break out into columns
        df['R1'] = df['high'] - df['low']
        df['R2'] = df['high'] - df['close'].shift(1) 
        df['R3'] = df['close'].shift(1) - df['low']
        # get the True Range
        df['True Range'] = df[['R1', 'R2', 'R3']].max(axis=1)
        # Get the Turtle N like ATR(20)
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
        # return the last line - yesterdays data
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

if __name__=="__main__":
    os.chdir('..')
    market = MarketData()

