import logging
import time

from storage_clients.base_storage_client import BaseStorageClient
from pymongo.mongo_client import MongoClient as MG
from definitions.order_definitions import OrderState, OrderAction
from data_classes.contract import Contract

from storage_clients.storage_exceptions import (
    StorageConnectionError,
    StorageWriteError,
    StorageReadError,
    StorageUpdateError,
)

from config import (
    MONGO_USERNAME,
    MONGO_PASSWORD,
    MONGO_CLUSTER,
    MONGO_DATABASE,
    MONGO_DATABASE_COLLECTION,
    MONGO_DATABASE_COLLECTION_STRATEGY_DATA,
    SLEEP_SECONDS,
    RETRY_COUNT,
)

logger = logging.getLogger(__name__)


class MongoClient(BaseStorageClient):
    name = "MongoClient"

    def __init__(self):
        self.connect()

    def connect(self):
        # Connect to the Mongo database
        logger.info("Connecting to Mongo database")
        count = 0
        while True:
            try:
                uri = f"mongodb+srv://{MONGO_USERNAME}:{MONGO_PASSWORD}@{MONGO_CLUSTER}.nlwwpjk.mongodb.net/?retryWrites=true&w=majority"
                self.client = MG(uri)
                self.client.admin.command("ping")

                self.db = self.client[MONGO_DATABASE]
                self.collection = self.db[MONGO_DATABASE_COLLECTION]
                self.strategyCollection = self.db[
                    MONGO_DATABASE_COLLECTION_STRATEGY_DATA
                ]

            except Exception:
                logger.error(f"Error connecting to storage client: {self.name}")
                time.sleep(SLEEP_SECONDS)
                count += 1

            else:
                logger.info("Connected to Mongo database successfully")
                break

            if count == RETRY_COUNT:
                logger.critical(
                    f"Critical error connecting to storage client: {self.name}"
                )
                raise StorageConnectionError

    def disconnect(self):
        # Disconnect from the Mongo database
        pass

    def write(self, collection, **data):
        # Write data to the Mongo database
        count = 0
        while True:
            try:
                collection.insert_one(data)

            except Exception:
                logger.error("Error writing to Mongo database")
                time.sleep(SLEEP_SECONDS)
                count += 1

            else:
                logger.debug("Data written to Mongo database successfully")
                break

            if count == RETRY_COUNT:
                logger.critical("Critical error writing to Mongo database")
                raise StorageWriteError

    def read(self, collection, **data):
        # Read data from the Mongo database
        count = 0
        while True:
            try:
                resultData = collection.find(data)

            except Exception:
                logger.error("Error reading from Mongo database")
                time.sleep(SLEEP_SECONDS)
                count += 1

            else:
                logger.debug("Data read from Mongo database successfully")
                return resultData

            if count == RETRY_COUNT:
                logger.critical("Error reading from Mongo database")
                raise StorageReadError

    def write_order(
        self,
        strategy_id,
        order_id,
        contract: Contract,
        quantity,
        action: OrderAction,
        executedPrice,
        lastExecutedTime: int,
        orderState: OrderState,
        **kwargs,
    ):
        # Save the order to the database, lastExecutedTime is UTC timestamp in ms
        self.write(
            self.collection,
            strategy_id=strategy_id,
            order_id=order_id,
            contract={
                "symbol": contract.symbol,
                "secType": contract.secType.value,
                "strike": contract.strike,
                "expiryDate": contract.expiryDate,
                "right": contract.right.value if contract.right else None,
            },
            quantity=quantity,
            action=action.value,
            executedPrice=executedPrice,
            lastExecutedTime=lastExecutedTime,
            orderState=orderState.value,
            **kwargs,
        )

    def update_order_state(self, strategy_id, order_id, newOrderState: OrderState):
        # Update the order state in the database
        count = 0
        while True:
            try:
                self.collection.update_one(
                    {"strategy_id": strategy_id, "order_id": order_id},
                    {"$set": {"orderState": newOrderState.value}},
                )

            except Exception:
                logger.error("Error updating order state in Mongo database")
                time.sleep(SLEEP_SECONDS)
                count += 1

            else:
                logger.debug("Order state updated in Mongo database successfully")
                break

            if count == RETRY_COUNT:
                logger.critical("Critical error updating order state in Mongo database")
                raise StorageUpdateError

    def check_for_active_orders(self, strategy_id):
        return list(
            self.read(
                self.collection,
                strategy_id=strategy_id,
                orderState=OrderState.SUBMITTED.value,
            )
        )

    def get_all_strategies(self):
        return list(self.read(self.strategyCollection))

    def write_strategy(self, strategy_id, strategy_name, strategy_status, **kwargs):
        self.write(
            self.strategyCollection,
            strategy_id=strategy_id,
            strategy_name=strategy_name,
            strategy_status=strategy_status,
            **kwargs,
        )
