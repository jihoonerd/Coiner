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

        def __init__(self, currency='ETH', trade_algorithm=None):

            super(Trader, self).__init__(api_key=api_key, api_secret=api_secret)
            self.currency = currency
            self.trade_algorithm = trade_algorithm
            self.table = pd.DataFrame(columns={'Time', 'Price', 'Buy_Price', 'Sell_Price'})
            self.orderbook = None
            self.last_currency_price = None
            self.available_cur = None
            self.available_krw = None
            self.trade_fee = None
            self.min_trade_cur_decimal = None
            self.target_buy_price = None
            self.target_sell_price = None
            self.trader_buy_price = None
            self.trader_buy_units = None

            self.set_trade_fee()
            self.recorder(record=False, report=False)
            self.update_wallet()
            self.set_min_trade_cur_decimal()
            self.info()

        def info(self):
            print("==============[Trader INFO]==============")
            print("Currency           : " + self.currency)
            print("Trading Algorithm  : " + str(self.trade_algorithm))
            print("Number of Logs     : " + str(len(self.table)))
            print("Last Currency Value: " + str(self.last_currency_price))
            print("Buy Price          : " + str(self.target_buy_price))
            print("Sell Price         : " + str(self.target_sell_price))
            print("Available Currency : " + str(self.available_cur))
            print("Available KRW      : " + str(self.available_krw))
            print("Trading Fee        : " + str(self.trade_fee))
            print("Min Trading Decimal: " + str(self.min_trade_cur_decimal))

            return None

        def set_min_trade_cur_decimal(self):
            if self.currency == 'BTC':
                self.min_trade_cur_decimal = 3
            elif self.currency == 'ETH':
                self.min_trade_cur_decimal = 2

            print("Set Minimum Trade Currency Decimal to " + str(self.min_trade_cur_decimal))

            return None

        def set_trade_fee(self):

            rg_params = {
                "currency": self.currency
            }

            response_fee = self.xcoinApiCall("/info/account", rg_params)
            status = "OK" if response_fee["status"] == "0000" else "ERROR"
            self.trade_fee = float(response_fee["data"]["trade_fee"])

            print("==========[Register Trade Fee]==========")
            print("Status   : " + status)
            print("Trade Fee: " + str(response_fee["data"]["trade_fee"]))

            return None

        def recorder(self, record=True, report=True):

            """
            Records current_time and price of given currency in Pandas format.

            :return: DataFrame of current_time and price
            :rtype: pd.DataFrame
            """

            rg_params = {

            }

            self.record_orderbook()
            response_recorder = self.xcoinApiCall("/public/ticker/" + self.currency, rg_params)
            status = "OK" if response_recorder["status"] == "0000" else "ERROR"
            last_price = response_recorder["data"]["closing_price"]
            current_time = str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

            if report:
                print("=============[Price Record]=============")
                print("Status: " + status)
                print("Time  : " + current_time)
                print("Index : " + str(len(self.table)))
                print("{0:6s}: ".format(self.currency) + last_price)

            current_time = pd.to_datetime(current_time, format="%Y-%m-%d %H:%M:%S")
            last_price = float(response_recorder["data"]["closing_price"])
            self.last_currency_price = last_price
            self.target_buy_price = float(self.orderbook.Buy_Price[4])
            self.target_sell_price = float(self.orderbook.Sell_Price[6])

            if record:
                new_data = {"Time": current_time, "Price": last_price}
                self.table = self.table.append(new_data, ignore_index=True)

            return self.table

        def update_wallet(self, report=True):

            rg_params = {
                "currency": self.currency,
            }

            response_update_wallet = self.xcoinApiCall("/info/balance", rg_params)
            status = "OK" if response_update_wallet["status"] == "0000" else "ERROR"
            self.available_cur = float(response_update_wallet["data"]["available_" + self.currency.lower()])
            self.available_krw = float(response_update_wallet["data"]["available_krw"])

            if report:
                print("============[Wallet Update]============")
                print("Status: " + status)
                print("Available " + self.currency + ": " + str(response_update_wallet["data"]["available_" + self.currency.lower()]))
                print("Available KRW: " + str(response_update_wallet["data"]["available_krw"]))

            return None

        def buy_place(self, units="ALL"):

            if units == "ALL":
                before_fee_unit = self.available_krw / self.target_buy_price
                expected_fee = before_fee_unit * self.trade_fee
                units_buy = math.floor((before_fee_unit - expected_fee) * (10**self.min_trade_cur_decimal))/(10**self.min_trade_cur_decimal)
            else:
                units_buy = round(float(units), self.min_trade_cur_decimal)

            rg_params = {
                "order_currency": self.currency,
                "payment_currency": "KRW",
                "units": units_buy,
                "price": int(self.target_buy_price),
                "type": "bid"
            }

            response_buy = self.xcoinApiCall("/trade/place", rg_params)
            status = "OK" if response_buy["status"] == "0000" else "ERROR"

            if status == "OK":
                print("============[PLACE BUY]============")
                print("Status     : " + status)
                print("Order    ID: " + response_buy["order_id"])
                print("Order Price: " + str(self.target_buy_price))
                self.trader_buy_price = self.target_buy_price
                self.trader_buy_units = units_buy

            else:
                print(response_buy)

            self.update_wallet(report=False)

            return units_buy, status

        def sell_place(self, units="ALL"):
            # TODO precision mismatch. before_fee_unit = self.available_cur -> flooring?
            if units == "ALL":
                before_fee_unit = self.available_cur
                expected_fee = before_fee_unit * self.trade_fee
                units_sell = math.floor((before_fee_unit - expected_fee) * (10**self.min_trade_cur_decimal))/(10**self.min_trade_cur_decimal)

            else:
                units_sell = round(float(units), self.min_trade_cur_decimal)

            rg_params = {
                "order_currency": self.currency,
                "payment_currency": "KRW",
                "units": units_sell,
                "price": int(self.target_sell_price),
                "type": "ask"
            }

            response_sell = self.xcoinApiCall("/trade/place", rg_params)
            status = "OK" if response_sell["status"] == "0000" else "ERROR"

            if status == "OK":
                print("============[PLACE SELL]============")
                print("Status     : " + status)
                print("Order    ID: " + response_sell["order_id"])
                print("Order Price: " + str(self.target_sell_price))

            else:
                print(response_sell)

            self.update_wallet(report=False)

            return units_sell, status

        def buy_market_price(self, units="ALL"):

            if units == "ALL":
                before_fee_unit = self.available_krw / self.last_currency_price
                expected_fee = before_fee_unit * self.trade_fee
                units_buy = math.floor((before_fee_unit - expected_fee) * (10**self.min_trade_cur_decimal))/(10**self.min_trade_cur_decimal)

            else:
                units_buy = round(float(units), self.min_trade_cur_decimal)

            rg_params = {
                "currency": self.currency,
                "units": units_buy
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

            return units_buy

        def sell_market_price(self, units='ALL'):

            if units == "ALL":
                before_fee_unit = self.available_cur
                expected_fee = before_fee_unit * self.trade_fee
                units_sell = math.floor((before_fee_unit - expected_fee) * (10**self.min_trade_cur_decimal))/(10**self.min_trade_cur_decimal)

            else:
                units_sell = round(float(units), self.min_trade_cur_decimal)

            rg_params = {
                "currency": self.currency,
                "units": units_sell
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

            return units_sell

        def record_orderbook(self, report=True):

            url_orderbook = urllib.request.urlopen(api_url + '/public/orderbook/' + self.currency)
            read_orderbook = url_orderbook.read()
            json_orderbook = json.loads(read_orderbook)

            orderbook = pd.DataFrame(columns={'Buy_Price', 'Buy_Quantity', 'Sell_Price', 'Sell_Quantity'})

            status = "OK" if json_orderbook['status'] == "0000" else "ERROR"

            print("==========[Record Orderbook]==========")
            print("Time  : " + str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
            print("Status: " + status)

            for i in range(len(json_orderbook["data"]["bids"])):
                buy_price = json_orderbook["data"]["bids"][i]["price"]
                buy_quantity = json_orderbook["data"]["bids"][i]["quantity"]
                sell_price = json_orderbook["data"]["asks"][i]["price"]
                sell_quantity = json_orderbook["data"]["asks"][i]["quantity"]

                orderbook = orderbook.append({'Buy_Price': buy_price,
                                              'Buy_Quantity': buy_quantity,
                                              'Sell_Price': sell_price,
                                              'Sell_Quantity': sell_quantity}, ignore_index=True)

            self.orderbook = orderbook

            if report:
                print(self.orderbook.head(10))
            return orderbook

        def run_trading(self):

            buy_limit = self.last_currency_price

            while True:
                self.recorder()
                if len(self.table) > 15:
                    bollinger_avg, bollinger_upper, bollinger_lower = bollinger_band(self.table,
                                                                                     window=15, std=2,
                                                                                     draw=False)

                    if self.last_currency_price > bollinger_upper.values[-1]:
                        if self.last_currency_price >= buy_limit:
                            _, status = self.sell_place()
                            if status == "OK":
                                buy_limit = bollinger_lower.values[-1] - 200
                                print("Set Buy Limit: " + str(buy_limit))

                    elif self.last_currency_price < bollinger_lower.values[-1]:
                        _, status = self.buy_place()
                        if status == "OK":
                            buy_limit = self.trader_buy_price * (self.trade_fee * self.trader_buy_units * 3 + 1) + 200
                            print("Set Buy Limit: " + str(buy_limit))

                time.sleep(10)


