from decimal import Decimal
from data_classes.contract import Contract
from data_classes.portfolio import Portfolio
from market_data_clients.base_market_data_client import (
    BaseMarketDataClient,
)
from storage_clients.base_storage_client import BaseStorageClient
from trading_clients.base_trading_client import BaseTradingClient
from strategies.base_strategy import BaseStrategy


class longBuySellTrail(BaseStrategy):
    name = "longBuySellTrail"

    def __init__(
        self,
        trading_client,
        storage_client,
        market_data_client,
        initialQuantity,
        initialContract,
        initialPortfolio,
    ):
        super().__init__(
            trading_client,
            storage_client,
            market_data_client,
            initialQuantity,
            initialContract,
            initialPortfolio,
        )

    def start(self):
        self.is_running = True

        # Check if there is an existing active order
        currentOrder = self.storage_client.check_for_active_order(self.strategy_id)

        # If there is an existing order, wair until it is filled

        while True:
            # Wait for order to be filled if exists otherwise
            ## WaitForCurrentOrderToBeFilled(currentOrder)

            oldOrder = currentOrder

            # Place new order
            ## PlaceNewOrder(oldOrder))

    def stop(self):
        self.is_running = False

    def get_strategy_info(self):
        pass


class short(BaseStrategy):
    def __init__(
        self,
        trading_client: BaseTradingClient,
        storage_client: BaseStorageClient,
        market_data_client: BaseMarketDataClient,
        initialQuantity: Decimal = None,
        initialContract: Contract = None,
        initialPortfolio: Portfolio = None,
    ):
        super().__init__(
            trading_client,
            storage_client,
            market_data_client,
            initialQuantity,
            initialContract,
            initialPortfolio,
        )

    def start(self):
        pass

    def stop(self):
        pass

    def get_strategy_info(self):
        pass
