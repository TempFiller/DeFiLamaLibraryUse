# Python convention to indicate that this is a script which can be run.
if __name__ == '__main__':
    print('This is a working script')

# This is a Python script to use the DeFiLama API to get TVL of different projects
# Link for API documentation/endpoints for Python:https://defillama.com/docs/api

# Each library is already installed in the virtual environment of this PyCharm project
# import the pandas library to use its functions and to work with dataframes
# import the requests library to use its functions and to work with url/API calls
# import the pprint module for a capability to “pretty-print” arbitrary Python data structures. Allows better overview.
import pandas as pd
import requests
import json
import pprint

#  Install the DeFi Lama library directly into an activated virtual environment: $ pip install DeFiLlama
from defillama import DefiLlama

# initialize api client
llama = DefiLlama()

###################################################################################################################
# possible functions of the defilama library. Similar to the API Documentation: https://defillama.com/docs/api

# Get all protocols data. Endpoint: GET /protocols
# response = llama.get_all_protocols()

# Get historical values of total TVL (all). Endpoint: GET /charts
# response = llama.get_historical_tvl()
# print(response)

# Get protocol TVL (current). Endpoint: GET /tvl/{name}
# response = llama.get_protocol_tvl(name='uniswap')
# print(response)
####################################################################################################################
# Now the function to get the historical TVL data for a project
# Get a protocol data (historical liquidity and TVL by Unix timestamp)
# Endpoint: GET /protocol/{name}

# Uniswap
response_UNI = llama.get_protocol(name='uniswap')
# print(response)

# with the pprint command we can get a better overview of the data output and what we need of it.
# Can then easier create a dataframe
#pprint.pprint(response_UNI)

# use pandas to create a dataframe with the wanted columns
df_TLV_history_UNI = pd.DataFrame(response_UNI, columns=['tvl'])
print(df_TLV_history_UNI)

# save the created table as a CSV file which then can be used in the analysis (after some minor changes/formatting).
# index = False: No Index Row in CSV
df_TLV_history_UNI.to_csv("TLV_history_UNI.csv", index=False)

# Curve Finance
response_CURVE = llama.get_protocol(name='curve')
# print(response)
df_TLV_history_CURVE = pd.DataFrame(response_CURVE, columns=['tvl'])
print(df_TLV_history_CURVE)
df_TLV_history_CURVE.to_csv("TLV_history_CURVE.csv", index=False)

# Maker DAO
response_MAKER = llama.get_protocol(name='makerdao')
# print(response)
df_TLV_history_MAKER = pd.DataFrame(response_MAKER, columns=['tvl'])
print(df_TLV_history_MAKER)
df_TLV_history_MAKER.to_csv("TLV_history_MAKER.csv", index=False)

# AAVE
response_AAVE = llama.get_protocol(name='aave')
# print(response)
df_TLV_history_AAVE = pd.DataFrame(response_AAVE, columns=['tvl'])
print(df_TLV_history_AAVE)
df_TLV_history_AAVE.to_csv("TLV_history_AAVE.csv", index=False)

# COMPOUND
response_COMP = llama.get_protocol(name='compound')
# print(response)
df_TLV_history_COMP = pd.DataFrame(response_COMP, columns=['tvl'])
print(df_TLV_history_COMP)
df_TLV_history_COMP.to_csv("TLV_history_COMP.csv", index=False)

# INSTADAPP
response_INSTADAPP = llama.get_protocol(name='instadapp')
# print(response)
df_TLV_history_INSTADAPP = pd.DataFrame(response_INSTADAPP, columns=['tvl'])
print(df_TLV_history_INSTADAPP)
df_TLV_history_INSTADAPP.to_csv("TLV_history_INSTADAPP.csv", index=False)

# SUSHI
response_SUSHI = llama.get_protocol(name='sushiswap')
# print(response)
df_TLV_history_SUSHI = pd.DataFrame(response_SUSHI, columns=['tvl'])
print(df_TLV_history_SUSHI)
df_TLV_history_SUSHI.to_csv("TLV_history_SUSHI.csv", index=False)

