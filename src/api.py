"""
Designed for IBKR single account
"""
import logging

from fastapi import FastAPI
from src.ibkr_client.ibkr_rest_client import IBKR_Rest_Client

import src.logging_settings
from src.config import IBKR_CASH_ACCOUNT_ID

logger = logging.getLogger(__name__)

app = FastAPI()
ibkr_rest_client = IBKR_Rest_Client()
active_strategies = []


@app.get("/portfolio/positions")
async def get_portfolio_positions():
    return ibkr_rest_client.get_portfolio_info()


@app.post("/portfolio/position")
async def get_portfolio_info():
    return ibkr_rest_client.get_portfolio_info()


@app.post("/orders/market")
async def place_market_order():
    return ibkr_rest_client.place_mkt_order()

# endpoint for seeing all available endpoints
@app.get("/")
async def list():
    return {"message": "Hello World"}

# endpoint for seeing all active strategies
@app.get("/strategies")
async def list():
    return {"message": "Hello World"}

# endpoint for starting a strategy
@app.post("/strategies")
async def list():
    return {"message": "Hello World"}

# endpoint for stopping a strategy
@app.delete("/strategies")
async def list():
    return {"message": "Hello World"}

