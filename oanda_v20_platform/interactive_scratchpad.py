# %%
# import DataFeed and run on defaults to experiment in ipython
from oanda_v20_platform.data import marketdata
from oanda_v20_platform.data.marketdata import MarketData
from oanda.oanda import DataFeed 
testDataFeed = DataFeed()
# %%
stream =   {"type":"PRICE",
            "time":"2021-05-13T22:00:43.020656828Z",
            "bids":[{"price":"1.20804","liquidity":10000000}],
            "asks":[{"price":"1.20828","liquidity":10000000}],
            "closeoutBid":"1.20804","closeoutAsk":"1.20828",
            "status":"tradeable",
            # "tradeable":true,
            "instrument":"EUR_USD"}

# %%
float(stream['bids'][0]['price'])

# %%
from data.marketdata import MarketData()
md = MarketData()

# %% 
from pathlib import Path

# %%

p = Path()
# %%

def get_db_path(pathlist=['data', 'marketdata.db']):
    """To solve the problem of finding files with relative
    paths on windows/linux/mac etc. esp when a module has been 
    imported into a different working directory
    This finds the current working directory cuts it back
    to oanda_v20_platform then adds the components of pathlist
    Args:
        pathlist list of str, folder and filenames required
        after oanda_v20_platform
    Returns:
         a pathlib object with the absolute path
        
    """
    p = Path()
    # get the current working dir
    cwd = p.cwd()
    # get the dir tree
    l = list(cwd.parts)
    # shorten it to the oanda_v20_platform root
    l = l[:l.index('oanda_v20_platform')+1]
    for x in pathlist:
        l.append(x)
    newpath = Path(*l)

    return newpath.absolute()





# %%
from oanda.oanda import Account
testAcc = Account()
# %%
import numpy as np
import pandas as pd 
from pandas.io.json import json_normalize
import sqlalchemy as sq
import json
import requests
# %%
# def get_instruments(self, params=None):
#         """Get instruments and there associated static data.
#         By default gets the core instruments stored in a csv. These core
#         instruments are the unique available instruments. 
#         Returns:
#             json: contains data that describes the available instruments
#         """
#         # if params == None:
#         #     params = {"instruments": ",".join(self.core_list)}

url = testAcc.base_url + '/v3/accounts/' + testAcc.account + '/instruments'
r = requests.get(url, headers=testAcc.headers)
# %%
data = r.json()


    # r = accounts.AccountInstruments(accountID=testAcc.account, 
    #                                 params=None)
    # self.client.request(r)
    # return r.response
# %%
