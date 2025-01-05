# Mock Kraken API

from pydantic import BaseModel, field_validator
from datetime import datetime
from typing import Optional
class Trade(BaseModel):
    # Data model for a single trade
    """
    "symbol": "MATIC/USD",
    "side": "sell",
    "price": 0.5117,
    "qty": 40.0,
    "ord_type": "market",
    "trade_id": 4665906,
    "timestamp": "2023-09-25T07:49:37.708706Z"
    """
    pair: str
    price: float
    volume: float
    timestamp: datetime
    timestamp_ms: Optional[int] = None
    
    
    # TODO: let Pydantic do the initialization of timestamp_ms from timestamp
    
    # @property
    # def timestamp_ms(self) -> int:
    #     """
    #     converts the timestamp to milliseconds
    #     """
    #     return int(self.timestamp.timestamp() * 1000)
    
    # @field_validator("timestamp_ms",mode="before")
    # def compute_timestamp_ms(cls, v, values):
    #     """
    #     Converts the timestamp to millieseconds.
    #     This function is called automatically by Pydantic before the trade object is created.
    #     """
    #     return int(values.data["timestamp"].timestamp() * 1000)
    
    # @field_validator("timestamp_ms", mode="before")
    # def compute_timestamp_ms(cls, v, values): # pydantic arguments
    #     """
    #     Converts the timestamp to millieseconds.
    #     This function is called automatically by Pydantic before the trade object is created.
    #     """
    #     timestamp = values.get("timestamp")
    #     if timestamp:
    #         return int(timestamp.timestamp() * 1000)
    #     return v 
    
    def to_dict(self):
        return self.model_dump_json() # convert to dictionary format for serialization

        # return {
        #     "pair": self.pair,
        #     "price": self.price,
        #     "volume": self.volume,
        #     "timestamp_ms": self.timestamp_ms,
        #     "timestamp": self.timestamp,
        # }
    