import logging
from typing import List

from strategies import strategies
from strategies.base_strategy import BaseStrategy
from trading_clients.base_trading_client import BaseTradingClient
from market_data_clients.base_market_data_client import BaseMarketDataClient
from storage_clients.base_storage_client import BaseStorageClient

logger = logging.getLogger(__name__)


class StrategyHandler:
    def __init__(
        self,
        trading_client: BaseTradingClient,
        market_data_client: BaseMarketDataClient,
        storage_client: BaseStorageClient,
    ):
        self.trading_client = trading_client
        self.market_data_client = market_data_client
        self.storage_client = storage_client
        self.strategies: List[BaseStrategy] = []
        self.load_strategies()

    def load_strategies(self):
        """Load all strategies from storage client"""
        logger.info("Loading strategies from storage client")
        self.strategies = self.storage_client.get_all_strategies()

    def get_strategy(self, strategy_id):
        for strategy in self.strategies:
            if strategy.strategy_id == strategy_id:
                return strategy

    def get_running_strategies(self):
        return [strategy for strategy in self.strategies if strategy.is_running]

    def create_strategy(self, strategy_name, **kwargs):
        strategy = strategies[strategy_name](**kwargs)
        self.strategies.append(strategy)
        return strategy.strategy_id

    def delete_strategy(self, strategy_id):
        strategy = self.get_strategy(strategy_id)
        self.strategies.remove(strategy)
        self.storage_client.delete_strategy(strategy_id)

    def start_strategy(self, strategy_id):
        strategy = self.get_strategy(strategy_id)
        strategy.start()

    def stop_strategy(self, strategy_id):
        strategy = self.get_strategy(strategy_id)
        strategy.stop()
