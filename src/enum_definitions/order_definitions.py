from enum import Enum


class OrderSide(Enum):
    BUY = "Buy"
    SELL = "Sell"


class OrderType(Enum):
    MARKET = "Market"
    LIMIT = "Limit"
    STOP = "Stop"
    STOP_LIMIT = "Stop Limit"
    TRAILING_STOP = "Trailing Stop"
    TRAILING_STOP_LIMIT = "Trailing Stop Limit"


class OrderState(Enum):
    PENDING_SUBMIT = "Pending Submit"
    PENDING_CANCEL = "Pending Cancel"
    PRE_SUBMITTED = "Pre Submitted"
    SUBMITTED = "Submitted"
    CANCELLED = "Cancelled"
    FILLED = "Filled"
    INACTIVE = "Inactive"
