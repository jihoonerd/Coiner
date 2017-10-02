# -*- coding: utf-8 -*-
"""
Created on 10/1/17
Author: Jihoon Kim
"""

import json
import datetime
import urllib.request
from config import api_url


def print_price(currency='ALL'):
    """
    Prints price of cryptocurrencies.
    
    :param currency: The type of currency
    :type currency: string or None
    :return: None
    :rtype: None
    """
    url_ticker = urllib.request.urlopen(api_url + '/public/ticker/' + currency)
    read_ticker = url_ticker.read()
    json_ticker = json.loads(read_ticker)
    status = "OK" if json_ticker['status'] == "0000" else "ERROR"

    print("Time  : " + str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
    print("Status: " + status)

    if currency == 'ALL':
        BTC = json_ticker['data']['BTC']['closing_price']
        ETH = json_ticker['data']['ETH']['closing_price']
        XRP = json_ticker['data']['XRP']['closing_price']

        print("BTC   : " + BTC)
        print("ETH   : " + ETH)
        print("XRP   : " + XRP)

    else:
        CUR = json_ticker['data']['closing_price']

        print("{0:6s}: ".format(currency) + CUR)

    return None
