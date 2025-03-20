import numpy as np
import pandas as pd
import yfinance as yf
from datetime import datetime
from options_data import fetch_call_options
from black_scholes import implied_volatility_call
import plotly.graph_objects as go


def compute_iv(row, risk_free_rate, dividend_yield):
    try:
        return implied_volatility_call(
            option_price=row['lastPrice'],
            S=row['underlying_price'],
            K=row['strike'],
            T=row['time_to_expiry'],
            r=risk_free_rate,
            q=dividend_yield
        )
    except:
        return np.nan

