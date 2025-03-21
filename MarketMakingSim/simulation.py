from OrderBook import OrderBook
from MarketMaker import MarketMaker, fixed_spread_strategy
from GBM import GBMSimulator
import numpy as np
import time
import matplotlib.pyplot as plt
from visualization import MarketMakerVisualizer

# --- Config ---
NUM_STEPS = 50
INITIAL_PRICE = 100.0
MU = 0.05
SIGMA = 0.15
DT = 1.0/NUM_STEPS

# --- Initialize components ---
gbm = GBMSimulator(S0=INITIAL_PRICE, mu=MU, sigma=SIGMA, dt=DT)
order_book = OrderBook(initial_price=INITIAL_PRICE)
market_maker = MarketMaker(order_book, lambda ob, s: fixed_spread_strategy(ob, s, spread=0.10), size=30)


gbm_prices = []
realized_pnls = []
unrealized_pnls = []
total_pnls = []


# --- Simulation loop ---
for t in range(NUM_STEPS):
    print(f"\n--- Time Step {t} ---")

    # 1. Advance GBM price
    if t != 0:
        true_price = gbm.step()
        print(f"Current GBM price: {true_price}")
    else:
        print(f"Current GBM price: {INITIAL_PRICE}")
        true_price = INITIAL_PRICE

    # 2. Cancel outdated limit orders (e.g., far from GBM)
    to_cancel = []
    for price in list(order_book.bids.keys()):
        if abs(price - true_price) / true_price > 0.03:
            to_cancel.append((price, "buy"))
        if price >= true_price:  # Bids cannot be above the true price
            to_cancel.append((price, "buy"))
    for price in list(order_book.asks.keys()):
        if abs(price - true_price) / true_price > 0.03:
            to_cancel.append((price, "sell"))
        if price <= true_price:  # Asks cannot be below the true price
            to_cancel.append((price, "sell"))
    for price, side in to_cancel:
        order_book.cancel_order(price, side)

    # 3. Add new random investor limit orders (near GBM)
    num_bids = np.random.randint(10, 20)
    for _ in range(num_bids):
        price = round(np.random.normal(loc=true_price*.99, scale=0.05), 2)
        size = np.random.randint(5, 20)
        side = "buy"

        # 20% chance the investor places a more aggressive bid
        if np.random.rand() < 0.20 and order_book.bids:
            price = round(max(order_book.bids.keys()) + 0.01, 2)  # Outbids best bid

        # Ensure no crossed market
        if order_book.asks and price >= min(order_book.asks.keys()):
            continue  # Skip this bid if it's too high

        order_book.add_limit_order(price, size, side)

    # Ensure 5-10 sell limit orders
    num_asks = np.random.randint(10, 20)
    for _ in range(num_asks):
        price = round(np.random.normal(loc=true_price*1.01, scale=0.05), 2)
        size = np.random.randint(5, 20)
        side = "sell"

        # 20% chance the investor places a more aggressive ask
        if np.random.rand() < 0.20 and order_book.asks:
            price = round(min(order_book.asks.keys()) - 0.01, 2)  # Undercuts best ask

        # Ensure no crossed market
        if order_book.bids and price <= max(order_book.bids.keys()):
            continue  # Skip this ask if it's too low

        order_book.add_limit_order(price, size, side)

    market_maker.place_quotes()

    # order_book.display_book()

    # 4. Execute some market orders
    for _ in range(np.random.randint(1, 6)):
        size = np.random.randint(5, 15)
        side = np.random.choice(["buy", "sell"])
        order_book.execute_market_order(size, side, market_maker=market_maker)

    market_maker.total_pnl_hist.append(round(market_maker.total_pnl,2))
    market_maker.realized_pnl_hist.append(round(market_maker.realized_pnl,2))
    market_maker.unrealized_pnl_hist.append(round(market_maker.unrealized_pnl,2))


    # 5. Show current order book
    # order_book.display_book()
    print(f"✅ Market Maker realized PnL: {market_maker.realized_pnl:.2f}, total (unrealized + realized) PnL: {market_maker.total_pnl:.2f}, Inventory: {market_maker.inventory}")
    gbm_prices.append(true_price)
    realized_pnls.append(market_maker.realized_pnl)
    unrealized_pnls.append(market_maker.unrealized_pnl)
    total_pnls.append(market_maker.total_pnl)


    # time.sleep(1)

visualizer = MarketMakerVisualizer(gbm_prices, total_pnls)
plt.show()
