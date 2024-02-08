# from trading_clients.ibkr_rest_client.ibkr_rest_client import IBKRRestClient
# from storage_clients.mongo_client import MongoClient
# from data_classes.contract import Contract

# from data_classes.portfolio import Portfolio
# from definitions.order_definitions import *
# from definitions.securities_definitions import *
# from utils.date_functions import format_date
# from dataclasses import asdict
# import time

# from definitions.securities_definitions import TradableSecurity, OptionSide
# from strategies.trailing_strategies.long_short_buy_sell_trail import (
#     LongShortBuySellTrail,
# )
# import logging_settings

# from strategy_handler.strategy_handler import StrategyHandler


# ibkr_client = IBKRRestClient()
# # ibkr_client.get_live_orders()
# mongo = MongoClient()
# # print(mongo.get_all_strategies())
# # mock_market_data = []
# strategyhand = StrategyHandler(ibkr_client, None, mongo)

# # contract = Contract(
# #     **{
# #         "symbol": "aapl",
# #         "secType": TradableSecurity.STOCK,
# #         # "strike": 197.5,
# #         # "expiryDate": format_date(2024, 1, 5),
# #         # "right": OptionSide.CALL,
# #     }
# # )


# # portfolio = Portfolio(1000, "USD")


# # strategy = LongShortBuySellTrail(
# #     ibkr_client,
# #     mongo,
# #     mock_market_data,
# #     1,
# #     contract,
# #     portfolio,
# #     3,
# #     TrailingStopType.PERCENTAGE,
# # )

# # strategy.start()


# # print(
# #     mongo.write_order(
# #         1,
# #         2,
# #         "testName",
# #         contract,
# #         1,
# #         OrderAction.BUY,
# #         100,
# #         time.time(),
# #         OrderState.SUBMITTED,
# #         trlAmtOrPrc=1,
# #         trlType=TrailingStopType.PERCENTAGE.value,
# #     )
# # )

# # orders = mongo.check_for_active_orders(1)
# # print(orders)

# # order = ibkr_client.place_market_order(
# #     100,
# #     OrderAction.BUY,
# #     OrderTIF.GOOD_TILL_CANCELLED,
# #     "AAPL",
# #     TradableSecurity.STOCK,
# # format_date(2024, 1, 5),
# # 197.5,
# # OptionSide.CALL,
# # )
# # order = ibkr_client.place_trail_order(
# #     1,
# #     OrderAction.BUY,
# #     OrderTIF.GOOD_TILL_CANCELLED,
# #     1,
# #     TrailingStopType.PERCENTAGE,
# #     "AAPL",
# #     TradableSecurity.OPTION,
# #     format_date(2024, 1, 5),
# #     197.5,
# #     OptionSide.CALL,
# # )

# # print(order)

# # while True:
# #     # print(ibkr_client.get_live_orders())
# #     # time.sleep(1)
# #     status = ibkr_client.get_order_status(order)
# #     print(status)
# #     time.sleep(1)
# # mongo.write_strategy(1, "testName", "Running")
# # mongo.write_strategy(2, "testName", "Running")
# # mongo.write_strategy(3, "testName", "Running")

# # print(strategyhand.strategies)
# import pickle

# strategy = LongShortBuySellTrail(ibkr_client, mongo, None)
# # strategy.start()
# dump = pickle.dumps(strategy)
# print(dump)

# from handlers.market_data_handler import MarketDataHandler

# market_data_handler = MarketDataHandler()

# print(MarketDataHandler.array)

# MarketDataHandler.array.append(1)

# print(MarketDataHandler.array)

# print(market_data_handler.array)

# market_data_handler.array.append(2)

# print(MarketDataHandler.array)


import docker

client = docker.DockerClient()
# cont = client.containers.list(all=True, filters={"name": "cool_*"})
# print(cont)
# for c in cont: 
#     print(c.name)
client.containers.create(image="voyz/ibeam", detach=True, environment={"IBEAM_ACCOUNT": "aibapi002", "IBEAM_PASSWORD": "layla1966"}, name="testCreate")

# print(client.containers.list(all=True))


# from trading_clients.ibkr_rest_client.ibkr_rest_client import IBKRRestClient

# ibkr_client = IBKRRestClient()
# print(ibkr_client.dockerClient.images.list()[0])



# from cryptography.fernet import Fernet
# key = Fernet.generate_key()
# print(key)
# print(key.decode('utf-8'))
# print(key.decode('utf-8').encode('utf-8'))

# f = Fernet(key)
# password = f.encrypt(b"your_ibkr_password123")
# print(f'IBEAM_PASSWORD={password}, IBEAM_KEY={key}')

# print(type((f.decrypt(password)).decode('utf-8')))


