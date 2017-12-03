# -*- coding: utf-8 -*-
"""
Created on 10/3/17
Author: Jihoon Kim
"""

import datetime
import pandas as pd
import time
import math
import json
import urllib.request
from account_info import api_key, api_secret
from api.xcoin_api_client import XCoinAPI
from api.config import api_url
from algorithm.utils import bollinger_band


class Trader(XCoinAPI):

        def __init__(self, currency='BTC'):

            super(Trader, self).__init__(api_key=api_key, api_secret=api_secret)
            self.currency = currency
            self.price_table = pd.DataFrame(columns={'Time', 'Price'})
            self.trade_table = pd.DataFrame(columns={'Time', 'Price', 'Units', 'Buy/Sell'})
            self.orderbook = pd.DataFrame(columns={'Bid_Price', 'Bid_Quantity', 'Ask_Price', 'Ask_Quantity'})
            self.last_currency_price = None
            self.available_cur = None
            self.available_krw = None
            self.trade_fee = None
            self.min_trade_cur_decimal = None
            self.target_bid_price = None
            self.target_ask_price = None
            self.trader_bid_price = None
            self.trader_units_bid = None

            self._set_min_trade_cur_decimal()
            self._set_trade_fee()
            self.update_wallet(report=False)
            self.info()

        def info(self):
            """
            Prints the information of Trader class.

            :return: None
            :rtype: None
            """
            print("==============[Trader INFO]==============")
            print("Currency           : " + self.currency)
            print("Last Currency Value: " + str(self.last_currency_price))
            print("Buy Price          : " + str(self.target_bid_price))
            print("Sell Price         : " + str(self.target_ask_price))
            print("Available Currency : " + str(self.available_cur))
            print("Available KRW      : " + str(self.available_krw))
            print("Trading Fee        : " + str(self.trade_fee))
            print("Min Trading Decimal: " + str(self.min_trade_cur_decimal))

            return None

        def _set_min_trade_cur_decimal(self):
            """
            Set minimum decimal to communicate Bithumb API

            :return: None
            :rtype: None
            """
            if self.currency in ['BTC', 'ZEC']:
                self.min_trade_cur_decimal = 1e-3
            elif self.currency in ['ETH', 'DASH', 'BCH', 'XMR']:
                self.min_trade_cur_decimal = 1e-2
            elif self.currency in ['LTC', 'ETC', 'QTUM']:
                self.min_trade_cur_decimal = 1e-1

            return None

        def _set_trade_fee(self):
            """
            Set trade fee

            :return: None
            :rtype: None
            """
            rg_params = {
                "currency": self.currency
            }

            response_fee = self.xcoinApiCall("/info/account", rg_params)
            self.trade_fee = float(response_fee["data"]["trade_fee"])

            return None

        def record_price(self, report=True, record=True):
            """
            Records current time and price of given currency in Pandas format.

            :return: DataFrame of current_time and price
            :rtype: pd.DataFrame
            """

            rg_params = {}
            response_ticker = self.xcoinApiCall("/public/ticker/" + self.currency, rg_params)
            status = "OK" if response_ticker['status'] == "0000" else "ERROR"
            ticker_return = dict()
            for i in response_ticker['data']:
                ticker_return['{0}'.format(i)] = response_ticker["data"][i]
            current_time = pd.to_datetime(str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")),
                                          format="%Y-%m-%d %H:%M:%S")

            if record:
                new_data = {"Time": current_time, "Price": ticker_return['closing_price']}
                self.price_table = self.price_table.append(new_data, ignore_index=True)

            if report:
                print("=============[Price Record]=============")
                print("Status: " + status)
                print("Time  : " + str(current_time))
                print("Index : " + str(len(self.price_table)))
                print("{0:6s}: ".format(self.currency) + ticker_return["closing_price"])

            return self.price_table

        def update_wallet(self, report=True):
            """
            Retrieve user's wallet information

            :param report: Print report
            :type report: Boolean
            :return: None
            :rtype: None
            """
            rg_params = {
                "currency": self.currency,
            }

            response_balance = self.xcoinApiCall("/info/balance", rg_params)
            status = "OK" if response_balance["status"] == "0000" else "ERROR"
            self.available_cur = float(response_balance["data"]["available_" + self.currency.lower()])
            self.available_krw = float(response_balance["data"]["available_krw"])

            if report:
                print("============[Wallet Update]============")
                print("Status: " + status)
                print("Available " + self.currency + ": " + str(response_balance["data"]
                                                                ["available_" + self.currency.lower()]))
                print("Available KRW: " + str(response_balance["data"]["available_krw"]))

            return None

        def order_bid(self, bid_price, units="ALL"):

            if units == "ALL":
                before_fee_unit = self.available_krw / bid_price
                expected_fee = before_fee_unit * self.trade_fee
                units_bid = math.floor((before_fee_unit - expected_fee) * (1 / self.min_trade_cur_decimal)) * self.\
                    min_trade_cur_decimal
            else:
                units_bid = math.floor(float(units) * 1/self.min_trade_cur_decimal) * self.min_trade_cur_decimal

            rg_params = {
                "order_currency": self.currency,
                "payment_currency": "KRW",
                "units": units_bid,
                "price": int(bid_price),
                "type": "bid"
            }

            response_bid = self.xcoinApiCall("/trade/place", rg_params)
            status = "OK" if response_bid["status"] == "0000" else "ERROR"

            if status == "OK":
                print("============[PLACE BUY]============")
                print("Status     : " + status)
                print("Order    ID: " + response_bid["order_id"])
                print("Order Price: " + str(self.target_bid_price))
                self.trader_bid_price = self.target_bid_price
                self.trader_units_bid = units_bid

            else:
                print(response_bid)

            current_time = pd.to_datetime(str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")),
                                          format="%Y-%m-%d %H:%M:%S")
            new_data = {"Time": current_time, "Price": bid_price, 'Units': units_bid, 'Bid/Ask': 'Bid'}
            self.trade_table = self.trade_table.append(new_data, ignore_index=True)
            self.update_wallet(report=True)
            return units_bid

        def order_ask(self, ask_price, units="ALL"):
            if units == "ALL":
                before_fee_unit = self.available_cur
                expected_fee = math.ceil(before_fee_unit * self.trade_fee)
                units_ask = math.floor((before_fee_unit - expected_fee) * (1 / self.min_trade_cur_decimal)) * self.\
                    min_trade_cur_decimal

            else:
                units_ask = math.floor(float(units) * (1 / self.min_trade_cur_decimal)) * self.min_trade_cur_decimal

            rg_params = {
                "order_currency": self.currency,
                "payment_currency": "KRW",
                "units": units_ask,
                "price": int(self.target_ask_price),
                "type": "ask"
            }

            response_sell = self.xcoinApiCall("/trade/place", rg_params)
            status = "OK" if response_sell["status"] == "0000" else "ERROR"

            if status == "OK":
                print("============[PLACE SELL]============")
                print("Status     : " + status)
                print("Order    ID: " + response_sell["order_id"])
                print("Order Price: " + str(self.target_ask_price))

            else:
                print(response_sell)

            current_time = pd.to_datetime(str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")),
                                          format="%Y-%m-%d %H:%M:%S")
            new_data = {"Time": current_time, "Price": ask_price, 'Units': units_ask, 'Bid/Ask': 'Ask'}
            self.trade_table = self.trade_table.append(new_data, ignore_index=True)
            self.update_wallet(report=True)

            return units_ask

        def order_market_price_bid(self, units="ALL"):

            if units == "ALL":
                before_fee_unit = self.available_krw / bid_price
                expected_fee = before_fee_unit * self.trade_fee
                units_bid = math.floor((before_fee_unit - expected_fee) * (1 / self.min_trade_cur_decimal)) * self.\
                    min_trade_cur_decimal
            else:
                units_bid = math.floor(float(units) * 1/self.min_trade_cur_decimal) * self.min_trade_cur_decimal

            rg_params = {
                "currency": self.currency,
                "units": units_bid
            }

            response_buy = self.xcoinApiCall("/trade/market_buy", rg_params)
            status = "OK" if response_buy["status"] == "0000" else "ERROR"

            if status == "OK":
                print("============[MARKET BUY]============")
                print("Status     : " + status)
                print("Order    ID: " + response_buy["order_id"])

                for i in range(len(response_buy["data"])):
                    print("Contract No: " + str(i))
                    print("Contract ID: " + str(response_buy["data"][i]["cont_id"]))
                    print("Units   BUY: " + str(response_buy["data"][i]["units"]))
                    print("Total   BUY: " + str(response_buy["data"][i]["total"]))
                    print("FEE        : " + str(response_buy["data"][i]["fee"]))
            else:
                print(response_buy)

            self.update_wallet(report=False)

            return units_bid

        def order_market_price_ask(self, units='ALL'):

            if units == "ALL":
                before_fee_unit = self.available_cur
                expected_fee = math.ceil(before_fee_unit * self.trade_fee)
                units_ask = math.floor((before_fee_unit - expected_fee) * (1 / self.min_trade_cur_decimal)) * self.\
                    min_trade_cur_decimal

            else:
                units_ask = math.floor(float(units) * (1 / self.min_trade_cur_decimal)) * self.min_trade_cur_decimal

            rg_params = {
                "currency": self.currency,
                "units": units_ask
            }

            response_sell = self.xcoinApiCall("/trade/market_sell", rg_params)
            status = "OK" if response_sell["status"] == "0000" else "ERROR"

            if status == "OK":
                print("============[MARKET SELL]============")
                print("Status     : " + status)
                print("Order    ID: " + response_sell["order_id"])

                for i in range(len(response_sell["data"])):
                    print("Contract No: " + str(i))
                    print("Contract ID: " + str(response_sell["data"][i]["cont_id"]))
                    print("Units  SELL: " + str(response_sell["data"][i]["units"]))
                    print("Total  SELL: " + str(response_sell["data"][i]["total"]))
                    print("FEE        : " + str(response_sell["data"][i]["fee"]))
            else:
                print(response_sell)

            self.update_wallet(report=False)

            return units_ask

        def record_orderbook(self, report=True):

            url_orderbook = urllib.request.urlopen(api_url + '/public/orderbook/' + self.currency)
            read_orderbook = url_orderbook.read()
            json_orderbook = json.loads(read_orderbook)

            status = "OK" if json_orderbook['status'] == "0000" else "ERROR"
            print("==========[Record Orderbook]==========")
            print("Time  : " + str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
            print("Status: " + status)
            for i in range(len(json_orderbook["data"]["bids"])):
                bid_price = json_orderbook["data"]["bids"][i]["price"]
                bid_quantity = json_orderbook["data"]["bids"][i]["quantity"]
                ask_price = json_orderbook["data"]["asks"][i]["price"]
                ask_quantity = json_orderbook["data"]["asks"][i]["quantity"]

                self.orderbook = self.orderbook.append({'Bid_Price': bid_price,
                                                        'Bid_Quantity': bid_quantity,
                                                        'Ask_Price': ask_price,
                                                        'Ask_Quantity': ask_quantity}, ignore_index=True)

            if report:
                print(self.orderbook.head(10))
            return self.orderbook

        def run_trading(self):

            buy_limit = self.last_currency_price
            count = 0
            file_name = str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

            while True:
                count += 1
                self.record_price()
                if len(self.price_table) > 15:
                    window = 15
                    std = 2
                    bollinger_avg, bollinger_upper, bollinger_lower = bollinger_band(self.price_table,
                                                                                     window=window, std=std,
                                                                                     draw=False)

                    if self.last_currency_price > bollinger_upper.values[-1]:
                        if self.last_currency_price >= buy_limit:
                            _, status = self.order_ask()
                            if status == "OK":
                                buy_limit = bollinger_lower.values[-1] - 200
                                print("Set Buy Limit: " + str(buy_limit))

                    elif self.last_currency_price < bollinger_lower.values[-1]:
                        _, status = self.order_bid()
                        if status == "OK":
                            # TODO this trading fee only accounts for buying fee. Should refelct selling trading fee.
                            buy_limit = self.trader_bid_price * (self.trade_fee * self.trader_units_bid * 2.5 + 1) * 1.01
                            print("Set Buy Limit: " + str(buy_limit))

                    if count % 100 == 0:
                        import matplotlib.pyplot as plt
                        self.price_table.to_csv('./log/' + file_name + '.csv', index=False)
                        plt.plot(self.price_table.index, self.price_table.Price, label="Price")
                        plt.plot(self.price_table.index, bollinger_avg, label="MA (" + str(window) + ")")
                        plt.plot(self.price_table.index, bollinger_upper, label="Upper Band (" + str(std) + "$\sigma$)")
                        plt.plot(self.price_table.index, bollinger_lower, label="Lower Band (" + str(std) + "$\sigma$)")
                        plt.fill_between(self.price_table.index, bollinger_lower, bollinger_upper, facecolor='k', alpha=.15)
                        plt.legend()
                        plt.grid()
                        plt.title("Bollinger Band (Window=" + str(window) + "), Records started on: " +
                                  str(self.price_table.Time[0]))
                        plt.savefig('./log/' + file_name + '.png')
                        plt.close()

                time.sleep(10)


