from storage_clients.mongo_client import MongoClient
from enum_definitions.order_definitions import OrderState
from strategies.stock_strategies import longBuySellTrail, short

hi = longBuySellTrail(None, None, None)
print(hi.strategy_id)
bye = short(None, None, None)
print(bye.strategy_id)
# test = MongoClient()


# test.write_order(
#     "test3",
#     "testhi",
#     {"test": "test"},
#     "testnjsd",
#     "test",
#     "test",
#     "test",
#     OrderState.SUBMITTED.value,
# )


# find = test.check_for_active_order("test3")
# print(find)
