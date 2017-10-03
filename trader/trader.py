# -*- coding: utf-8 -*-
"""
Created on 10/3/17
Author: Jihoon Kim
"""

import urllib.request
import json
import datetime
import pandas as pd

from config import api_url
from account_info import api_key, api_secret
from xcoin_api_client import XCoinAPI


class Trader(XCoinAPI):

    def __init__(self, currency='ETH', trade_algorithm=None, api_key=api_key, api_secret=api_secret):

        super(Trader, self).__init__(api_key=api_key, api_secret=api_secret)
        self.currency = currency
        self.trade_algorithm = trade_algorithm
        self.table = pd.DataFrame(columns={'Time', 'Price'})
        self.available_eth = 0
        self.available_krw = 0

    def recorder(self):
        """
        Records time and price of given currency in Pandas format.

        :return: DataFrame of time and price
        :rtype: pd.DataFrame
        """

        url_ticker = urllib.request.urlopen(api_url + '/public/ticker/' + self.currency)
        read_ticker = url_ticker.read()
        json_ticker = json.loads(read_ticker)
        status = "OK" if json_ticker['status'] == "0000" else "ERROR"

        time = str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        CUR = json_ticker['data']['closing_price']
        print("===========================")
        print("Time  : " + time)
        print("Status: " + status)
        print("{0:6s}: ".format(self.currency) + CUR)
        print("===========================")

        time = pd.to_datetime(time, format="%Y-%m-%d %H:%M:%S")
        CUR = float(json_ticker['data']['closing_price'])

        new_data = {'Time': time, 'Price': CUR}
        self.table = self.table.append(new_data, ignore_index=True)

        return self.table

    def update_wallet(self, currency="ETH"):

        rgParams = {
            "currency": currency,
        }

        result = self.xcoinApiCall("/info/balance", rgParams)
        self.available_eth = float(result["data"]["available_eth"])
        self.available_krw = float(result["data"]["available_krw"])
        #print("Available " + currency + ": " + result["data"]["available_eth"])
        #print("Available KRW: " + result["data"]["available_krw"])
