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
from scipy.interpolate import griddata

# App Title
st.title("Interactive Implied Volatility Surface")

# Sidebar inputs for user configuration
st.sidebar.header("Configure Parameters")

ticker_symbol = st.sidebar.text_input("Ticker Symbol", "AAPL")
risk_free_rate = st.sidebar.number_input("Risk-free Rate (annual)", min_value=0.0, max_value=0.2, value=0.05, step=0.005)
dividend_yield = st.sidebar.number_input("Dividend Yield (annual)", min_value=0.0, max_value=0.1, value=0.0, step=0.005)
y_axis_choice = st.sidebar.selectbox(
    "Y-axis Data:",
    ["Strike Price ($)", "Moneyness (%)"]
)
min_strike_pct = st.sidebar.number_input(
    "Minimum Strike (% of Spot Price)", min_value=50.0, max_value=100.0, value=70.0, step=1.0
)

max_strike_pct = st.sidebar.number_input(
    "Maximum Strike (% of Spot Price)", min_value=100.0, max_value=200.0, value=130.0, step=1.0
)



# Button to trigger calculation
if st.sidebar.button("Calculate Vol Surface"):
    with st.spinner('Fetching data and calculating volatility...'):

        try:
            ticker = yf.Ticker(ticker_symbol)
            expirations = ticker.options
            if not expirations:
                st.error("No option data available for the provided ticker.")
                st.stop()
        except Exception as e:
            st.error(f"Failed to fetch data for ticker {ticker_symbol}: {e}")
            st.stop()
        
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
        options_df = options_df[options_df['days_to_expiry'] >= 7]

        options_df['implied_volatility'] = options_df.apply(compute_iv, axis=1, args=(risk_free_rate, dividend_yield))
        # Moneyness as percentage (strike price / underlying price * 100)
        options_df['moneyness'] = (options_df['strike'] / options_df['underlying_price']) * 100

        min_strike = current_price * (min_strike_pct / 100)
        max_strike = current_price * (max_strike_pct / 100)

        # Apply filtering clearly
        options_df = options_df[
        (options_df['strike'] >= min_strike) & 
        (options_df['strike'] <= max_strike)
        ]

        options_df.dropna(subset=['implied_volatility'], inplace=True)

        if y_axis_choice == "Strike Price ($)":
            y_axis_column = 'strike'
            y_label = 'Strike Price ($)'
        else:
            y_axis_column = 'moneyness'
            y_label = 'Moneyness (%)'

        pivot_iv_surface = options_df.pivot_table(
            index=y_axis_column,
            columns='days_to_expiry',
            values='implied_volatility'
        )

        pivot_iv_surface.columns = pivot_iv_surface.columns.astype(float)
        pivot_iv_surface_clean = pivot_iv_surface.dropna(axis=0, how='any').dropna(axis=1, how='any')

        expirations_numeric = pivot_iv_surface_clean.columns.values.astype(float)


        # Original discrete data points
        points = np.array([
            (row['days_to_expiry'], row[y_axis_column]) 
            for idx, row in options_df.iterrows()
        ])
        values = options_df['implied_volatility'].values
        y_values = pivot_iv_surface_clean.index.values
        

        # Define a regular grid over the entire data range (adjust '50j' for more resolution)
        grid_x, grid_y = np.mgrid[
            min(expirations_numeric):max(expirations_numeric):50j,  # X-axis (Days to expiry)
            min(y_values):max(y_values):50j         # Y-axis (Strike/Moneyness)
        ]

        # Smooth the implied volatility surface using cubic interpolation
        smoothed_iv = griddata(points, values, (grid_x, grid_y), method='cubic')

        # Plot smoothed implied volatility surface
        fig = go.Figure(data=[go.Surface(
            z=smoothed_iv,
            x=grid_x[:, 0],
            y=grid_y[0, :],
            colorscale='Viridis'
        )])


        fig.update_layout(
            title=f'Implied Volatility Surface for {ticker_symbol}',
            scene=dict(
                xaxis_title='Days to Expiry',
                yaxis_title=y_axis_choice,
                zaxis_title='Implied Volatility'
            ),
            autosize=False,
            width=800,
            height=700,
        )

        st.plotly_chart(fig, use_container_width=True)

