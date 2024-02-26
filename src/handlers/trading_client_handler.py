import logging
from typing import List
import inspect

import docker

from utils.cipher import encrypt_str, decrypt_str

from trading_clients import TRADING_CLIENTS
from trading_clients.base_trading_client import BaseTradingClient
from storage_clients.base_storage_client import BaseStorageClient

from definitions.trading_client_definitions import AccountStatus, AccountType

logger = logging.getLogger(__name__)

class TradingClientHandler:
    def __init__(self, storage_client: BaseStorageClient) -> None:
        logger.info("Initializing trading client handler")
        self.storage_client = storage_client
        self.trading_clients: List[BaseTradingClient] = []
        self.dockerClient = docker.DockerClient()
        
        self.load_trading_clients()

    def load_trading_clients(self):
        for container in self.dockerClient.containers.list(all=True, filters={"name":"trading_client_*"}):
            container.stop()
            container.remove()

        for account in self.storage_client.get_all_accounts():
            for accountType in AccountType:
                if accountType.value == account.get("account_type"):
                    account["account_type"] = accountType

        
            account["user"] = decrypt_str(account["user"])
            account["password"] = decrypt_str(account["password"])
            # account["ibkrAccountId"] = decrypt_str(account.get("ibkrAccountId", "Not Provided"))
            trading_client = TRADING_CLIENTS[account["trading_client_name"]](**account)

            self.trading_clients.append(trading_client)        
            

    def get_trading_client_types(self):
        return list(TRADING_CLIENTS.keys())
    
    def get_trading_client_signature(self, trading_client_name):
        signature = inspect.signature(TRADING_CLIENTS[trading_client_name])
        param_names = [param.name for param in signature.parameters.values()]
        return param_names
        
    
    def get_trading_clients(self):
        return [
            {   "trading_client_account_user": encrypt_str(trading_client.user),
                "trading_client_type": trading_client.name,
                "trading_client_id": trading_client.trading_client_id,
                "trading_client_account_type": trading_client.account_type.value,
                # "ibkrAccountId": trading_client.accountId if trading_client.accountId == None else encrypt_str(trading_client.accountId),
                "status": self.get_trading_client_status(trading_client.trading_client_id)
            } for trading_client in self.trading_clients
        ]

    def start_trading_client(self, trading_client_id):
        trading_client = self.get_trading_client(trading_client_id)
        trading_client.connect()

    def stop_trading_client(self, trading_client_id):
        trading_client = self.get_trading_client(trading_client_id)
        trading_client.disconnect()
        

    def create_trading_client(self, trading_client_name: str, **kwargs):
        encryptedUser = kwargs.get("user")
        encryptedPassword = kwargs.get("password")

        kwargs["user"] = decrypt_str(kwargs.get("user"))
        kwargs["password"] = decrypt_str(kwargs.get("password"))

        trading_client = TRADING_CLIENTS[trading_client_name](**kwargs)
        self.trading_clients.append(trading_client)

        kwargs["user"] = encryptedUser
        kwargs["password"] = encryptedPassword

        self.storage_client.write_account(trading_client_name,
                                        trading_client.account_type.value,
                                          trading_client.trading_client_id,
                                          **{key:value for key, value in kwargs.items() if type(key) == str and type(value) == str}),
    
    
    def delete_trading_client(self, trading_client_id: str):
        trading_client = self.get_trading_client(trading_client_id)
        trading_client.disconnect()
        trading_client.container.remove()
        self.trading_clients.remove(trading_client)
        self.storage_client.remove_account(trading_client.trading_client_id)

    def get_trading_client_status(self, trading_client_id: str):
        trading_client = self.get_trading_client(trading_client_id)
        return trading_client.get_status()

    def get_trading_client(self, trading_client_id: str):
        for trading_client in self.trading_clients:
            if trading_client.trading_client_id == trading_client_id:
                return trading_client



    