from fastapi import APIRouter

marketDataRouter = APIRouter()

from handlers.market_data_handler import MarketDataHandler

market_data_handler = MarketDataHandler()

@marketDataRouter.get("/get_market_data_client_types")
async def get_market_data_client_types():
    return market_data_handler.get_market_data_client_types()