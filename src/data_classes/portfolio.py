from dataclasses import dataclass


@dataclass
class Portfolio:
    account_id: str
    account_name: str
    balance: float
    currency: str
    is_active: bool
    numberOfTransactions: int
