from fastapi import APIRouter

from routers.market_data_handler_router import marketDataRouter
from routers.storage_handler_router import storageRouter
from routers.strategy_handler_router import strategyRouter
from routers.trading_handler_router import tradingRouter


mainRouter = APIRouter()


mainRouter.include_router(strategyRouter, prefix="/strategy")
mainRouter.include_router(tradingRouter, prefix="/trading_accounts")
mainRouter.include_router(marketDataRouter, prefix="/market_data")
mainRouter.include_router(storageRouter, prefix="/storage")
