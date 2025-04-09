import asyncio
import signal
import sys
import os
from typing import Dict, Any
from utils.api import ExchangeAPI
from utils.logger import TradeLogger
from strategies.bond_bot import BondBot
from dotenv import load_dotenv

load_dotenv()

class TradingBot:
    def __init__(self):
        self.running = False
        self.api = ExchangeAPI()
        self.logger = TradeLogger()
        self.strategies = {
            'bond_bot': BondBot(self.api, self.logger)
        }

    async def validate_config(self) -> bool:
        """Validate configuration before starting."""
        required_vars = [
            'EXCHANGE_URL',
            'EXCHANGE_API_KEY',
            'BOND_FAIR_VALUE',
            'MAX_POSITION_SIZE',
            'TRADE_SIZE'
        ]
        
        missing_vars = [var for var in required_vars if not os.getenv(var)]
        if missing_vars:
            print(f"Error: Missing required environment variables: {', '.join(missing_vars)}")
            return False
        
        try:
            # Test API connection
            response = self.api.get_order_book("BOND")
            if not response:
                print("Error: Could not connect to exchange API")
                return False
        except Exception as e:
            print(f"Error testing API connection: {e}")
            return False
        
        return True

    async def monitor_performance(self):
        """Monitor and log performance metrics."""
        while self.running:
            try:
                for name, strategy in self.strategies.items():
                    stats = strategy.get_stats()
                    print(f"\n{name} Stats:")
                    print(f"Position: {stats['position']}")
                    print(f"Total Trades: {stats['total_trades']}")
                    print(f"Total Volume: {stats['total_volume']}")
                    print(f"Current P&L: {stats['pnl']:.2f}")
            except Exception as e:
                print(f"Error monitoring performance: {e}")
            await asyncio.sleep(5)  # Update every 5 seconds

    async def run_strategies(self):
        """Run all trading strategies."""
        while self.running:
            try:
                for strategy in self.strategies.values():
                    strategy.execute_strategy()
                await asyncio.sleep(0.25)  # 250ms between iterations
            except Exception as e:
                print(f"Error in strategy execution: {e}")
                await asyncio.sleep(1)  # Wait before retrying

    def handle_shutdown(self, signum, frame):
        """Handle shutdown signals."""
        print("\nShutting down trading bot...")
        self.running = False

    async def run(self):
        """Main entry point."""
        # Validate configuration
        if not await self.validate_config():
            sys.exit(1)

        # Set up signal handlers
        signal.signal(signal.SIGINT, self.handle_shutdown)
        signal.signal(signal.SIGTERM, self.handle_shutdown)

        print("Starting trading bot...")
        self.running = True

        try:
            # Run strategies and monitoring concurrently
            await asyncio.gather(
                self.run_strategies(),
                self.monitor_performance()
            )
        except Exception as e:
            print(f"Error in main loop: {e}")
        finally:
            print("Trading bot stopped.")

async def main():
    bot = TradingBot()
    await bot.run()

if __name__ == "__main__":
    asyncio.run(main()) 