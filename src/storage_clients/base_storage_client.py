from abc import ABC, abstractmethod


class BaseStorageClient(ABC):
    @abstractmethod
    def connect(self):
        pass

    @abstractmethod
    def disconnect(self):
        pass

    @abstractmethod
    def write(self, **data):
        pass

    @abstractmethod
    def read(self, **data):
        pass

    @abstractmethod
    def write_order(
        self,
        strategy_id,
        strategy_name,
        contract,
        quantity,
        side,
        executedPrice,
        executedTime,
        orderState,
    ):
        pass

    @abstractmethod
    def check_for_active_order(self, strategy_id):
        """
        Check if there is an active order for the strategy id and return it
        if not return None
        """
        pass
