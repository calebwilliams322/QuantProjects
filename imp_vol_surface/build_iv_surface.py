import numpy as np
import pandas as pd
import yfinance as yf
from datetime import datetime
from options_data import fetch_call_options
from black_scholes import implied_volatility_call
import matplotlib.pyplot as plt
import plotly.graph_objects as go

# Configuration / Assumptions
ticker_symbol = 'AAPL'
risk_free_rate = 0.05  # Example value
dividend_yield = 0.0   # Example value


ticker = yf.Ticker(ticker_symbol)
expirations = ticker.options

all_calls = []
current_price = ticker.history().iloc[-1]['Close']
today = datetime.now()

for exp in expirations:
    calls = fetch_call_options(ticker_symbol, exp)
    exp_date = datetime.strptime(exp, '%Y-%m-%d')
    calls['expiration'] = exp_date
    calls['days_to_expiry'] = (exp_date - today).days
    calls['time_to_expiry'] = calls['days_to_expiry'] / 365.0
    calls['underlying_price'] = current_price
    all_calls.append(calls)

options_df = pd.concat(all_calls).reset_index(drop=True)


def compute_iv(row):
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

options_df['implied_volatility'] = options_df.apply(compute_iv, axis=1)
options_df.dropna(subset=['implied_volatility'], inplace=True)


pivot_iv_surface = options_df.pivot_table(
    index='strike', 
    columns='days_to_expiry', 
    values='implied_volatility'
)

pivot_iv_surface_clean = pivot_iv_surface.dropna(axis=0, how='any').dropna(axis=1, how='any')

# Prepare axes data
strikes = pivot_iv_surface_clean.index.values
expirations = pivot_iv_surface_clean.columns.values
iv_values = pivot_iv_surface_clean.values

# Create 3D surface plot
fig = go.Figure(data=[go.Surface(
    z=iv_values,
    x=expirations,
    y=strikes,
    colorscale='Viridis'
)])

fig.update_layout(
    title=f'Implied Volatility Surface for {ticker_symbol}',
    scene=dict(
        xaxis_title='Days to Expiry',
        yaxis_title='Strike Price',
        zaxis_title='Implied Volatility'
    ),
    autosize=False,
    width=800,
    height=700,
)

fig.show()