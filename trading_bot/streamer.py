
import requests
from alpaca.trading import TradingStream
import json
from strategy import *

# QUESTDB_HOST = os.environ.get("QUESTDB_HOST", "localhost")
QUESTDB_HOST = "localhost"
CONF = f"http::addr={QUESTDB_HOST}:9000;username=admin;password=quest;"

with open("cfg.json", "r") as config_file:
        config = json.load(config_file)
    
TABLE_NAME = config.get("table_name")
ALPACA_API_KEY = config.get("ALPACA_API_KEY")
ALPACA_SECRET_KEY = config.get("ALPACA_API_SECRET")

API_URL = "http://localhost:8000/trades/"


async def handler(data):
    
    if data.event == "fill":
         
        print(data.order)

        trade_dict = {
            "client_order_id": data.order.client_order_id,
            "symbol": data.order.symbol,
            "side": data.order.side,
            "filled_qty": data.order.filled_qty,
            "filled_avg_price": data.order.filled_avg_price,
            "timestamp": data.order.filled_at.isoformat()
        }

        response = requests.post(API_URL, json = trade_dict)
        if response.status_code == 200:
             print(f"Trade posted to database: {trade_dict}")
        else:
             print(f"Error submitting trade to database: {response.text}")



stream = TradingStream(ALPACA_API_KEY, ALPACA_SECRET_KEY, paper=True)
stream.subscribe_trade_updates(handler)
stream.run()



