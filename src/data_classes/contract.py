from dataclasses import dataclass


@dataclass
class Contract:
    symbol: str
    contract_type: str
    underlying_symbol: str
    strike: float
    expiration_date: str
    cash: float
    futures: str
    # Add more attributes as needed
