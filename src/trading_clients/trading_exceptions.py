class TradingConnectionError(Exception):
    """Exception raised for errors in connecting to a Trading client."""

    def __init__(self, message="Error connecting to Trading client"):
        self.message = message
        super().__init__(self.message)


class TradingGetPortfolioInfoError(Exception):
    """Exception raised for errors in getting a portfolio from a Trading client."""

    def __init__(self, message="Error getting portfolio from Trading client"):
        self.message = message
        super().__init__(self.message)


class TradingPlaceOrderError(Exception):
    """Exception raised for errors in placing an order with a Trading client."""

    def __init__(self, message="Error placing order with Trading client"):
        self.message = message
        super().__init__(self.message)


class TradingGetInstrumentError(Exception):
    """Exception raised for errors in getting an instrument from a Trading client."""

    def __init__(self, message="Error getting instrument from Trading client"):
        self.message = message
        super().__init__(self.message)


class TradingGetOrderError(Exception):
    """Exception raised for errors in getting an order from a Trading client."""

    def __init__(self, message="Error getting order from Trading client"):
        self.message = message
        super().__init__(self.message)


class TradingCancelOrderError(Exception):
    """Exception raised for errors in cancelling an order with a Trading client."""

    def __init__(self, message="Error cancelling order with Trading client"):
        self.message = message
        super().__init__(self.message)
