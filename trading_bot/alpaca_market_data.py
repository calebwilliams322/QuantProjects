from pytz import utc
import requests
from market_data import MarketData
from datetime import datetime, timedelta
import pandas as pd
from alpaca.data import StockHistoricalDataClient, StockBarsRequest, DataFeed, TimeFrame
import json
with open("cfg.json", "r") as config_file:
        config = json.load(config_file)
    
TABLE_NAME = config.get("table_name")
ALPACA_API_KEY = config.get("ALPACA_API_KEY")
ALPACA_SECRET_KEY = config.get("ALPACA_API_SECRET")

class AlpacaMarketData(MarketData):
    """
    Implementation of the MarketData interface using the Alpaca Market Data API.
    This class fetches current and historical price data to support trading strategies.
    """

    BASE_URL = "https://data.alpaca.markets/v2"

    def __init__(self, api_key: str, secret_key: str):
        """
        Initializes the AlpacaMarketData instance with API keys for authentication.
        :param api_key: Your Alpaca API key.
        :param secret_key: Your Alpaca API secret key.
        """
        self.headers = {
            "APCA-API-KEY-ID": ALPACA_API_KEY,
            "APCA-API-SECRET-KEY": ALPACA_SECRET_KEY
        }

    def get_current_price(self, symbol: str) -> float:
        """
        Fetches the latest market price for the given symbol.
        :param symbol: The asset symbol (e.g., 'AAPL').
        :return: The latest price of the symbol.
        """
        endpoint = f"{self.BASE_URL}/stocks/{symbol}/trades/latest"
        try:
            response = requests.get(endpoint, headers=self.headers)
            response.raise_for_status()
            data = response.json()
           
            return data["trade"]["p"]  # 'p' is the price field
        except Exception as e:
            print(f"Error fetching current price for {symbol}: {e}")
            raise


    def get_last_close_price(self, symbol: str) -> float:
        """
        Fetches the last close price for the given symbol.
        :param symbol: The asset symbol.
        :return: The last close price of the symbol.
        """
        client = StockHistoricalDataClient(ALPACA_API_KEY, ALPACA_SECRET_KEY)
        now = datetime.now()
   
        request_params = StockBarsRequest(
            symbol_or_symbols=symbol,
            timeframe=TimeFrame.Day,
            start=now - timedelta(days=10),
            end=now,
            feed = DataFeed.IEX
        )
        
        barset = client.get_stock_bars(request_params).df
        return barset["close"].iloc[-1]
    
    def feed_bars(self, symbol: str, timeframe: TimeFrame, start_time: datetime, end_time: datetime) -> pd.DataFrame:
        '''Grab stock bars of various type. This will be a method of providing
        a strategy with appropriate data
        '''
        client = StockHistoricalDataClient(ALPACA_API_KEY, ALPACA_SECRET_KEY)
        request_params = StockBarsRequest(
            symbol_or_symbols=symbol,
            timeframe=timeframe,
            start=start_time,
            end=end_time,
            feed = DataFeed.IEX
        )

        bars = client.get_stock_bars(request_params=request_params).df
        return bars
    
    
    
