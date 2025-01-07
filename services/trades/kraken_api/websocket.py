import json
from datetime import datetime
from typing import List

from loguru import logger
from websocket import create_connection

from .trade import Trade


class KrakenWebsocketAPI:
    URL = (
        "wss://ws.kraken.com/v2"  # https://docs.kraken.com/api/docs/websocket-v2/trade
    )

    def __init__(self, pairs: List[str]):
        self.pairs = pairs

        # create a websocket connection to Kraken
        # https://websocket-client.readthedocs.io/en/latest/examples.html
        self._ws_client = create_connection(
            url=self.URL,
        )

        # subscribe to the Kraken Websocket API
        self._subscribe()

    def get_trades(self) -> List[Trade]:
        """
        Fetches the trades from the Kraken Websocket APIs and return them as a list of Trade objects
        Returns:
            List[Trade]: A list of Trade objects
        """

        # receive data from websocket
        data = self._ws_client.recv()

        # check for data channels == heart beat (no trades for that timing)
        if "heartbeat" in data:
            logger.info("Heartbeat received")
            return []

        try:
            # transform the data into a list of JSON object - DICT
            data = json.loads(data)
        except json.JSONDecodeError as e:
            logger.error(f"Failed decoding JSON: {e}")
            return []

        # print(json.dumps(data,indent=2)) - in CLI to pretty print

        try:
            trades_data = data["data"]
        except KeyError as e:
            logger.error(f"No 'data' field with trades in the message: {e}")
            return []

        trades = []

        for trade in trades_data:
            trade_obj = Trade.from_kraken_api_response(
                pair=trade["symbol"],
                price=trade["price"],
                volume=trade["qty"],
                timestamp=trade["timestamp"],
            )
            trades.append(trade_obj)

        # trades = [Trade(
        #     pair=trade["symbol"],
        #     price=trade["price"],
        #     volume=trade["qty"],
        #     timestamp=trade["timestamp"],
        # ) for trade in trades_data]

        # breakpoint()

        return trades

    def _subscribe(self):
        """
        Subscribes to the Kraken Websocket API and waits fo initial snapshot
        """
        # send a subscribe request to the websocket
        self._ws_client.send(
            json.dumps(
                {
                    "method": "subscribe",
                    "params": {
                        "channel": "trade",
                        "symbol": self.pairs,
                        "snapshot": True,
                    },
                }
            )
        )

        for _ in self.pairs:
            # to drop first two messages (info and snapshot)
            _ = self._ws_client.recv()  # wait for the response
            _ = self._ws_client.recv()  # wait for the response


def datestr2milliseconds(iso_time: str) -> int:
    """
    Converts the ISO time to milliseconds
            Examples:
                - "2024-01-03T16:20:30.123Z" -> 1704299430123
                - "2024-01-03T16:20:30.000Z" -> 1704299430000

            Args:
                iso_time (str): ISO time format (e.g., "2024-01-03T16:20:30.123Z")
            Returns:
                int: Unix timestamp in milliseconds
    """
    dt = datetime.strptime(iso_time, "%Y-%m-%dT%H:%M:%S.%fZ")
    return int(dt.timestamp() * 1000)
