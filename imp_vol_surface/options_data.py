import yfinance as yf
import pandas as pd


def fetch_call_options(ticker_symbol, expiration_date=None):
    ticker = yf.Ticker(ticker_symbol)

    if expiration_date is None:
        expiration_date = ticker.options[0]  # Nearest expiration by default

    calls_df = ticker.option_chain(expiration_date).calls
    return calls_df