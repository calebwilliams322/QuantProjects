from datetime import *
from strategy import *
from alpaca_market_data import *


class BuyCloseSellOpen(Strategy):
    """
    A strategy that buys at market close and sells at market open.
    """

    def __init__(self, symbol: str, capital: float):
        self.strategy_id = "BuyCloseSellOpen"
        self.symbol = symbol
        self.capital = capital
        self.position = 0  # Shares
    
        

    def generate_signal(self, last_close_price: float, current_price: float, data: pd.DataFrame) -> dict:
        """
        Generate a buy or sell signal based on the time of day.
        - Buys at market close.
        - Sells at market open the next day.
        """
        now = datetime.now(utc)
        close_time = now.replace(hour=21, minute=0, second=0, microsecond=0)  
        open_time = now.replace(hour=14, minute=32, second=0, microsecond=0)    


        if now >= close_time - timedelta(minutes=10) and self.position == 0 and now < close_time:
            
            # Buy signal at market close
            price = last_close_price
            quantity = int(self.capital * 0.5 // price)  # Buy shares equivalent to half of capital
            self.position = quantity
            return {"action": "buy", "symbol": self.symbol, "quantity": quantity, "price": price}

        elif now >= close_time - timedelta(minutes=10) and now < close_time and self.position < 0:
            price = last_close_price
            quantity = -self.position
            self.position = 0
            return {"action": "buy", "symbol": self.symbol, "quantity": quantity, "price": price}
            

        elif now >= open_time and now < close_time - timedelta(hours=2) and self.position > 0:
            # Sell signal at market open
            price = last_close_price
            quantity = self.position
            self.position = 0
            return {"action": "sell", "symbol": self.symbol, "quantity": quantity, "price": price}

        elif now >= open_time and now < close_time - timedelta(hours=2) and self.position == 0:
            price = last_close_price
            quantity = int(self.capital * 0.5 // price)  # Sell shares equivalent to half of capital
            self.position = -quantity
            return {"action": "sell", "symbol": self.symbol, "quantity": quantity, "price": price}
        
        else:
            return None
        
