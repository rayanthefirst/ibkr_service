from fastapi import APIRouter, HTTPException
from config import trading_client_handler


from definitions.trading_client_definitions import AccountType

tradingRouter = APIRouter()

@tradingRouter.get("/get_trading_client_types")
async def get_trading_client_types():
    return trading_client_handler.get_trading_client_types()

@tradingRouter.get("/get_account_type")
async def get_account_type():
    return [accountType.value for accountType in AccountType]

@tradingRouter.get("/get_client_signature")
async def get_trading_client_signature(trading_client_name: str):
    return trading_client_handler.get_trading_client_signature(trading_client_name)

@tradingRouter.get("/get_clients")
async def get_placed_trading_clients():
    return trading_client_handler.get_trading_clients()

@tradingRouter.post("/create")
async def create_trading_client(kwargs: dict):

    for accountType in AccountType:
        if accountType.value == kwargs.get("account_type"):
            kwargs["account_type"] = accountType

    trading_client_handler.create_trading_client(**kwargs)
    return "Created trading client successfully"

@tradingRouter.get("/start")
async def start_trading_client(trading_client_id: str):
    trading_client_handler.start_trading_client(trading_client_id)
    return "Successfully started trading client"

@tradingRouter.get("/stop")
async def stop_trading_client(trading_client_id: str):
    trading_client_handler.stop_trading_client(trading_client_id)
    return "Successfully stopped trading client"


@tradingRouter.delete("/delete")
async def delete_trading_client(trading_client_id: str):
    if not trading_client_id: raise HTTPException(400, detail="Trading Client ID Not Found")
    trading_client_handler.delete_trading_client(trading_client_id)
    return "Successfully deleted trading client"
