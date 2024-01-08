import logging_settings

from strategy_handler.strategy_handler import StrategyHandler

from strategies import strategies
from config import TRADING_CLIENT, MARKET_DATA_CLIENT, STORAGE_CLIENT

from trading_clients import TRADING_CLIENTS
from market_data_clients import MARKET_DATA_CLIENTS
from storage_clients import STORAGE_CLIENTS

from fastapi import FastAPI
import uvicorn

import logging
import inspect
from decimal import Decimal


from data_classes.contract import Contract

logger = logging.getLogger(__name__)
app = FastAPI()

trading_client = TRADING_CLIENTS[TRADING_CLIENT]()
# market_data_client = MARKET_DATA_CLIENTS[MARKET_DATA_CLIENT]()
storage_client = STORAGE_CLIENTS[STORAGE_CLIENT]()
strategy_handler = StrategyHandler(trading_client, None, storage_client)


@app.get("/strategy/strategies")
def get_strategies():
    return [strategy.name for strategy in strategies.values()]


@app.get("/strategy/signature/{strategy_name}")
def get_strategy_signature(strategy_name: str):
    signature = inspect.signature(strategies[strategy_name])
    param_names = [param.name for param in signature.parameters.values()]
    return param_names


@app.post("/strategy/place_order/{strategy_name}")
def place_strategy(strategy_name: str, strategy_params: dict):
    # strategy = strategy_handler.create_strategy(strategy_name, **kwargs)
    print(strategy_name)
    print(strategy_params)
    con = Contract(**strategy_params["initialContract"])
    print(con)


if __name__ == "__main__":
    uvicorn.run("api:app", port=80, log_level="info", reload=True)
