# -*- coding: utf-8 -*-
"""
Created on 10/3/17
Author: Jihoon Kim
"""

from account_info import api_key, api_secret
import pandas as pd


class Trader(object):

    def __init__(self, currency, trade_algorithm, api_key=api_key, api_secret=api_secret):
        self.currency = currency
        self.trade_algorithm = trade_algorithm
        self.api_key = api_key
        self.api_secret = api_secret
        self.table = pd.DataFrame(columns={'Time', 'Price'})

