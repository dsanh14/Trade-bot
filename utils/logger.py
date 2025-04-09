import csv
import os
import gzip
import shutil
from datetime import datetime
from typing import Dict, Any, Optional
from pathlib import Path

class TradeLogger:
    def __init__(self, log_dir: str = 'data', max_file_size: int = 10 * 1024 * 1024):  # 10MB
        self.log_dir = Path(log_dir)
        self.trades_file = self.log_dir / 'trades.csv'
        self.performance_file = self.log_dir / 'performance.csv'
        self.max_file_size = max_file_size
        
        # Create log directory if it doesn't exist
        self.log_dir.mkdir(parents=True, exist_ok=True)
        
        # Initialize log files
        self._init_log_file(self.trades_file, ['timestamp', 'symbol', 'order_type', 'price', 'size', 'response'])
        self._init_log_file(self.performance_file, ['timestamp', 'pnl', 'positions'])

    def _init_log_file(self, file_path: Path, headers: list):
        """Initialize a log file with headers if it doesn't exist."""
        if not file_path.exists():
            try:
                with open(file_path, 'w', newline='') as f:
                    writer = csv.writer(f)
                    writer.writerow(headers)
            except IOError as e:
                print(f"Error initializing log file {file_path}: {e}")

    def _rotate_file(self, file_path: Path):
        """Rotate log file if it exceeds max size."""
        if file_path.exists() and file_path.stat().st_size > self.max_file_size:
            try:
                # Create backup with timestamp
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                backup_path = file_path.parent / f"{file_path.stem}_{timestamp}.csv.gz"
                
                # Compress and move the file
                with open(file_path, 'rb') as f_in:
                    with gzip.open(backup_path, 'wb') as f_out:
                        shutil.copyfileobj(f_in, f_out)
                
                # Clear the original file and write headers
                with open(file_path, 'w', newline='') as f:
                    writer = csv.writer(f)
                    writer.writerow(['timestamp', 'symbol', 'order_type', 'price', 'size', 'response'])
                
                # Keep only last 5 backups
                backups = sorted(file_path.parent.glob(f"{file_path.stem}_*.csv.gz"))
                if len(backups) > 5:
                    for old_backup in backups[:-5]:
                        old_backup.unlink()
            except IOError as e:
                print(f"Error rotating log file {file_path}: {e}")

    def log_trade(self, symbol: str, order_type: str, price: float, size: int, response: Dict[str, Any]):
        """Log a trade execution."""
        try:
            self._rotate_file(self.trades_file)
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
        except IOError as e:
            print(f"Error logging trade: {e}")

    def log_performance(self, pnl: float, positions: Dict[str, int]):
        """Log current performance metrics."""
        try:
            self._rotate_file(self.performance_file)
            with open(self.performance_file, 'a', newline='') as f:
                writer = csv.writer(f)
                writer.writerow([
                    datetime.now().isoformat(),
                    pnl,
                    str(positions)
                ])
        except IOError as e:
            print(f"Error logging performance: {e}")

    def get_trade_history(self) -> list:
        """Get the trade history."""
        trades = []
        try:
            with open(self.trades_file, 'r') as f:
                reader = csv.DictReader(f)
                trades = list(reader)
        except IOError as e:
            print(f"Error reading trade history: {e}")
        return trades

    def get_performance_history(self) -> list:
        """Get the performance history."""
        performance = []
        try:
            with open(self.performance_file, 'r') as f:
                reader = csv.DictReader(f)
                performance = list(reader)
        except IOError as e:
            print(f"Error reading performance history: {e}")
        return performance 