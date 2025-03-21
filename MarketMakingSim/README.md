# Market Making Simulator

This project is a simulation of a simplified financial market that models an order book and the behavior of a basic market maker. It is designed to help visualize how liquidity is provided, how market orders interact with limit orders, and how a market maker can generate profit by capturing the bid-ask spread.

## Core Components

### Order Book
- Stores **limit orders** (bids and asks) at various price levels.
- Executes **market orders** by sweeping through available price levels.
- Dynamically calculates and updates the **mid-price** after each event.
- Supports **cancellation** of existing orders.

### Market Maker
- Posts **limit bid and ask orders** at a fixed spread around the mid-price.
- Reacts to changes in the mid-price by canceling and reposting quotes.
- Ensures continuous liquidity in the book and competes with investor orders.

### Investor Behavior
- Random investors generate activity in each simulation step:
  - **Limit Orders**: placed at random prices near the mid.
  - **Market Orders**: executed immediately against the book.
  - **Cancellations**: randomly remove existing orders.

## 🔄 Simulation Flow
1. Market maker posts bid/ask quotes.
2. Random investor activity is simulated.
3. The order book executes and updates.
4. Market maker reacts and adjusts quotes.

## 🚀 Future Features
- Profit and Loss (PnL) tracking.
- Inventory-aware market making strategies.
- Spread adjustment based on market volatility.
- Order book visualization tools.

---

This project is ideal for learning about order-driven markets, liquidity provision, and market structure dynamics.
