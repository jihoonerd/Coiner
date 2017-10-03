# -*- coding: utf-8 -*-
"""
Created on 10/3/17
Author: Jihoon Kim
"""

import urllib.request
import json
from config import api_url
import datetime
import pandas as pd


def recorder(table, currency='ETH'):
    """
    Records time and price of given currency in Pandas format.

    :param currency: The type of currency
    :type currency: string or None
    :param table: Dataframe of time and price
    :type table: pd.DataFrame or None
    :return: DataFrame of time and price
    :rtype: pd.DataFrame
    """

    url_ticker = urllib.request.urlopen(api_url + '/public/ticker/' + currency)
    read_ticker = url_ticker.read()
    json_ticker = json.loads(read_ticker)
    status = "OK" if json_ticker['status'] == "0000" else "ERROR"

    time = str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    CUR = json_ticker['data']['closing_price']
    print("===========================")
    print("Time  : " + time)
    print("Status: " + status)
    print("{0:6s}: ".format(currency) + CUR)
    print("===========================")

    new_data = {'Time': time, 'Price': CUR}
    table = table.append(new_data, ignore_index=True)

    return table
