from strategy import *
from alpaca_market_data import *
from datetime import *

class MoodyTrader(Strategy):
    """
    A strategy that buys at market close and sells at market open.
    """

    def __init__(self, symbol: str, capital: float):
        self.strategy_id = "MoodyTrader"
        self.symbol = symbol
        self.capital = capital
        self.position = 0  # Track long or short 

    def generate_signal(self, last_close_price: float, current_price: float, data: pd.DataFrame) -> dict:
        """
        Simply short when a trader would typically be in a 'bad' mood. Go
        long after a nice lunch break. 
        """
        market_open = datetime.now(utc).replace(hour=14, minute=31, 
                                                second=0, microsecond=0)
        market_close = datetime.now(utc).replace(hour=21, minute=0, 
                                                 second=0, microsecond=0)
        now = datetime.now(utc)
        
        if now > market_open and now < market_open + timedelta(hours=4) and self.position ==0:
            price = current_price
            quantity = int(self.capital * 0.5 // price)
            self.position = - quantity
            return {"action": "sell", "symbol": self.symbol, "quantity": quantity, "price": price}
        elif now > market_open + timedelta(hours=6) and now < market_close and self.position < 0:
            price = current_price
            quantity = - self.position
            self.position = 0
            return {"action": "buy", "symbol": self.symbol, "quantity": quantity, "price": price}
        
        else:
            return None