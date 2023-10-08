"""
IBKR REST API Client account methods
"""
import calendar
import logging
import time
import warnings

from requests import Response, get, post, delete
from urllib3.exceptions import InsecureRequestWarning
from src.sec_def import option_secType, stock_secType
from src.config import IBKR_CASH_ACCOUNT_ID

import src.logging_settings

from src.ibkr_client.base_platform_client import BasePlatformClient

warnings.simplefilter("ignore", InsecureRequestWarning)

logger = logging.getLogger(__name__)


class IBKR_Rest_Client(BasePlatformClient):
    """Interactive Brokers REST API Client"""

    def __init__(self):
        self.host_url = "https://localhost:5000/v1/api"
        self.accountId = IBKR_CASH_ACCOUNT_ID

    def check_response(self, resp: Response) -> bool:
        if resp.status_code == 200:
            return True
        elif resp.status_code != 200:
            logger.error(f"IBKR REST Error: {resp.json()}")
            raise Exception(f"IBKR REST Error: {resp.json()['error']}")
        else:
            raise Exception(f"Client Error: {resp.json()['error']}")

    def ibkr_get_request(self, uri_path: str, params: dict = None) -> Response:
        resp = get(self.host_url + uri_path, params=params, verify=False)
        if self.check_response(resp):
            return resp.json()

    def ibkr_post_request(
        self, uri_path: str, body: dict = None, params: dict = None
    ) -> Response:
        resp = post(self.host_url + uri_path, json=body, params=params, verify=False)
        if self.check_response(resp):
            return resp.json()

    def ibkr_delete_request(
        self, uri_path: str, body: dict = None, params: dict = None
    ) -> Response:
        resp = delete(self.host_url + uri_path, json=body, params=params, verify=False)
        if self.check_response(resp):
            return resp.json()

    # ABSTRACT BASE CLASS METHODS
    def get_portfolio_info(self):
        while True:
            try:
                accountPositions = [
                    {
                        "position": pos["position"],
                        "currency": pos["currency"],
                        "expiry": pos["expiry"],
                        "putOrCall": pos["putOrCall"],
                        "strike": pos["strike"],
                        "assetClass": pos["assetClass"],
                        "ticker": pos["ticker"],
                    }
                    # Default 30 pos per request
                    for pos in self.ibkr_get_request(
                        f"/portfolio/{self.accountId}/positions/0"
                    )
                    if pos["assetClass"] != "CASH"
                ]

                accountCash = [
                    {
                        "position": pos["cashbalance"],
                        "currency": k,
                        "expiry": None,
                        "putOrCall": None,
                        "strike": 0,
                        "assetClass": "CASH",
                        "ticker": k,
                    }
                    for k, pos in self.ibkr_get_request(
                        f"/portfolio/{self.accountId}/ledger"
                    ).items()
                    if k != "BASE"
                ]

            except KeyError:
                time.sleep(0.01)
            else:
                break

        return accountPositions + accountCash

    def place_mkt_order(
        self,
        quantity: float,
        action: str,
        timeInForce: str,
        symbol: str,
        secType: str,
        expiryDate: str = None,
        strike: float = None,
        right: str = None,
    ):
        conid = self.get_instrument_conid(symbol, secType, expiryDate, strike, right)

        try:
            createdOrder = self.ibkr_post_request(
                f"/iserver/account/{self.accountId}/orders",
                body={
                    "orders": [
                        {
                            "conid": conid,
                            "secType": secType,
                            "orderType": "MKT",
                            "quantity": quantity,
                            "side": action,
                            "tif": timeInForce,
                        }
                    ]
                },
            )[0]

        except Exception:
            raise Exception

        orderSubmitId = createdOrder["id"]

        while True:
            sendOrder = self.ibkr_post_request(
                f"/iserver/reply/{orderSubmitId}", body={"confirmed": True}
            )[0]
            if "order_id" in sendOrder:
                return sendOrder
            else:
                orderSubmitId = sendOrder["id"]

    def place_trail_order(
        self,
        quantity: float,
        action: str,
        timeInForce: str,
        trlAmtOrPrc: float,
        trlType: str,
        symbol: str,
        secType: str,
        expiryDate: str = None,
        strike: float = None,
        right: str = None,
    ):
        conid = self.get_instrument_conid(symbol, secType, expiryDate, strike, right)

        try:
            createdOrder = self.ibkr_post_request(
                f"/iserver/account/{self.accountId}/orders",
                body={
                    "orders": [
                        {
                            "conid": conid,
                            "secType": secType,
                            "orderType": "TRAIL",
                            "quantity": quantity,
                            "side": action,
                            "tif": timeInForce,
                            "trailingAmt": trlAmtOrPrc,
                            "trailingType": trlType,
                        }
                    ]
                },
            )[0]

        except Exception:
            raise Exception

        orderSubmitId = createdOrder["id"]

        while True:
            sendOrder = self.ibkr_post_request(
                f"/iserver/reply/{orderSubmitId}", body={"confirmed": True}
            )[0]
            if "order_id" in sendOrder:
                return sendOrder
            else:
                orderSubmitId = sendOrder["id"]

    def get_instrument_conid(
        self,
        symbol: str,
        secType: str,
        expiryDate: str = None,
        strike: float = None,
        right: str = None,
    ):
        """
        right: "call" or "put"
        Only works for STK and OPT
        """
        symbolInfo = self.ibkr_post_request(
            "/iserver/secdef/search", body={"symbol": symbol}
        )[0]
        underlyingConid = int(symbolInfo["conid"])
        if secType == option_secType:
            numericalFormattedDate = expiryDate.replace("-", "")
            availableOptionDates = symbolInfo["opt"].split(";")

            if numericalFormattedDate not in availableOptionDates:
                raise Exception("No available option contract for expiry date")

            monthYearFormattedDate = (
                calendar.month_abbr[int(expiryDate[5:7])].upper() + expiryDate[2:4]
            )
            availableStrikes = self.ibkr_get_request(
                "/iserver/secdef/strikes",
                params={
                    "conid": underlyingConid,
                    "sectype": "OPT",
                    "month": monthYearFormattedDate,
                },
            )

            if strike not in availableStrikes[right]:
                raise Exception("No available option contract for strike price")

            for option in self.ibkr_get_request(
                "/iserver/secdef/info",
                params={
                    "conid": underlyingConid,
                    "sectype": "OPT",
                    "month": monthYearFormattedDate,
                    "strike": strike,
                    "right": "C" if right == "call" else "P",
                },
            ):
                if option["maturityDate"] == numericalFormattedDate:
                    return int(option["conid"])

        elif secType == stock_secType:
            return underlyingConid

    def get_live_orders(self):
        live_orders = self.ibkr_get_request("/iserver/account/orders")["orders"]
        return live_orders

    def get_order_status(self, orderId: int):
        order_status = self.ibkr_get_request(f"/iserver/account/order/status/{orderId}")
        return order_status

    def cancel_order(self, orderId: int):
        cancelled_order = self.ibkr_delete_request(
            f"/iserver/account/{self.accountId}/order/{orderId}"
        )
        return cancelled_order
