# QuantProjects: Black-Scholes Option Pricer & Sensitivity Analysis Heatmaps

## Overview

This project is a quant pet project that demonstrates a comprehensive implementation of the Black-Scholes option pricing model integrated into an interactive web application using Streamlit. The app includes:

- **Black-Scholes Pricing:** Calculate call and put option prices using the Black-Scholes formula.
- **Interactive GUI:** Adjust fixed parameters (underlying price, strike, risk-free rate, dividend yield, time to expiry, volatility) via the sidebar.
- **Base Price Display:** View the computed base call and put option prices in custom grey "bubbles".
- **Sensitivity Analysis:** Generate heatmaps showing how option prices vary over a grid of underlying prices and volatilities.
- **PnL Analysis:** Toggle and input purchase prices to display PnL heatmaps (the difference between the Black-Scholes price and market price).
- **Data Persistence:** Save each calculation's parameters and results in a SQLite database.
- **User Directions:** Access instructions via an expandable section.
- **Deployment Ready:** Includes a Dockerfile for containerized deployment.

## Features

- **Interactive Inputs:** Easily modify parameters via a sidebar.
- **Dynamic Heatmaps:** View real-time updates of option prices and PnL across a defined grid.
- **Data Persistence:** Log calculations to an SQLite database for later review.
- **User-Friendly Interface:** Includes clear directions and visually appealing design.
- **Docker Deployment:** Easily containerize and deploy the app.

## Installation

1. **Clone the Repository:**

   ```bash
   git clone <repository_url>
   cd QuantProjects
