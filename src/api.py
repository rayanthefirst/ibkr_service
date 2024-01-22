import logging_settings

from strategy_handler.strategy_handler import StrategyHandler

from config import STORAGE_CLIENT

from storage_clients import STORAGE_CLIENTS
from trading_clients import TRADING_CLIENTS
from market_data_clients import MARKET_DATA_CLIENTS

from data_classes.portfolio import Portfolio
from data_classes.contract import Contract

from definitions.securities_definitions import TradableSecurity, OptionSide


from fastapi import FastAPI
import uvicorn

import logging
from decimal import Decimal

logger = logging.getLogger(__name__)
app = FastAPI()

from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

try:
    storage_client = STORAGE_CLIENTS[STORAGE_CLIENT]()
    strategy_handler = StrategyHandler(storage_client)

except Exception as e:
    logger.critical(e)
    raise e


@app.get("/trading_client/get_all_available_trading_clients")
async def get_all_available_trading_clients():
    return list(TRADING_CLIENTS.keys())


@app.get("/market_data_client/get_all_available_market_data_clients")
async def get_all_available_market_data_clients():
    return list(MARKET_DATA_CLIENTS.keys())


@app.get("/storage_client/get_all_available_storage_clients")
async def get_all_available_storage_clients():
    return list(STORAGE_CLIENTS.keys())


# Handler endpoints
@app.get("/strategy/available_strategies")
async def get_available_strategies():
    return strategy_handler.get_all_available_strategies()


@app.get("/strategy/signature/{strategy_name}")
async def get_strategy_signature(strategy_name: str):
    return strategy_handler.get_strategy_signature(strategy_name)


@app.get("/strategy/get_placed_strategies")
async def get_placed_strategies():
    return strategy_handler.get_placed_strategies()


@app.get("/strategy/start_strategy/{strategy_id}")
async def start_strategy(strategy_id: str):
    return strategy_handler.start_strategy(strategy_id)


@app.get("/strategy/stop_strategy/{strategy_id}")
async def stop_strategy(strategy_id: str):
    return strategy_handler.stop_strategy(strategy_id)


@app.post("/strategy/create_strategy/{strategy_name}")
async def create_strategy(strategy_name: str, strategy_params: dict):
    trading_client = TRADING_CLIENTS[strategy_params.get("trading_client")]()
    storage_client = STORAGE_CLIENTS[strategy_params.get("storage_client")]()
    market_data_client = MARKET_DATA_CLIENTS[
        strategy_params.get("market_data_client")
    ]()

    initialQuantity = (
        Decimal(strategy_params.get("initialQuantity"))
        if strategy_params.get("initialQuantity")
        else None
    )

    for security in TradableSecurity:
        if security.value == strategy_params.get("secType"):
            secType = security
            break

    strike = (
        Decimal(strategy_params.get("strike"))
        if strategy_params.get("strike")
        else None
    )

    for side in OptionSide:
        if side.value == strategy_params.get("right"):
            side = side

    initialContract = Contract(
        strategy_params.get("symbol"),
        secType,
        strike,
        strategy_params.get("expiryDate"),
        side,
    )

    cashBalance = (
        Decimal(strategy_params.get("cashBalance"))
        if strategy_params.get("cashBalance")
        else None
    )

    initialPortfolio = Portfolio(cashBalance=cashBalance)

    strategy_params["trading_client"] = trading_client
    strategy_params["storage_client"] = storage_client
    strategy_params["market_data_client"] = market_data_client
    strategy_params["initialQuantity"] = initialQuantity

    strategy_params["initialContract"] = initialContract
    strategy_params["initialPortfolio"] = initialPortfolio

    return strategy_handler.create_strategy(strategy_name, **strategy_params)


@app.delete("/strategy/delete_strategy/{strategy_id}")
async def delete_strategy(strategy_id: str):
    return strategy_handler.delete_strategy(strategy_id)


if __name__ == "__main__":
    uvicorn.run("api:app", port=80, log_level="info", reload=True)
