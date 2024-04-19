from fastapi import APIRouter, HTTPException
# from handlers.account_client_handler import AccountClientHandler


# account_handler = AccountClientHandler()

from Enums.account_definitions import AccountType

accountRouter = APIRouter()


"""
Manage Account Clienrts
Account Info
Place Strategy
- Get all user accounts for user
- Get 
"""
# @accountRouter.get

# @accountRouter.get("/get_trading_client_types")
# async def get_trading_client_types():
#     return account_handler.get_trading_client_types()

# @accountRouter.get("/get_account_type")
# async def get_account_type():
#     return [accountType.value for accountType in AccountType]

# @accountRouter.get("/get_client_signature")
# async def get_trading_client_signature(trading_client_name: str):
#     return account_handler.get_trading_client_signature(trading_client_name)

# @accountRouter.get("/get_clients")
# async def get_placed_trading_clients():
#     return account_handler.get_trading_clients()

# @accountRouter.post("/create")
# async def create_trading_client(kwargs: dict):

#     for accountType in AccountType:
#         if accountType.value == kwargs.get("account_type"):
#             kwargs["account_type"] = accountType

#     account_handler.create_trading_client(**kwargs)
#     return "Created trading client successfully"

# @accountRouter.get("/start")
# async def start_trading_client(trading_client_id: str):
#     account_handler.start_trading_client(trading_client_id)
#     return "Successfully started trading client"

# @accountRouter.get("/stop")
# async def stop_trading_client(trading_client_id: str):
#     account_handler.stop_trading_client(trading_client_id)
#     return "Successfully stopped trading client"


# @accountRouter.delete("/delete")
# async def delete_trading_client(trading_client_id: str):
#     if not trading_client_id: raise HTTPException(400, detail="Trading Client ID Not Found")
#     account_handler.delete_trading_client(trading_client_id)
#     return "Successfully deleted trading client"
