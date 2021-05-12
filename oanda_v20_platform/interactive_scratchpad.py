# %%
# import DataFeed and run on defaults to experiment in ipython
from oanda.oanda import DataFeed 
testDataFeed = DataFeed()
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
