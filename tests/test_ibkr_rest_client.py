import pytest
from src.account_clients.ibkr_rest_client import IBKR_Rest_Client


class TestIBKR_Rest_Client:
    def setup_class(cls):
        cls.client = IBKR_Rest_Client()

    def test_get_portfolio_info(self):
        portfolio_info = self.client.get_portfolio_info()
        assert isinstance(portfolio_info, list)

    def test_place_mkt_order(self):
        order = self.client.place_mkt_order(
            quantity=100, action="BUY", timeInForce="DAY", symbol="AAPL", secType="STK"
        )
        assert isinstance(order, dict)

    def test_place_trail_order(self):
        order = self.client.place_trail_order(
            quantity=100,
            action="BUY",
            timeInForce="DAY",
            trlAmtOrPrc=1.0,
            trlType="ABS",
            symbol="AAPL",
            secType="STK",
        )
        assert isinstance(order, dict)
