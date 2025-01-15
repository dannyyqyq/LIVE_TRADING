import json
import time
from typing import List

import requests
from loguru import logger

from .base import TradesAPI
from .trade import Trade


class KrakenRestAPI(TradesAPI):
    def __init__(self, pairs: List[str]):
        self.pairs = pairs

    def get_trades(self):
        breakpoint()

    def is_done(self):
        pass


class KrakenRestAPISinglePair(TradesAPI):
    URL = "https://api.kraken.com/0/public/Trades"

    def __init__(
        self,
        pair: str,
        last_n_days: int,
    ):
        self.pair = pair
        self.last_n_days = last_n_days
        self.since_timestamp_sec = int(time.time()) - last_n_days * 24 * 60 * 60

        logger.info(
            f"getting trades for pair: {self.pair} for the last {self.since_timestamp_sec} "
        )

    def get_trades(self) -> List[Trade]:
        """
        Sends a request to the Kraken API and returns trades for that pair
        """

        headers = {"Accept": "application/json"}

        # Get parameters
        params = {
            "pair": self.pair,
            "since": self.since_timestamp_sec,
        }

        response = requests.request("GET", self.URL, headers=headers, params=params)

        # Parse response as json
        try:
            data = json.loads(response.text)
        except json.JSONDecodeError as e:
            logger.error(f"Failed decoding JSON: {e}")
            return []

        # Get trades for the self.pair currency
        try:
            trades = data["result"][self.pair]
        except KeyError as e:
            logger.error(f"Failed to get trades for pair: {self.pair} : {e}")
            return []

        # convert the trade to trade objects
        trades = [
            Trade.from_kraken_rest_api_response(
                pair=self.pair,
                price=trade[0],
                volume=trade[1],
                timestamp_sec=trade[2],
            )
            for trade in trades
        ]

        return trades

    def is_done(self):
        pass
