from abc import ABC, abstractmethod

class MarketData(ABC):
    """
    Abstract interface for fetching market data.
    """

    @abstractmethod
    def get_current_price(self, symbol: str) -> float:
        """
        Retrieve the current market price for a given symbol.
        :param symbol: The asset symbol (e.g., 'AAPL', 'BTC/USD').
        :return: The current price of the symbol.
        """
        pass

    @abstractmethod
    def get_last_close_price(self, symbol: str) -> float:
        """
        Retrieve the last closing price for a given symbol.
        :param symbol: The asset symbol.
        :return: The last close price.
        """
        pass

    @abstractmethod
    def feed_bars(self, symbol: str, time_interval: str) -> float:
        """
        To feed a strategy stock bars.
        """
        pass