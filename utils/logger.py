import csv
import os
from datetime import datetime
from typing import Dict, Any

class TradeLogger:
    def __init__(self, log_dir: str = 'data'):
        self.log_dir = log_dir
        self.trades_file = os.path.join(log_dir, 'trades.csv')
        self.performance_file = os.path.join(log_dir, 'performance.csv')
        
        # Create log directory if it doesn't exist
        os.makedirs(log_dir, exist_ok=True)
        
        # Initialize trade log file
        if not os.path.exists(self.trades_file):
            with open(self.trades_file, 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(['timestamp', 'symbol', 'order_type', 'price', 'size', 'response'])

        # Initialize performance log file
        if not os.path.exists(self.performance_file):
            with open(self.performance_file, 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(['timestamp', 'pnl', 'positions'])

    def log_trade(self, symbol: str, order_type: str, price: float, size: int, response: Dict[str, Any]):
        """Log a trade execution."""
        with open(self.trades_file, 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([
                datetime.now().isoformat(),
                symbol,
                order_type,
                price,
                size,
                str(response)
            ])

    def log_performance(self, pnl: float, positions: Dict[str, int]):
        """Log current performance metrics."""
        with open(self.performance_file, 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([
                datetime.now().isoformat(),
                pnl,
                str(positions)
            ])

    def get_trade_history(self) -> list:
        """Get the trade history."""
        trades = []
        with open(self.trades_file, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                trades.append(row)
        return trades

    def get_performance_history(self) -> list:
        """Get the performance history."""
        performance = []
        with open(self.performance_file, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                performance.append(row)
        return performance 