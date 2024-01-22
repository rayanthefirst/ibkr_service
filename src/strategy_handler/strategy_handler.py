import logging
import inspect
from typing import List

from definitions.strategy_definitions import StrategyStatus

from strategies import strategies
from trading_clients import TRADING_CLIENTS
from market_data_clients import MARKET_DATA_CLIENTS
from storage_clients import STORAGE_CLIENTS

from config import TRADING_CLIENT, MARKET_DATA_CLIENT, STORAGE_CLIENT


from strategies.base_strategy import BaseStrategy
from trading_clients.base_trading_client import BaseTradingClient
from market_data_clients.base_market_data_client import BaseMarketDataClient
from storage_clients.base_storage_client import BaseStorageClient

logger = logging.getLogger(__name__)


class StrategyHandler:
    def __init__(
        self,
        storage_client: BaseStorageClient,
    ):
        self.storage_client = storage_client
        self.strategies: List[BaseStrategy] = []
        self.load_strategies()

    def load_strategies(self):
        """Load all strategies from storage client"""
        logger.info("Loading strategies from storage client")

        for strategy in self.storage_client.get_all_strategies():
            strategy["trading_client"] = TRADING_CLIENTS[TRADING_CLIENT]()
            strategy["market_data_client"] = MARKET_DATA_CLIENTS[MARKET_DATA_CLIENT]()
            strategy["storage_client"] = STORAGE_CLIENTS[STORAGE_CLIENT]()
            strategy: BaseStrategy = strategies[strategy["strategy_name"]](**strategy)
            self.strategies.append(strategy)

    def get_all_available_strategies(self):
        return list(strategies.keys())

    def get_placed_strategies(self):
        return [
            {
                "strategy_id": strategy.strategy_id,
                "strategy_name": strategy.name,
                "strategy_status": StrategyStatus.ACTIVE.value
                if strategy.is_running
                else StrategyStatus.INACTIVE.value,
            }
            for strategy in self.strategies
        ]

    def get_strategy_signature(self, strategy_name: str):
        signature = inspect.signature(strategies[strategy_name])
        param_names = [param.name for param in signature.parameters.values()]
        return param_names

    def start_strategy(self, strategy_id):
        strategy = self.get_strategy(strategy_id)
        if strategy == None:
            logger.error("Strategy not found")
            return f"Strategy {strategy_id} not found"
        elif strategy.is_running:
            logger.error("Strategy is already running")
            return f"Strategy {strategy_id} is already running"
        strategy.start()
        self.storage_client.update_strategy_status(strategy_id, StrategyStatus.ACTIVE)
        return f"Strategy {strategy_id} started"

    def stop_strategy(self, strategy_id):
        strategy = self.get_strategy(strategy_id)
        if strategy == None:
            logger.error("Strategy not found")
            return f"Strategy {strategy_id} not found"
        elif not strategy.is_running:
            logger.error("Strategy is not running")
            return f"Strategy {strategy_id} is not running"
        strategy.stop()
        self.storage_client.update_strategy_status(strategy_id, StrategyStatus.INACTIVE)
        return f"Strategy {strategy_id} stopped"

    def create_strategy(self, strategy_name, **kwargs):
        strategy: BaseStrategy = strategies[strategy_name](**kwargs)
        self.storage_client.write_strategy(
            strategy.strategy_id, strategy_name, StrategyStatus.INACTIVE
        )
        self.strategies.append(strategy)
        return strategy.strategy_id

    def delete_strategy(self, strategy_id):
        strategy = self.get_strategy(strategy_id)
        strategy.stop()
        self.strategies.remove(strategy)
        self.storage_client.remove_strategy(strategy_id)
        return f"Strategy {strategy_id} deleted"

    def get_strategy(self, strategy_id):
        for strategy in self.strategies:
            if strategy.strategy_id == strategy_id:
                return strategy


# def get_running_strategies(self):
#     return [strategy for strategy in self.strategies if strategy.is_running]
