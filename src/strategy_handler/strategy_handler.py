import asyncio
from strategies import strategies
from strategies.base_strategy import BaseStrategy
import logging
from typing import List

logger = logging.getLogger(__name__)


class StrategyHandler:
    def __init__(self):
        self.strategies: List(BaseStrategy) = []

    def create_strategy(self):
        pass

    def get_all_strategies(self):
        return self.strategies

    def get_running_strategies(self):
        return [strategy for strategy in self.strategies if strategy.is_running]

    def add_strategy(self, strategy):
        self.strategies.append(strategy)

    def start(self):
        logger.info("Starting strategy handler")
        for strategy in self.strategies:
            strategy.start()
