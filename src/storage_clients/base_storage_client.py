from abc import ABC, abstractmethod
from definitions.order_definitions import OrderState, OrderAction
from data_classes.contract import Contract


class BaseStorageClient(ABC):
    name = "BaseStorageClient"

    @abstractmethod
    def connect(self):
        pass

    @abstractmethod
    def disconnect(self):
        pass

    @abstractmethod
    def write_order(
        self,
        strategy_id,
        order_id,
        contract: Contract,
        quantity,
        action: OrderAction,
        executedPrice,
        executedTime: int,  # Unix timestamp UTC in ms
        orderState: OrderState,
        **kwargs,
    ):
        pass

    @abstractmethod
    def update_order_state(self, strategy_id, order_id, newOrderState: OrderState):
        pass

    @abstractmethod
    def check_for_active_orders(self, strategy_id):
        """
        Check if there is any active orders for the strategy id and return it
        if not return empty list
        """
        pass

    @abstractmethod
    def get_all_strategies(self):
        """
        Get all strategies for the strategy handler
        """
        pass
