from typing import Dict, Optional
from utils.api import ExchangeAPI
from utils.logger import TradeLogger

class BondBot:
    def __init__(self, api: ExchangeAPI, logger: TradeLogger, fair_value: float = 1000.0):
        self.api = api
        self.logger = logger
        self.fair_value = fair_value
        self.buy_threshold = fair_value - 1.0  # Buy when price < 999
        self.sell_threshold = fair_value + 1.0  # Sell when price > 1001
        self.position = 0
        self.max_position = 100  # Maximum position size

    def get_best_prices(self, order_book: Dict) -> tuple[Optional[float], Optional[float]]:
        """Get the best bid and ask prices from the order book."""
        if not order_book:
            return None, None
        
        best_bid = order_book.get('bids', [{}])[0].get('price', None)
        best_ask = order_book.get('asks', [{}])[0].get('price', None)
        return best_bid, best_ask

    def execute_strategy(self, symbol: str = "BOND"):
        """Execute the bond trading strategy."""
        # Get current order book
        order_book = self.api.get_order_book(symbol)
        best_bid, best_ask = self.get_best_prices(order_book)

        if best_bid is None or best_ask is None:
            print("No valid prices in order book")
            return

        # Check if we should buy
        if best_ask < self.buy_threshold and self.position < self.max_position:
            size = min(10, self.max_position - self.position)  # Buy in chunks of 10
            response = self.api.place_order(symbol, "BUY", best_ask, size)
            if response:
                self.position += size
                self.logger.log_trade(symbol, "BUY", best_ask, size, response)

        # Check if we should sell
        if best_bid > self.sell_threshold and self.position > -self.max_position:
            size = min(10, self.max_position + self.position)  # Sell in chunks of 10
            response = self.api.place_order(symbol, "SELL", best_bid, size)
            if response:
                self.position -= size
                self.logger.log_trade(symbol, "SELL", best_bid, size, response)

        # Log current performance
        self.logger.log_performance(
            pnl=self.position * (self.fair_value - best_bid if self.position > 0 else best_ask - self.fair_value),
            positions={symbol: self.position}
        ) 