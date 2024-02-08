import utils.logging_settings

from config import FASTAPI_HOST, FASTAPI_LOG_LEVEL, FASTAPI_PORT, FASTAPI_ENV

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from routers.market_data_handler_router import marketDataRouter
from routers.storage_handler_router import storageRouter
from routers.strategy_handler_router import strategyRouter
from routers.trading_handler_router import tradingRouter

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(marketDataRouter, prefix="/market_data")
app.include_router(storageRouter, prefix="/storage")
app.include_router(strategyRouter, prefix="/strategy")
app.include_router(tradingRouter, prefix="/trading_accounts")


if __name__ == "__main__":
    if FASTAPI_ENV == "prod":
        uvicorn.run("api:app", port=FASTAPI_PORT, log_level=FASTAPI_LOG_LEVEL, reload=False, host=FASTAPI_HOST)
    elif FASTAPI_ENV == "dev":
        uvicorn.run("api:app", port=FASTAPI_PORT, log_level=FASTAPI_LOG_LEVEL, reload=True, host=FASTAPI_HOST)
