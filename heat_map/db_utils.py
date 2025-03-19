import psycopg2
import pandas as pd

DB_NAME = "heat_map_db"
DB_USER = "postgres"
DB_PASSWORD = ""
DB_HOST = "localhost"  # or your remote host
DB_PORT = 5432         # default PostgreSQL port

def init_db():
    """Initializes the PostgreSQL database and creates the tables if they don't exist."""
    conn = psycopg2.connect(
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT
    )
    cur = conn.cursor()

    # Create the inputs table
    cur.execute("""
    CREATE TABLE IF NOT EXISTS black_scholes_inputs (
        calculation_id SERIAL PRIMARY KEY,
        stock_price       DECIMAL(18,9) NOT NULL,
        strike_price      DECIMAL(18,9) NOT NULL,
        interest_rate     DECIMAL(18,9) NOT NULL,
        volatility        DECIMAL(18,9) NOT NULL,
        time_to_expiry    DECIMAL(18,9) NOT NULL
    );
    """)

    # Create the outputs table
    cur.execute("""
    CREATE TABLE IF NOT EXISTS black_scholes_outputs (
        calculation_output_id SERIAL PRIMARY KEY,
        volatility_shock    DECIMAL(18,9) NOT NULL,
        stock_price_shock   DECIMAL(18,9) NOT NULL,
        option_price        DECIMAL(18,9) NOT NULL,
        is_call             BOOLEAN       NOT NULL,
        calculation_id      INT           NOT NULL,
        FOREIGN KEY (calculation_id)
            REFERENCES black_scholes_inputs(calculation_id)
            ON DELETE CASCADE
            ON UPDATE CASCADE
    );
    """)

    conn.commit()
    cur.close()
    conn.close()



def insert_black_scholes_input(stock_price, strike_price, interest_rate, volatility, time_to_expiry):
    """Insert a single row into black_scholes_inputs and return the new calculation_id."""
    conn = psycopg2.connect(
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT
    )
    cur = conn.cursor()
    cur.execute("""
    INSERT INTO black_scholes_inputs (stock_price, strike_price, interest_rate, volatility, time_to_expiry)
    VALUES (%s, %s, %s, %s, %s)
    RETURNING calculation_id
    """, (stock_price, strike_price, interest_rate, volatility, time_to_expiry))
    
    new_id = cur.fetchone()[0]
    conn.commit()
    cur.close()
    conn.close()
    return new_id

def insert_black_scholes_output(calculation_id, volatility_shock, stock_price_shock, option_price, is_call):
    """Insert a single row into black_scholes_outputs for a given calculation_id."""
    conn = psycopg2.connect(
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT
    )
    cur = conn.cursor()
    cur.execute("""
    INSERT INTO black_scholes_outputs (calculation_id, volatility_shock, stock_price_shock, option_price, is_call)
    VALUES (%s, %s, %s, %s, %s)
    """, (calculation_id, volatility_shock, stock_price_shock, option_price, is_call))
    conn.commit()
    cur.close()
    conn.close()

def get_all_inputs():
    """Retrieve all rows from the black_scholes_inputs table as a DataFrame."""
    conn = psycopg2.connect(
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT
    )
    # Use pandas read_sql_query to retrieve data as a DataFrame
    df = pd.read_sql_query("SELECT * FROM black_scholes_inputs ORDER BY calculation_id DESC", conn)
    conn.close()
    return df
