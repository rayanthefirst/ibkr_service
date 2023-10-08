from abc import ABC, abstractmethod
from ibkr_client.ibkr_rest_client import IBKR_Rest_Client
from decimal import Decimal


class BaseStrategy(ABC):
    """Abstract base class for trading strategies"""

    def __init__(self, ibkr_client: IBKR_Rest_Client, portfolio_allocation: Decimal, conId: int, quantity: Decimal):
        self.ibkr_client = ibkr_client
        self.portfolio_allocation = portfolio_allocation
        self.conId = conId
        self.quantity = quantity


        self.
        self.is_running = False


    
    @abstractmethod
    def start(self):
        self.is_running = True
        # Implement your strategy logic here
    
    @abstractmethod
    def stop(self):
        self.is_running = False
        # Implement any cleanup logic here
    
    @abstractmethod
    def get_trade_info(self):
        # Implement logic to retrieve trade information
        pass
