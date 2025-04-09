import time
import asyncio
from utils.api import ExchangeAPI
from utils.logger import TradeLogger
from strategies.bond_bot import BondBot

async def main():
    # Initialize API client and logger
    api = ExchangeAPI()
    logger = TradeLogger()
    
    # Initialize trading strategies
    bond_bot = BondBot(api, logger)
    
    print("Starting trading bot...")
    
    try:
        while True:
            # Execute strategies
            bond_bot.execute_strategy()
            
            # Sleep for 250ms between iterations
            await asyncio.sleep(0.25)
            
    except KeyboardInterrupt:
        print("\nStopping trading bot...")
    except Exception as e:
        print(f"Error in main loop: {e}")

if __name__ == "__main__":
    asyncio.run(main()) 