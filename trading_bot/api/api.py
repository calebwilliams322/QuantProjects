import requests
import logging
import logging.config
import time
from asyncpg import connect
import json
from contextlib import asynccontextmanager
from fastapi import FastAPI

from models import *

QUESTDB_HOST = "localhost"
QUESTDB_ENDPOINT = f"http://{QUESTDB_HOST}:9000/exec"
QUESTDB_HEALTHCHECK = f"http://{QUESTDB_HOST}:9003"

with open("cfg.json", "r") as config_file:
        config = json.load(config_file)
    
TABLE_NAME = config.get("table_name")
DATABASE_URL = f"postgresql://admin:quest@{QUESTDB_HOST}:8812/questdb"

# logging.config.fileConfig("logging.conf")
# logger = logging.getLogger(__name__)
# print("Using logger: ", logger.name, logger.level, logger.handlers)

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Initializes database"""

    # sql = f"""
    # CREATE TABLE IF NOT EXISTS {TABLE_NAME}(
    #     client_order_id STRING,
    #     symbol SYMBOL,
    #     side STRING,
    #     filled_qty DOUBLE,
    #     filled_avg_price DOUBLE,
    #     timestamp TIMESTAMP
    # ) TIMESTAMP(timestamp)
    # PARTITION BY DAY WAL;
    # """.replace("\n", " ")

    # for _ in range(5):
    #     try:
    #         hc_result = requests.get(QUESTDB_HEALTHCHECK)
    #         if hc_result.ok:
    #             # logger.debug("Connected to database")
    #             break
    #     except:
    #         # logger.debug("Waiting to connect to database")
    #         time.sleep(3)

    # if not hc_result or not hc_result.ok:
    #     raise ConnectionError("Failed to connect to database")

    # # logger.debug(f"Initializing database with SQL:\n{sql}")
    # response = requests.get(QUESTDB_ENDPOINT, params={"query": sql.replace("\n", "")})
    # response.raise_for_status()
    # # logger.debug("Database initialized")
    # # yield
    # # logger.debug("Goodbye")

    print("hello, the lifespan function has been called...")
    conn = await connect(DATABASE_URL)
    try:
        sql = f"""
        CREATE TABLE IF NOT EXISTS {TABLE_NAME} (
            client_order_id STRING,
            symbol SYMBOL,
            side STRING,
            filled_qty DOUBLE,
            filled_avg_price DOUBLE,
            timestamp TIMESTAMP
        ) TIMESTAMP(timestamp)
        PARTITION BY DAY;
        """
        await conn.execute(sql)
        print("Table initialized successfully.")
        yield
    finally:
        await conn.close()


# Initialize FastAPI app with designated lifespan
app = FastAPI(lifespan=lifespan)

# Define endpoints

'''
NOTES: I heard people talking about using 'await' and then 'connect' from the asyncpg package, not 
quite sure what is the best way to make sure the sql query is actually sent to the api. 
'''

@app.post("/trades/")
async def add_trade(trades: dict):

    conn = await connect(DATABASE_URL)

    try:
        await conn.execute(f"""
        INSERT INTO {TABLE_NAME} (client_order_id, symbol, side, filled_qty, filled_avg_price, timestamp)
        VALUES ($1, $2, $3, $4, $5, $6);
        """, trades['client_order_id'], trades['symbol'], trades['side'], float(trades['filled_qty']), \
        float(trades['filled_avg_price']), datetime.fromisoformat(trades['timestamp']).replace(tzinfo=None))
        return {"status": "Trade successful"}

    finally:
         await conn.close()

@app.get("/trades/")
async def get_trades():
    conn = await connect(DATABASE_URL)
    try:
        rows_obj = await conn.fetch(f"SELECT * FROM {TABLE_NAME};")
        return [dict(row) for row in rows_obj]
    finally: 
        await conn.close()


