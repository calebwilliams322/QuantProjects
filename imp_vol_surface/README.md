# Implied Volatility Surface Visualizer

This project is an interactive quantitative finance tool designed to generate and visualize implied volatility surfaces for call options based on real-time data retrieved from Yahoo Finance. The implied volatility surface helps traders and analysts visualize market expectations regarding future volatility across different strike prices and maturities.

---

## 📌 **Project Overview**

This project allows users to:

- Input any stock ticker symbol (e.g., `AAPL`, `MSFT`).
- Retrieve real-time option chain data from Yahoo Finance.
- Compute the implied volatility for each available call option using the Black–Scholes model.
- Generate an interactive 3D surface plot of implied volatility:
  - **X-axis**: Time to expiry (maturity).
  - **Y-axis**: Strike price or moneyness (configurable).
  - **Z-axis**: Implied volatility (color-coded for clarity).

---

## 🚀 **Getting Started**

### **Step 1: Clone the repository**
```bash
git clone https://github.com/<your_username>/QuantProjects.git
cd QuantProjects/imp_vol_surface
