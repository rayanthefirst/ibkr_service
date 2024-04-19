# Test MongoDB connection
from clients.storage_clients import STORAGE_CLIENTS
from config import STORAGE_CLIENT

try:
    storage_client = STORAGE_CLIENTS[STORAGE_CLIENT]()
except Exception as e:
    logger.error(f"Error connecting to MongoDB: {e}")
    raise e
else:
    logger.info(f"Connected to MongoDB")