# BALANCER
response_BALANCER = llama.get_protocol(name='balancer')
# print(response)
df_TLV_history_BALANCER = pd.DataFrame(response_BALANCER, columns=['tvl'])
print(df_TLV_history_BALANCER)
df_TLV_history_BALANCER.to_csv("TLV_history_BALANCER.csv", index=False)

# dydx
response_dydx = llama.get_protocol(name='dydx')
# print(response)
df_TLV_history_dydx = pd.DataFrame(response_dydx, columns=['tvl'])
print(df_TLV_history_dydx)
df_TLV_history_dydx.to_csv("TLV_history_dydx.csv", index=False)

# BANCOR
response_BANCOR = llama.get_protocol(name='bancor')
# print(response)
df_TLV_history_BANCOR = pd.DataFrame(response_BANCOR, columns=['tvl'])
print(df_TLV_history_BANCOR)
df_TLV_history_BANCOR.to_csv("TLV_history_BANCOR.csv", index=False)

# WBTC
response_WBTC = llama.get_protocol(name='wbtc')
# print(response)
df_TLV_history_WBTC = pd.DataFrame(response_WBTC, columns=['tvl'])
print(df_TLV_history_WBTC)
df_TLV_history_WBTC.to_csv("TLV_history_WBTC.csv", index=False)

######################################################################################################################

# Now we want to get the historical TVL of DeFi on all chains (tracked by DeFi Llama).
# Returns historical values of the total sum of TVLs from all listed protocols. Endpoint: GET /charts
response_TVL_all = llama.get_historical_tvl()
# print(response_TVL_all)
pprint.pprint(response_TVL_all)
df_TLV_history_all = pd.DataFrame(response_TVL_all)
df_TLV_history_all.to_csv("TLV_history_all.csv", index=False)

######################################################################################################################

# unfortunately is the Endpoint: GET /charts/{chain} is not defined in the defillama library. So we have to construct a
# class and function ourselves to get the historical TVL of a chain (i.e. Ethereum)

# --------- Constants --------- #

BASE_URL = "https://api.llama.fi"

# --------- Constants --------- #


class DefiLlama:
    """
    DeFi Llama class to act as DeFi Llama's API client.
    All the requests can be made through this class.
    """

    def __init__(self):
        """
        Initialize the object
        """
        self.session = requests.Session()

    def _send_message(self, method, endpoint, params=None, data=None):
        """
        Send API request.
        :param method: HTTP method (get, post, delete, etc.)
        :param endpoint: Endpoint (to be added to base URL)
        :param params: HTTP request parameters
        :param data: JSON-encoded string payload for POST
        :return: dict/list: JSON response
        """
        url = BASE_URL + endpoint
        response = self.session.request(method, url, params=params,
                                 data=data, timeout=30)
        return response.json()

    def _get(self, endpoint, params=None):
        """
        Get API request
        :param endpoint: Endpoint (to be added to base URL)
        :param params: HTTP request parameters
        :return:
        """
        return self._send_message('GET', endpoint, params=params)

    def get_historical_tvl_chain(self, name):
        """
        Returns historical values of the total sum of TVLs from a specific listed protocol.
        Endpoint: GET /charts/{chain}

        :return: JSON response
        """
        path = f'/charts/{name}'

        return self._get(path)


# now we can use the new function fo the DeFiLlama class to get the TVL on the Ethereum chain
response_TVL_ETHchain = DefiLlama().get_historical_tvl_chain(name='Ethereum')
# print(response_TVL_ETHchain)
pprint.pprint(response_TVL_ETHchain)
df_TLV_history_ETH = pd.DataFrame(response_TVL_ETHchain)
df_TLV_history_ETH.to_csv("TLV_history_ETH.csv", index=False)
