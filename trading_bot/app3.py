import logging
import json
from datetime import datetime, timedelta
from alpaca_broker import AlpacaBroker
from alpaca_market_data import AlpacaMarketData
from trading_engine import TradingEngine
from BuyCloseSellOpen import BuyCloseSellOpen
from MoodyTrader import MoodyTrader
from ShortTermMomentum import ShortTermMomentum

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("trading_app")

# Configuration
with open("cfg.json", "r") as config_file:
        config = json.load(config_file)
    
TABLE_NAME = config.get("table_name")
ALPACA_API_KEY = config.get("ALPACA_API_KEY")
ALPACA_SECRET_KEY = config.get("ALPACA_API_SECRET")



# Let's do some testing



SYMBOL = "AAPL"  # Example stock symbol
CAPITAL = 10000  # Example capital for trading (in USD)
TRADE_DAYS = 5   # Number of trading days to run
STRATEGY_ID = "BuyCloseSellOpen"  # Unique ID for the strategy

# Main application logic
def main():
    broker = AlpacaBroker(ALPACA_API_KEY, ALPACA_SECRET_KEY)
    market_data = AlpacaMarketData(ALPACA_API_KEY, ALPACA_SECRET_KEY)
    my_strat1 = BuyCloseSellOpen(symbol= SYMBOL, capital=CAPITAL)
    my_engine1 = TradingEngine(strategy=my_strat1, broker=broker, market_data=market_data, capital=CAPITAL)

    my_strat2 = MoodyTrader(symbol="META", capital=CAPITAL)
    my_engine_2 = TradingEngine(strategy=my_strat2, broker=broker, market_data=market_data, capital=CAPITAL)

    my_strat3 = ShortTermMomentum(symbol="MSFT", capital=CAPITAL)
    my_engine3 = TradingEngine(strategy=my_strat3, broker=broker, market_data=market_data, capital = CAPITAL)

    start_date = datetime.now()
    end_date = start_date + timedelta(days=5)  # Run for 1 day
    sleep_interval = 60  # 1-minute intervals

    # Run the trading engine
    print("Starting the ShortTermMomentum strategy...")

    # my_engine1.run(start_date=start_date, end_date=end_date, sleep_interval=sleep_interval)
    my_engine3.run(start_date=start_date, end_date=end_date, sleep_interval=sleep_interval)
    print("BuyCloseSellOpen strategy has completed.")

        

if __name__ == "__main__":
    main()