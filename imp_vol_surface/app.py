# app.py
import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime
from options_data import fetch_call_options
from black_scholes import implied_volatility_call
from build_iv_surface import compute_iv
import plotly.graph_objects as go

# App Title
st.title("Interactive Implied Volatility Surface")

# Sidebar inputs for user configuration
st.sidebar.header("Configure Parameters")

ticker_symbol = st.sidebar.text_input("Ticker Symbol", "AAPL")
risk_free_rate = st.sidebar.number_input("Risk-free Rate (annual)", min_value=0.0, max_value=0.2, value=0.05, step=0.005)
dividend_yield = st.sidebar.number_input("Dividend Yield (annual)", min_value=0.0, max_value=0.1, value=0.0, step=0.005)

# Button to trigger calculation
if st.sidebar.button("Calculate Vol Surface"):
    with st.spinner('Fetching data and calculating volatility...'):
        
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

        options_df['implied_volatility'] = options_df.apply(compute_iv, axis=1)
        options_df.dropna(subset=['implied_volatility'], inplace=True)

        pivot_iv_surface = options_df.pivot_table(
            index='strike',
            columns='days_to_expiry',
            values='implied_volatility'
        )

        pivot_iv_surface_clean = pivot_iv_surface.dropna(axis=0, how='any').dropna(axis=1, how='any')

        strikes = pivot_iv_surface_clean.index.values
        expirations = pivot_iv_surface_clean.columns.values
        iv_values = pivot_iv_surface_clean.values

        # Interactive Plotly 3D plot
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

        st.plotly_chart(fig, use_container_width=True)

