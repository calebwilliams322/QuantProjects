import numpy as np

class OrderBook:
    def __init__(self, initial_price=100.0):
        self.bids = {}   # {price: [{"size": size, "owner": owner}]}
        self.asks = {}  
        self.mid_price = initial_price
        self.initial_price = initial_price

        for i in range(5):
            bid_price = round(initial_price - 0.01 * (i + 1), 2)
            ask_price = round(initial_price + 0.01 * (i + 1), 2)
            bid_size = np.random.randint(5, 20)
            ask_size = np.random.randint(5, 20)
            self.bids[bid_price] = [{"size": bid_size, "owner": "investor"}]
            self.asks[ask_price] = [{"size": ask_size, "owner": "investor"}]

        self.update_mid_price()

    def update_mid_price(self):
        if self.bids and self.asks:
            best_bid = max(self.bids.keys())
            best_ask = min(self.asks.keys())
            self.mid_price = (best_bid + best_ask) / 2

    def add_limit_order(self, price, size, side, owner="investor"):
        book = self.bids if side == "buy" else self.asks
        if price not in book:
            book[price] = []
        
        book[price].append({"size": size, "owner": owner})


    def cancel_order(self, price, side):
        book = self.bids if side == "buy" else self.asks
        if price in book:
            del book[price]
        self.update_mid_price()

    def execute_market_order(self, size, side, market_maker = None):
        """
        Executes a market order, prioritizing price levels and reducing order sizes.
        Tracks whether the market maker's orders are filled.
        """
        book = self.asks if side == "buy" else self.bids
        price_levels = sorted(book.keys()) if side == "buy" else sorted(book.keys(), reverse=True)

        print(f"Market Order Size: {size}")

        remaining = size
        market_maker_fills = 0  # Track market maker fills


        for price in price_levels:
            if remaining <= 0:
                break
            
            # Execute orders at this price level
            new_orders = []
            for order in book[price]:  # Loop through orders at this price
                available = order["size"]  # Extract integer size
                trade_size = min(available, remaining)
                order["size"] -= trade_size
                remaining -= trade_size

                # Track market maker fills
                if market_maker and order["owner"] == "market_maker":
                    market_maker_fills += trade_size
                    market_maker.update_pnl(price, trade_size, side)

                # If there's remaining size, keep the order
                if order["size"] > 0:
                    new_orders.append(order)

            # Update or remove price level
            if new_orders:
                book[price] = new_orders
            else:
                del book[price]

        self.update_mid_price()

        # Print fill information for debugging
        if market_maker_fills > 0:
            print(f"✅ Market Maker filled {market_maker_fills} units on {side} market order.")


    def get_current_market_price(self): # mid price
        """ Estimates the current market price based on the best available bid/ask. """
        if self.bids and self.asks:
            return (max(self.bids.keys()) + min(self.asks.keys())) / 2  # Mid-price
        elif self.bids:  # No asks, use best bid
            return max(self.bids.keys())
        elif self.asks:  # No bids, use best ask
            return min(self.asks.keys())
        return self.mid_price



    def display_book(self):
        """Displays the order book in a structured table format."""
        print("\nOrder Book Snapshot:")
        print(f"{'Price':<10} {'Ask Size (Owner)':<20} {'Bid Size (Owner)':<20}")
        print("-" * 50)

        all_prices = sorted(set(self.bids.keys()) | set(self.asks.keys()), reverse=True)  # Fix: Use self.bids, self.asks

        for price in all_prices:
            ask_str = " - "
            bid_str = " - "
            
            if price in self.asks:
                ask_orders = [f"{order['size']} ({order['owner']})" for order in self.asks[price]]
                ask_str = ", ".join(ask_orders)
            
            if price in self.bids:
                bid_orders = [f"{order['size']} ({order['owner']})" for order in self.bids[price]]
                bid_str = ", ".join(bid_orders)
            
            print(f"{price:<10} {ask_str:<20} {bid_str:<20}")
        print("-" * 50)
