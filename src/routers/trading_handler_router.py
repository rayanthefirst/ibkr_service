from fastapi import APIRouter

from handlers.trading_client_handler import TradingClientHandler
from handlers.storage_client_handler import StorageClientHandler


tradingRouter = APIRouter()

storage_client_handler = StorageClientHandler()
default_storage_client = storage_client_handler.get_default_storage_client()


trading_client_handler = TradingClientHandler(default_storage_client)


@tradingRouter.get("/get_trading_client_types")
async def get_trading_client_types():
    return trading_client_handler.get_trading_client_types()
