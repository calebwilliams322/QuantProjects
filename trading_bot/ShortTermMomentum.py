from alpaca_market_data import AlpacaMarketData
from strategy import *
from alpaca_market_data import *


class ShortTermMomentum(Strategy):
    """
    A strategy that determines whether a stock has 'momentum',
    in which case it goes long for the day. Otherwise it goes short.
    """

    def __init__(self, symbol: str, capital: float):
        self.strategy_id = "ShortTermMomentum"
        self.symbol = symbol
        self.capital = capital
        self.position = 0  # To track whether the strategy currently has an asset purchased or not
        

    def generate_signal(self, last_close_price: float, current_price: float, data: pd.DataFrame) -> dict:
        """
        Calculate the percent change in first 30 minutes and decide
        """
        now = datetime.now(utc)
        market_close = datetime.now(utc).replace(hour=21, minute=0, second=0, microsecond=0)
        market_open = datetime.now(utc).replace(hour=14, minute=31, second=0, microsecond=0)
    
        if len(data) > 0:
            if now < market_close - timedelta(hours=1) and now > market_open + timedelta(minutes=30) and self.position == 0:
                
                opening_price = data.iloc[0]['open']
                price_30min = data.iloc[-1]['close']
                change = ((price_30min - opening_price)/opening_price)*100
                print(f"{self.symbol}: Opening Price: {opening_price}, 30-Minute Price: {price_30min}, Change: {change:.2f}%")
                if change > 1:
                    price = current_price
                    quantity = int(self.capital * 0.5 // price)  # Buy shares equivalent to half of capital
                    self.position = quantity
                    return {"action": "buy", "symbol": self.symbol, "quantity": quantity, "price": price}
                else:
                    print(f"Opening surge was not enough to warrent a momentum buy, going short")
                    price = current_price
                    quantity = int(self.capital * 0.5 // price)  # Buy shares equivalent to half of capital
                    self.position = - quantity
                    return {"action": "sell", "symbol": self.symbol, "quantity": quantity, "price": price}
    
        else:
            print("No market data available, you missed the 30 minute window!")
            if now > market_open + timedelta(hours=6) and now < market_close and self.position < 0:
                price = current_price
                quantity = -self.position
                self.position = 0
                return {"action": "buy", "symbol": self.symbol, "quantity": quantity, "price": price}   
            elif now > market_open + timedelta(hours=6) and now < market_close and self.position > 0:
                price = current_price
                quantity = self.position
                self.position = 0
                return {"action": "sell", "symbol": self.symbol, "quantity": quantity, "price": price} 
            else:
                return None

        
        