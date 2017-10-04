# -*- coding: utf-8 -*-
"""
Created on 10/4/17
Author: Jihoon Kim
"""


import matplotlib.pyplot as plt


def bollinger_band(table, window=20, std=2, draw=True):

    """

    :param table:
    :type table:
    :param window:
    :type window:
    :param std:
    :type std:
    :param draw:
    :type draw:
    :return:
    :rtype:
    """
    moving_avg_price = table.Price.rolling(window).mean()
    moving_std_price = table.Price.rolling(window).std()

    upper_band = moving_avg_price + (moving_std_price * std)
    lower_band = moving_avg_price - (moving_std_price * std)

    if draw:
        plt.plot(table.index, table.Price, label="Price")
        plt.plot(table.index, moving_avg_price, label="MA (" + str(window) + ")")
        plt.plot(table.index, upper_band, label="Upper Band (" + str(std) + "$\sigma$)")
        plt.plot(table.index, lower_band, label="Lower Band (" + str(std) + "$\sigma$)")
        plt.fill_between(table.index, lower_band, upper_band, facecolor='m', alpha=.15)
        plt.legend()
        plt.title("Bollinger Band (Window=" + str(window) + "), Records started on: " +
                  str(table.Time[0]))

    return moving_avg_price, upper_band, lower_band
