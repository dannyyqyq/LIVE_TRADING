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
    def from_kraken_api_response(
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

    @staticmethod  # The method is defined as a static method. This means it doesn't rely on the instance (self) or class (cls) to work and can be called directly using the class name.
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

        # return {
        #     "pair": self.pair,
        #     "price": self.price,
        #     "volume": self.volume,
        #     "timestamp_ms": self.timestamp_ms,
        #     "timestamp": self.timestamp,
        # }
