from abc import ABC, abstractmethod
from broker import *
from market_data import *
import pandas as pd

# Base Strategy class to define the interface for trading strategies
class Strategy(ABC):
    """
    Abstract base class for trading strategies.
    """

    def __init__(self, strategy_id:str):
        self.strategy_id = strategy_id
        

    @abstractmethod
    def generate_signal(self, last_close_price: float, current_price: float, data: pd.DataFrame) -> dict:
        """
        Generate a trading signal based on the strategy.
        :param market_data: Instance of MarketData to access market info.
        :return: A dictionary containing the trading signal, e.g.:
                 {"action": "buy", "symbol": "AAPL", "quantity": 10, "price": 150.0}
        """
        pass