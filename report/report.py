# -*- coding: utf-8 -*-
"""
Created on 10/1/17
Author: Jihoon Kim
"""

import json
import datetime
import urllib.request


def print_price():
    """
    Prints price of cryptocurrencies.

    :return: None
    """
    url_ticker = urllib.request.urlopen('https://api.bithumb.com/public/ticker/ALL')
    read_ticker = url_ticker.read()
    json_ticker = json.loads(read_ticker)

    BTC = json_ticker['data']['BTC']['closing_price']
    ETH = json_ticker['data']['ETH']['closing_price']
    XRP = json_ticker['data']['XRP']['closing_price']

    status = "OK" if json_ticker['status'] == "0000" else "ERROR"

    print("Time  : " + str(datetime.datetime.now()))
    print("Status: " + status)
    print("BTC   : " + BTC)
    print("ETH   : " + ETH)
    print("XRP   : " + XRP)

    return None
