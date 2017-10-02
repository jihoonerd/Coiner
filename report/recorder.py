# -*- coding: utf-8 -*-
"""
Created on 10/3/17
Author: Jihoon Kim
"""


def recorder(currency='ETH', interval=10):

    """
    Records time and price of given currency in Pandas format.

    :param currency: The type of currency
    :type currency: string or None
    :param interval: Time interval of recording
    :type interval: int
    :return: DataFrame of time and price
    :rtype: pd.DataFrame
    """
    return price_record