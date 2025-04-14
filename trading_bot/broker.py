from abc import ABC, abstractmethod

class Broker(ABC):
    """
    Abstract Broker class that defines the interface for all broker implementations.
    """

    @abstractmethod
    def buy(self, symbol: str, quantity: float, order_type: str, time_in_force: str) -> dict:
        """
        Place a buy order.
        :param symbol: The asset symbol (e.g., 'BTC/USD', 'AAPL').
        :param quantity: Quantity of the asset to buy.
        :param order_type: Type of order ('market', 'limit', etc.).
        :param time_in_force: Time in force ('gtc', 'ioc', etc.).
        :return: Details of the submitted order.
        """
        pass

    @abstractmethod
    def sell(self, symbol: str, quantity: float, order_type: str, time_in_force: str) -> dict:
        """
        Place a sell order.
        :param symbol: The asset symbol (e.g., 'BTC/USD', 'AAPL').
        :param quantity: Quantity of the asset to sell.
        :param order_type: Type of order ('market', 'limit', etc.).
        :param time_in_force: Time in force ('gtc', 'ioc', etc.).
        :return: Details of the submitted order.
        """
        pass

    @abstractmethod
    def get_order_status(self, order_id: str) -> dict:
        """
        Retrieve the status of an order.
        :param order_id: The unique ID of the order.
        :return: Current status of the order.
        """
        pass

   

