import numpy as np


def run_simulation(gbm, order_book, market_maker, num_steps):
    gbm_prices = []
    realized_pnl = []
    unrealized_pnl = []
    total_pnl = []

    for _ in range(num_steps):
        # 1️⃣ Update GBM Price
        if _ == 0:
            true_price = order_book.initial_price


        true_price = gbm.step()
        gbm_prices.append(true_price)

        # 2️⃣ Cancel outdated limit orders
        to_cancel = []
        for price in list(order_book.bids.keys()):
            if abs(price - true_price) / true_price > 0.03:
                to_cancel.append((price, "buy"))
        for price in list(order_book.asks.keys()):
            if abs(price - true_price) / true_price > 0.03:
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

        # 4️⃣ Market Maker places quotes
        market_maker.place_quotes()

        # 5️⃣ Execute market orders
        for _ in range(np.random.randint(1, 6)):
            size = np.random.randint(5, 15)
            side = np.random.choice(["buy", "sell"])
            order_book.execute_market_order(size, side, market_maker = market_maker)

        market_maker.total_pnl_hist.append(round(market_maker.total_pnl,2))
        market_maker.realized_pnl_hist.append(round(market_maker.realized_pnl,2))
        market_maker.unrealized_pnl_hist.append(round(market_maker.unrealized_pnl,2))

        # 6️⃣ Track PnL
        realized_pnl.append(market_maker.realized_pnl)
        unrealized_pnl.append(market_maker.unrealized_pnl)
        total_pnl.append(market_maker.total_pnl)

    return gbm_prices, total_pnl
