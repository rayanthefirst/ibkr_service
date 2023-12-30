"""
Designed for IBKR single account
"""
import logging

from fastapi import FastAPI, Body
from src.trading_clients.ibkr_rest_client import IBKR_Rest_Client
from decimal import Decimal

import src.logging_settings
from src.config import IBKR_CASH_ACCOUNT_ID

logger = logging.getLogger(__name__)

app = FastAPI()
ibkr_rest_client = IBKR_Rest_Client()
active_strategies = []


@app.get("/portfolio/info")
async def get_portfolio_info():
    logger.info(ibkr_rest_client.get_portfolio_info())
    # return


@app.post("/orders/market")
async def place_market_order(
    quantity: Decimal = Body(...),
    action: str = Body(...),
    timeInForce: str = Body(...),
    symbol: str = Body(...),
    secType: str = Body(...),
    expiryDate: str = Body(None),
    strike: Decimal = Body(None),
    right: str = Body(None),
):
    return ibkr_rest_client.place_mkt_order(
        quantity, action, timeInForce, symbol, secType, expiryDate, strike, right
    )


@app.post("/orders/trail")
async def place_trail_order(
    quantity: Decimal = Body(...),
    action: str = Body(...),
    timeInForce: str = Body(...),
    trlAmtOrPrc: Decimal = Body(...),
    trlType: str = Body(...),
    symbol: str = Body(...),
    secType: str = Body(...),
    expiryDate: str = Body(None),
    strike: Decimal = Body(None),
    right: str = Body(None),
):
    return ibkr_rest_client.place_trail_order(
        quantity,
        action,
        timeInForce,
        trlAmtOrPrc,
        trlType,
        symbol,
        secType,
        expiryDate,
        strike,
        right,
    )


@app.post("/instrument/conid")
async def get_instrument_conid(
    symbol: str = Body(...),
    secType: str = Body(...),
    expiryDate: str = Body(None),
    strike: Decimal = Body(None),
    right: str = Body(None),
):
    return ibkr_rest_client.get_instrument_conid(
        symbol, secType, expiryDate, strike, right
    )


@app.get("/orders/live")
async def get_live_orders():
    return ibkr_rest_client.get_live_orders()


@app.get("/order/status/{orderId}")
async def get_order_status(orderId: int):
    return ibkr_rest_client.get_order_status(orderId)


@app.delete("/order/{orderId}")
async def cancel_order(orderId: int):
    return ibkr_rest_client.cancel_order(orderId)


@app.get("/")
async def get_active_strategies():
    return ibkr_rest_client.get_portfolio_info()
