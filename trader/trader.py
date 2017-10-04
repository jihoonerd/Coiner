# -*- coding: utf-8 -*-
"""
Created on 10/3/17
Author: Jihoon Kim
"""

import datetime
import pandas as pd
import time
from account_info import api_key, api_secret
from api.xcoin_api_client import XCoinAPI


class Trader(XCoinAPI):

        def __init__(self, currency='ETH', trade_algorithm=None):

            super(Trader, self).__init__(api_key=api_key, api_secret=api_secret)
            self.currency = currency
            self.trade_algorithm = trade_algorithm
            self.table = pd.DataFrame(columns={'Time', 'Price'})
            self.currency_current_value = None
            self.available_eth = None
            self.available_krw = None
            self.trade_fee = None

            self.set_trade_fee()
            self.update_wallet()

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

        def recorder(self, report=True):

            """
            Records time and price of given currency in Pandas format.

            :return: DataFrame of time and price
            :rtype: pd.DataFrame
            """

            rg_params = {
                "currency": self.currency
            }
            response_recorder = self.xcoinApiCall("/public/ticker/" + self.currency, rg_params)
            status = "OK" if response_recorder["status"] == "0000" else "ERROR"
            current_price = response_recorder["data"]["closing_price"]
            time = str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

            if report:
                print("=============[Price Record]=============")
                print("Status: " + status)
                print("Time  : " + time)
                print("Index : " + str(len(self.table)))
                print("{0:6s}: ".format(self.currency) + current_price)

            time = pd.to_datetime(time, format="%Y-%m-%d %H:%M:%S")
            current_price = float(response_recorder["data"]["closing_price"])
            self.currency_current_value = current_price

            new_data = {"Time": time, "Price": current_price}
            self.table = self.table.append(new_data, ignore_index=True)

            return self.table

        def update_wallet(self, report=True):

            rg_params = {
                "currency": self.currency,
            }

            response_update_wallet = self.xcoinApiCall("/info/balance", rg_params)
            status = "OK" if response_update_wallet["status"] == "0000" else "ERROR"
            self.available_eth = float(response_update_wallet["data"]["available_" + self.currency.lower()])
            self.available_krw = float(response_update_wallet["data"]["available_krw"])

            if report:
                print("============[Wallet Update]============")
                print("Status: " + status)
                print("Available " + self.currency + ": " + str(response_update_wallet["data"]["available_" + self.currency.lower()]))
                print("Available KRW: " + str(response_update_wallet["data"]["available_krw"]))

            return None

        def buy(self, units="ALL"):

            self.recorder(report=False)

            if units == "ALL":
                before_fee_unit = self.available_krw / self.currency_current_value
                expected_fee = before_fee_unit * self.trade_fee
                units_buy = round(before_fee_unit - expected_fee, 4)

            else:
                units_buy = round(float(units), 4)

            rg_params = {
                "currency": self.currency,
                "units": units_buy
            }

            response_buy = self.xcoinApiCall("/trade/market_buy", rg_params)
            status = "OK" if response_buy["status"] == "0000" else "ERROR"

            if status == "OK":
                print("===============[BUY]===============")
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

            return None
