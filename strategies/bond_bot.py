import os
from typing import Dict, Optional, Tuple
from utils.api import ExchangeAPI
from utils.logger import TradeLogger
from dotenv import load_dotenv

load_dotenv()

class BondBot:
    def __init__(self, api: ExchangeAPI, logger: TradeLogger):
        self.api = api
        self.logger = logger
        
        # Load configuration from environment variables
        self.fair_value = float(os.getenv('BOND_FAIR_VALUE', '1000.0'))
        self.max_position = int(os.getenv('MAX_POSITION_SIZE', '100'))
        self.trade_size = int(os.getenv('TRADE_SIZE', '10'))
        self.buy_threshold = self.fair_value - 1.0
        self.sell_threshold = self.fair_value + 1.0
        
        # Initialize state
        self.position = 0
        self.total_trades = 0
        self.total_volume = 0
        self.pnl = 0.0
        
        # Load saved state if exists
        self._load_state()

    def _load_state(self):
        """Load saved state from file if exists."""
        try:
            state_file = 'data/bond_bot_state.json'
            if os.path.exists(state_file):
                import json
                with open(state_file, 'r') as f:
                    state = json.load(f)
                    self.position = state.get('position', 0)
                    self.total_trades = state.get('total_trades', 0)
                    self.total_volume = state.get('total_volume', 0)
                    self.pnl = state.get('pnl', 0.0)
        except Exception as e:
            print(f"Error loading state: {e}")

    def _save_state(self):
        """Save current state to file."""
        try:
            state_file = 'data/bond_bot_state.json'
            import json
            state = {
                'position': self.position,
                'total_trades': self.total_trades,
                'total_volume': self.total_volume,
                'pnl': self.pnl
            }
            with open(state_file, 'w') as f:
                json.dump(state, f)
        except Exception as e:
            print(f"Error saving state: {e}")

    def get_best_prices(self, order_book: Dict) -> Tuple[Optional[float], Optional[float]]:
        """Get the best bid and ask prices from the order book."""
        if not order_book:
            return None, None
        
        try:
            best_bid = order_book.get('bids', [{}])[0].get('price', None)
            best_ask = order_book.get('asks', [{}])[0].get('price', None)
            return best_bid, best_ask
        except (IndexError, KeyError) as e:
            print(f"Error parsing order book: {e}")
            return None, None

    def calculate_pnl(self, current_price: float) -> float:
        """Calculate current P&L based on position and current price."""
        if self.position > 0:
            return self.position * (current_price - self.fair_value)
        elif self.position < 0:
            return self.position * (self.fair_value - current_price)
        return 0.0

    def execute_strategy(self, symbol: str = "BOND"):
        """Execute the bond trading strategy."""
        try:
            # Get current order book
            order_book = self.api.get_order_book(symbol)
            best_bid, best_ask = self.get_best_prices(order_book)

            if best_bid is None or best_ask is None:
                print("No valid prices in order book")
                return

            # Update P&L
            self.pnl = self.calculate_pnl(best_bid if self.position > 0 else best_ask)

            # Check if we should buy
            if best_ask < self.buy_threshold and self.position < self.max_position:
                size = min(self.trade_size, self.max_position - self.position)
                response = self.api.place_order(symbol, "BUY", best_ask, size)
                if response:
                    self.position += size
                    self.total_trades += 1
                    self.total_volume += size
                    self.logger.log_trade(symbol, "BUY", best_ask, size, response)

            # Check if we should sell
            if best_bid > self.sell_threshold and self.position > -self.max_position:
                size = min(self.trade_size, self.max_position + self.position)
                response = self.api.place_order(symbol, "SELL", best_bid, size)
                if response:
                    self.position -= size
                    self.total_trades += 1
                    self.total_volume += size
                    self.logger.log_trade(symbol, "SELL", best_bid, size, response)

            # Log current performance
            self.logger.log_performance(
                pnl=self.pnl,
                positions={symbol: self.position}
            )

            # Save state
            self._save_state()

        except Exception as e:
            print(f"Error in bond strategy execution: {e}")

    def get_stats(self) -> Dict:
        """Get current strategy statistics."""
        return {
            'position': self.position,
            'total_trades': self.total_trades,
            'total_volume': self.total_volume,
            'pnl': self.pnl,
            'fair_value': self.fair_value,
            'buy_threshold': self.buy_threshold,
            'sell_threshold': self.sell_threshold
        } 