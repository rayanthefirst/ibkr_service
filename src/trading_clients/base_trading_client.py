from abc import ABC, abstractmethod
from decimal import Decimal
from definitions.order_definitions import (
    OrderState,
    OrderAction,
    OrderTIF,
    TrailingStopType,
)
from definitions.securities_definitions import TradableSecurity, OptionSide


class BaseTradingClient(ABC):
    """Abstract base class which encapsulates necessary functions from trading platforms"""

    name = "BaseTradingClient"

    @abstractmethod
    def connect(self):
        ...

    @abstractmethod
    def disconnect(self):
        ...

    @abstractmethod
    def get_portfolio_info(self):
        """
        Example response:
        [{'position': Decimal('7614.6300000000001091393642127513885498046875'), 'currency': 'CAD', 'expiry': None, 'putOrCall': None, 'strike': Decimal('0'), 'assetClass': 'CASH', 'ticker': 'CAD'},
          {'position': Decimal('6971.59000000000014551915228366851806640625'), 'currency': 'USD', 'expiry': None, 'putOrCall': None, 'strike': Decimal('0'), 'assetClass': 'CASH', 'ticker': 'USD'}]
        """

    @abstractmethod
    def place_market_order(
        self,
        quantity: Decimal,
        action: OrderAction,
        timeInForce: OrderTIF,
        symbol: str,
        secType: TradableSecurity,
        expiryDate: str = None,
        strike: Decimal = None,
        right: OptionSide = None,
    ):
        ...

    @abstractmethod
    def place_trail_order(
        self,
        quantity: Decimal,
        action: OrderAction,
        timeInForce: OrderTIF,
        trlAmtOrPrc: Decimal,
        trlType: TrailingStopType,
        symbol: str,
        secType: TradableSecurity,
        expiryDate: str = None,
        strike: Decimal = None,
        right: OptionSide = None,
    ):
        ...

    @abstractmethod
    def get_order_status(self, orderId: int):
        """
        Example response:
        {'status': 'filled', 'executedPrice': Decimal('181.13'), 'executedTime': 1704488394000}
        """
        ...

    @abstractmethod
    def cancel_order(self, orderId: int):
        ...
