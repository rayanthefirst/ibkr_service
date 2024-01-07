from abc import ABC, abstractmethod
from trading_clients.base_trading_client import BaseTradingClient
from storage_clients.base_storage_client import BaseStorageClient
from market_data_clients.base_market_data_client import BaseMarketDataClient

from data_classes.contract import Contract
from data_classes.portfolio import Portfolio

from decimal import Decimal


class BaseStrategy(ABC):
    """
    Abstract base class for trading strategies
    Strategy specific functions will be implemented in the derived class
    """

    _last_id = 0
    name = "BaseStrategy"

    def __init__(
        self,
        trading_client: BaseTradingClient,
        storage_client: BaseStorageClient,
        market_data_client: BaseMarketDataClient,
        initialQuantity: Decimal = None,
        initialContract: Contract = None,
        initialPortfolio: Portfolio = None,
    ):
        self.trading_client = trading_client
        self.storage_client = storage_client
        self.market_data_client = market_data_client

        self.quantity = initialQuantity
        self.contract = initialContract
        self.portfolio = initialPortfolio

        self.strategy_id = BaseStrategy._get_next_id()
        self.is_running = False
        self.lastFilledOrder = None

    @staticmethod
    def _get_next_id():
        BaseStrategy._last_id += 1
        return BaseStrategy._last_id

    @abstractmethod
    def start(self):
        self.is_running = True
        # Implement your strategy logic here

    @abstractmethod
    def stop(self):
        self.is_running = False
        # Implement any cleanup logic here

    @abstractmethod
    def get_strategy_info(self):
        # Implement logic to retrieve trade information
        pass

    @abstractmethod
    def get_new_quantity(self):
        pass

    @abstractmethod
    def get_new_contract(self):
        pass

    @abstractmethod
    def get_new_portfolio(self):
        pass
