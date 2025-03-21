class MarketMaker:
    def __init__(self, order_book, strategy, size=10):
        """
        Parameters:
        - order_book: the OrderBook object
        - strategy: a callable that takes (order_book, size) and returns (bid_price, ask_price)
        - size: quantity of each order
        """
        self.order_book = order_book
        self.strategy = strategy
        self.size = size
        self.current_bid = None
        self.current_ask = None
        self.realized_pnl = 0  # Track accumulated PnL
        self.inventory = 0  # Track net position
        self.total_pnl = 0
        self.total_pnl_hist = []
        self.realized_pnl_hist = []
        self.unrealized_pnl = 0
        self.unrealized_pnl_hist = []

    def update_pnl(self, price, size, side):
        """ Updates PnL when market orders execute against the MM. """
        if side == "buy":  # MM is selling at ask price
            self.realized_pnl += size * price # Revenue from selling
            self.inventory -= size  # Reduce position
        elif side == "sell":  # MM is buying at bid price
            self.realized_pnl -= size * price  # Cost from buying
            self.inventory +=  size # Increase position

        self.unrealized_pnl = self.inventory * (self.order_book.get_current_market_price())

        self.total_pnl = self.inventory * (self.order_book.get_current_market_price()) + self.realized_pnl
        

    def place_quotes(self):
        if not self.order_book.bids or not self.order_book.asks:
            return

        best_bid = max(self.order_book.bids.keys())
        best_ask = min(self.order_book.asks.keys())

        # Market maker takes whatever is available, ensuring two decimal places
        bid_price = round(best_bid + 0.01, 2)  # Just below best ask
        ask_price = round(best_ask - 0.01, 2)  # Just above best bid

        # Ensure no crossed market
        if bid_price >= ask_price:
            return  # Skip placing orders if they would cross the spread

        # Cancel old orders
        if self.current_bid is not None:
            self.order_book.cancel_order(self.current_bid, "buy")
        if self.current_ask is not None:
            self.order_book.cancel_order(self.current_ask, "sell")

        # Place new market maker orders
        self.order_book.add_limit_order(bid_price, self.size, "buy", owner="market_maker")
        self.order_book.add_limit_order(ask_price, self.size, "sell", owner="market_maker")

        self.current_bid = bid_price
        self.current_ask = ask_price


def fixed_spread_strategy(order_book, size, spread=0.10):
    if not order_book.bids or not order_book.asks:
        return None, None  # Avoid placing quotes if the book is empty
    
    best_bid = max(order_book.bids.keys())
    best_ask = min(order_book.asks.keys())
    mid_price = (best_bid + best_ask) / 2
    return round(mid_price - spread / 2, 2), round(mid_price + spread / 2, 2)

