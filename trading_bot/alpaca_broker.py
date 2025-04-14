from alpaca.trading.client import TradingClient
from alpaca.trading.requests import MarketOrderRequest
from alpaca.trading.enums import OrderSide, OrderType, TimeInForce
from broker import Broker
from typing import Literal



class AlpacaBroker(Broker):
    """
    Implementation of the Broker interface using the Alpaca API.
    """

    def __init__(self, api_key: str, secret_key: str):
        """
        Initializes the AlpacaBroker with API keys.
        This will create an instance of Alpaca's TradingClient to interact with the API.

        :param api_key: Your Alpaca API key.
        :param secret_key: Your Alpaca API secret key.
        """
        self.client = TradingClient(api_key, secret_key)
    
    def create_client_order_id(self, strategy_id: str, trade_number: int, entry_or_exit=Literal["ENTRY", "EXIT"]) ->  str:
        '''Strategy id must have form strategy_id = f"{STRATEGY_NAME}_{trade_number}:{uuid4()}" when implemented'''
        return f"{strategy_id}_{trade_number}@{entry_or_exit}"
    

    def place_order(self, symbol: str, quantity:float, action: str, strategy_id: str, trade_number: int):
        if action == "buy" or action == "BUY" or action == "Buy":
            entry_or_exit="ENTRY"
            order = self.buy(symbol=symbol, quantity=quantity, strategy_id=strategy_id, trade_number=trade_number, entry_or_exit=entry_or_exit)
            return order
        else:
            entry_or_exit= "EXIT"
            order = self.sell(symbol=symbol, quantity=quantity, strategy_id=strategy_id, trade_number=trade_number, entry_or_exit=entry_or_exit)
            return order

    def buy(self, symbol: str, quantity: float, strategy_id: str, trade_number: int, entry_or_exit=Literal["ENTRY", "EXIT"]) -> dict:
        """
        Places a buy order using Alpaca's TradingClient.

        """
        try:
            order_request = MarketOrderRequest(
                client_order_id= self.create_client_order_id(strategy_id, trade_number, entry_or_exit),
                symbol=symbol,
                qty=quantity,
                side=OrderSide.BUY,
                type=OrderType.MARKET,
                time_in_force=TimeInForce.GTC,
            )
            order = self.client.submit_order(order_request)
            return order  # dict of order
        except Exception as e:
            print(f"Error placing buy order: {e}")
            raise

    def sell(self, symbol: str, quantity: float, strategy_id: str, trade_number: int, entry_or_exit=Literal["ENTRY", "EXIT"]) -> dict:
        """
        Places a sell order using Alpaca's TradingClient.
        """
        try:
            
            order_request = MarketOrderRequest(
                client_order_id = self.create_client_order_id(strategy_id=strategy_id, trade_number=trade_number, entry_or_exit=entry_or_exit),
                symbol=symbol,
                qty=quantity,
                side=OrderSide.SELL,
                time_in_force=TimeInForce.GTC,
            )
            order = self.client.submit_order(order_request)
            return order  # dict of order
        except Exception as e:
            print(f"Error placing sell order: {e}")
            raise

    def get_order_status(self, order_id: str) -> dict:
        """
        Retrieves the status of an order.

        Expected Behavior:
        - Should return details about the order's current status (e.g., 'filled', 'canceled').
        - This method is critical for strategies that need to manage open positions effectively.
        """
        try:
            order = self.client.get_order_by_id(order_id)
            return order.model_dump()  # dict of order status
        except Exception as e:
            print(f"Error retrieving order status: {e}")
            raise

    