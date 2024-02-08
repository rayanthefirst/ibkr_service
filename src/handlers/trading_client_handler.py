import logging
from typing import List

import docker
from cryptography.fernet import Fernet

from config import KEY_BYTES

from trading_clients import TRADING_CLIENTS
from trading_clients.ibkr_rest_client.ibkr_rest_client import IBKRRestClient
from trading_clients.base_trading_client import BaseTradingClient
from storage_clients.base_storage_client import BaseStorageClient

from definitions.trading_client_definitions import AccountStatus

logger = logging.getLogger(__name__)

class TradingClientHandler:
    def __init__(self, storage_client: BaseStorageClient) -> None:
        logger.info("Initializing trading client handler")
        self.storage_client = storage_client
        self.trading_clients: List[BaseTradingClient] = []
        self.dockerClient = docker.DockerClient()
        self.encrpytionClient = Fernet(KEY_BYTES)
        
        self.load_trading_clients()

    def load_trading_clients(self):
        for container in self.dockerClient.containers.list(all=True, filters={"name":"trading_client_*"}):
            container.stop()
            container.remove()

        for account in self.storage_client.get_all_accounts():
            trading_client = TRADING_CLIENTS[account["trading_client_name"]](**account)
            if account["account_status"] == AccountStatus.ACTIVE.value:
                trading_client.connect()

            self.trading_clients.append(trading_client)        
            

    def get_trading_client_types(self):
        return list(TRADING_CLIENTS.keys())
    
    def get_trading_clients(self):
        return [
            {
                "trading_client_id": trading_client.trading_client_id,
                "trading_client_account_type": trading_client.account_type.value,
                "trading_client_status": AccountStatus.ACTIVE.value if trading_client.is_running else AccountStatus.INACTIVE.value
            } for trading_client in self.trading_clients
        ]

    def start_trading_client(self, trading_client_id):
        trading_client = self.get_trading_client(trading_client_id)
        trading_client.connect()

    def stop_trading_client(self, trading_client_id):
        trading_client = self.get_trading_client(trading_client_id)
        trading_client.disconnect()
        

    def create_trading_client(self, trading_client_name: str, **kwargs):
        trading_client = TRADING_CLIENTS[trading_client_name](**kwargs)
        trading_client_container = self.create_trading_client_container()

    
    def delete_trading_client(self, trading_client_name: str):
        ...

    def get_trading_client(self, trading_client_id: str):
        for trading_client in self.trading_clients:
            if trading_client.trading_client_id == trading_client_id:
                return trading_client



    