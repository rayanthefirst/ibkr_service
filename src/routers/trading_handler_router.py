from fastapi import APIRouter

from handlers.trading_client_handler import TradingClientHandler
from handlers.storage_client_handler import StorageClientHandler

from definitions.trading_client_definitions import AccountType

tradingRouter = APIRouter()

storage_client_handler = StorageClientHandler()
default_storage_client = storage_client_handler.get_default_storage_client()


trading_client_handler = TradingClientHandler(default_storage_client)


@tradingRouter.get("/get_trading_client_types")
async def get_trading_client_types():
    return trading_client_handler.get_trading_client_types()

@tradingRouter.get("/get_account_type")
async def get_account_type():
    return [accountType.value for accountType in AccountType]

@tradingRouter.get("/get_trading_client_signature")
async def get_trading_client_signature(trading_client_name: str):
    return trading_client_handler.get_trading_client_signature(trading_client_name)

@tradingRouter.get("/get_placed_trading_clients")
async def get_placed_trading_clients():
    return trading_client_handler.get_trading_clients()

@tradingRouter.post("/create_trading_client")
async def create_trading_client(kwargs: dict):

    for accountType in AccountType:
        if accountType.value == kwargs.get("account_type"):
            kwargs["account_type"] = accountType

    trading_client_handler.create_trading_client(**kwargs)

