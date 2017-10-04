# -*- coding: utf-8 -*-
"""
Created on 10/4/17
Author: Jihoon Kim
"""


import matplotlib.pyplot as plt


def bollinger_band(table, window=20, std=2, draw=True):

    moving_avg_price = table.Price.rolling(window).mean()
    moving_std_price = table.Price.rolling(window).std()

    upper_band = moving_avg_price + (moving_std_price * std)
    lower_band = moving_avg_price - (moving_std_price * std)

    if draw:
        plt.figure(figsize=(800, 600))
        plt.plot(table.Time, table.Price, label="Price")
        plt.plot(table.Time, moving_avg_price, label="MA (" + str(window) + ")")
        plt.plot(table.Time, upper_band, label="Upper Band (" + str(std) + "$\sigma$)")
        plt.plot(table.Time, lower_band, label="Lower Band (" + str(std) + "$\sigma$)")
        plt.legend()
        plt.title("Bollinger Band (Window=" + str(window) + ")")

    return moving_avg_price, upper_band, lower_band
