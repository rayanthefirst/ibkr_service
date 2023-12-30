from storage_clients.base_storage_client import BaseStorageClient
from pymongo.mongo_client import MongoClient as MG
from enum_definitions.order_definitions import OrderState

from config import (
    MONGO_USERNAME,
    MONGO_PASSWORD,
    MONGO_CLUSTER,
    MONGO_DATABASE,
    MONGO_DATABASE_COLLECTION,
)


class MongoClient(BaseStorageClient):
    def __init__(self):
        self.connect()

    def connect(self):
        # Connect to the Mongo database
        uri = f"mongodb+srv://{MONGO_USERNAME}:{MONGO_PASSWORD}@{MONGO_CLUSTER}.nlwwpjk.mongodb.net/?retryWrites=true&w=majority"
        self.client = MG(uri)
        self.db = self.client[MONGO_DATABASE]
        self.collection = self.db[MONGO_DATABASE_COLLECTION]

    def disconnect(self):
        # Disconnect from the Mongo database
        pass

    def write(self, **data):
        # Write data to the Mongo database
        self.collection.insert_one(data)

    def read(self, **data):
        # Read data from the Mongo database
        return self.collection.find(data)

    def write_order(
        self,
        strategy_id,
        strategy_name,
        contract,
        quantity,
        side,
        executedPrice,
        executedTime,
        orderState,
    ):
        # Save the order to the database
        self.write(
            strategy_id=strategy_id,
            strategy_name=strategy_name,
            contract=contract,
            quantity=quantity,
            side=side,
            executedPrice=executedPrice,
            executedTime=executedTime,
            orderState=orderState,
        )

    def check_for_active_order(self, strategy_id):
        return list(
            self.read(strategy_id=strategy_id, orderState=OrderState.SUBMITTED.value)
        )

    # def update_order(self, strategy_id, orderState):
    #     self.collection.update_one({"strategy_id": strategy_id}, {"$set": {"orderState": orderState}}
