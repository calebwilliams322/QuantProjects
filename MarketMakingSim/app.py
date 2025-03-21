import streamlit as st
import numpy as np
from GBM import GBMSimulator
from OrderBook import OrderBook
from MarketMaker import MarketMaker, fixed_spread_strategy
from simulation_generator import run_simulation
from visualization import MarketMakerVisualizer

# Streamlit App Title
st.title("Market-Making Simulator")

# Sidebar for simulation parameters
st.sidebar.header("Simulation Parameters")

num_steps = st.sidebar.slider("Number of Steps", min_value=10, max_value=1000, value=50, step=10)
initial_price = st.sidebar.number_input("Initial Price", min_value=50.0, max_value=200.0, value=100.0, step=1.0)
mu = st.sidebar.slider("Drift (μ)", min_value=-0.1, max_value=0.1, value=0.05, step=0.01)
sigma = st.sidebar.slider("Volatility (σ)", min_value=0.01, max_value=0.5, value=0.15, step=0.01)
spread = st.sidebar.slider("Market Maker Spread", min_value=0.01, max_value=1.0, value=0.10, step=0.01)
size = st.sidebar.slider("Order Size", min_value=5, max_value=50, value=25, step=5)

# Button to run simulation
if st.sidebar.button("Run Simulation"):
    st.subheader("Please wait while we simulate Market-Making...")
    
    # Initialize GBM simulator and order book
    gbm = GBMSimulator(S0=initial_price, mu=mu, sigma=sigma, dt=1.0/num_steps)
    order_book = OrderBook(initial_price=initial_price)

    # Initialize Market Maker
    market_maker = MarketMaker(order_book, lambda ob, s: fixed_spread_strategy(ob, s, spread=spread), size=size)

    # Run the simulation
    gbm_prices, total_pnl = run_simulation(gbm, order_book, market_maker, num_steps)



    # Display animated PnL visualization
    st.subheader("Market Maker PnL Over Time")
    visualizer = MarketMakerVisualizer(gbm_prices, total_pnl)
    # visualizer.save_animation("animation.mp4")
    # st.video("animation.mp4")   

    visualizer.save_animation("animation.gif")  # Save as GIF
    st.image("animation.gif")
