import time
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry


class OrderBookService:

    BASE_URL = "https://fapi.binance.com"

    def __init__(self):

        self.session = requests.Session()

        retry = Retry(
            total=3,
            connect=3,
            read=3,
            backoff_factor=1,
            status_forcelist=[
                429,
                500,
                502,
                503,
                504,
            ],
            allowed_methods=["GET"],
        )

        adapter = HTTPAdapter(max_retries=retry)

        self.session.mount(
            "https://",
            adapter,
        )

        self.session.mount(
            "http://",
            adapter,
        )

    # ------------------------------------
    # Normalize Symbol
    # ------------------------------------

    def normalize_symbol(
        self,
        symbol,
    ):

        return (
            symbol
            .replace("/", "")
            .replace(":USDT", "")
            .upper()
        )

    # ------------------------------------
    # Internal GET
    # ------------------------------------

    def _get(
        self,
        endpoint,
        params=None,
    ):

        url = f"{self.BASE_URL}{endpoint}"

        response = self.session.get(
            url,
            params=params,
            timeout=30,
        )

        response.raise_for_status()

        return response.json()

    # ------------------------------------
    # Order Book
    # ------------------------------------

    def get_order_book(
        self,
        symbol,
        limit=100,
    ):

        if limit not in (
            5,
            10,
            20,
            50,
            100,
            500,
            1000,
        ):
            raise ValueError(
                "Invalid Binance depth limit."
            )

        symbol = self.normalize_symbol(symbol)

        data = self._get(

            "/fapi/v1/depth",

            params={
                "symbol": symbol,
                "limit": limit,
            },

        )

        return {

            "symbol": symbol,

            "last_update_id": data["lastUpdateId"],

            "timestamp": int(
                time.time() * 1000
            ),

            "bids": [

                {
                    "price": float(x[0]),
                    "qty": float(x[1]),
                }

                for x in data["bids"]

            ],

            "asks": [

                {
                    "price": float(x[0]),
                    "qty": float(x[1]),
                }

                for x in data["asks"]

            ],

        }