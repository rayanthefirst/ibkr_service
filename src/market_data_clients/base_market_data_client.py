from abc import ABC, abstractmethod


class BaseMarketDataClient(ABC):
    """
    Base class for market data clients.
    Remove abastract methods and add common methods for all market data clients.
    """

    name = "BaseMarketDataClient"

    @abstractmethod
    def connect(self):
        pass

    @abstractmethod
    def subscribe(self, symbol):
        pass

    @abstractmethod
    def unsubscribe(self, symbol):
        pass

    @abstractmethod
    def disconnect(self):
        pass
