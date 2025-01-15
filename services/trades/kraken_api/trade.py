# Mock Kraken API

from datetime import datetime

from pydantic import BaseModel


class Trade(BaseModel):
    """
    A trade from the Kraken API.
    """

    pair: str
    price: float
    volume: float
    timestamp: str
    timestamp_ms: int

    @classmethod
    def from_kraken_rest_api_response(
        cls,
        pair: str,
        price: float,
        volume: float,
        timestamp_sec: float,
    ) -> "Trade":
        """
        Convert a kraken rest api response to a trade object
        E.G:
            ['103746.00000', '0.01224207', 1734352637.559016, 's', 'l', '', 77377589]
            Price: float
            Volume: float
            timestamp: float(seconds since epoch)
        """
        # Convert timestamp_sec from float to str
        timestamp_ms = int(float(timestamp_sec)) * 1000
        return cls(
            pair=pair,
            price=price,
            volume=volume,
            timestamp=cls._milliseconds2datestr(timestamp_ms),
            timestamp_ms=timestamp_ms,
        )

    @classmethod
    def from_kraken_websocket_api_response(
        cls,
        pair: str,
        price: float,
        volume: float,
        timestamp: datetime,
    ) -> "Trade":
        return cls(
            pair=pair,
            price=price,
            volume=volume,
            timestamp=timestamp,
            timestamp_ms=cls._datestr2milliseconds(timestamp),
        )

    @staticmethod
    def _milliseconds2datestr(milliseconds: int) -> str:
        return datetime.fromtimestamp(milliseconds / 1000).strftime(
            "%Y-%m-%dT%H:%M:%S.%fZ"
        )

    @staticmethod
    def _datestr2milliseconds(datestr: str) -> int:
        return int(
            datetime.strptime(datestr, "%Y-%m-%dT%H:%M:%S.%fZ").timestamp() * 1000
        )

    def to_str(self) -> str:
        # pydanctic model to string
        return self.model_dump_json()

    def to_dict(self) -> dict:
        # pydanctic model to dictionary
        return self.model_dump()
