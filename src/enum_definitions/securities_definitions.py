from enum import Enum


class TradableSecurity(Enum):
    STOCK = "Stock"
    OPTION = "Option"
    FOREX = "Forex"
