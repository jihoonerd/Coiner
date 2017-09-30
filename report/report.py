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
    urlTicker = urllib.request.urlopen('https://api.bithumb.com/public/ticker/ALL')
    readTicker = urlTicker.read()
    jsonTicker = json.loads(readTicker)

    BTC = jsonTicker['data']['BTC']['closing_price']
    ETH = jsonTicker['data']['ETH']['closing_price']
    XRP = jsonTicker['data']['XRP']['closing_price']

    status = "OK" if jsonTicker['status'] == "0000" else "ERROR"

    print("Time  : " + str(datetime.datetime.now()))
    print("Status: " + status)
    print("BTC   : " + BTC)
    print("ETH   : " + ETH)
    print("XRP   : " + XRP)

    return None
