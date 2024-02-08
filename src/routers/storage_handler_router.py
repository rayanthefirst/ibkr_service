from fastapi import APIRouter

storageRouter = APIRouter()

from handlers.storage_client_handler import StorageClientHandler


storage_client_handler = StorageClientHandler()

@storageRouter.get("/get_storage_client_types")
async def get_storage_client_types():
    return storage_client_handler.get_storage_client_types()
