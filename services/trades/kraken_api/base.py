from abc import ABC, abstractmethod
from typing import List

from .trade import Trade


class TradesAPI(ABC):
    def __init__(self, pairs: List[str]):
        self.pairs = pairs

    @abstractmethod
    def get_trades(self) -> List[Trade]:
        breakpoint()

    @abstractmethod
    def is_done(self) -> bool:
        pass
