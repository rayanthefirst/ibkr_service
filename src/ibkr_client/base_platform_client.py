from abc import ABC, abstractmethod


class BasePlatformClient(ABC):
    """Abstract base class which encapsulates necessary functions from trading platforms"""

    @abstractmethod
    def get_portfolio_info(self):
        ...

    @abstractmethod
    def place_mkt_order(self):
        ...
