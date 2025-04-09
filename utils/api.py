import requests
import os
import time
from typing import Dict, List, Optional, Union
from dotenv import load_dotenv
from functools import wraps

load_dotenv()

def retry(max_retries: int = 3, delay: float = 1.0):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(max_retries):
                try:
                    return func(*args, **kwargs)
                except requests.exceptions.RequestException as e:
                    if attempt == max_retries - 1:
                        raise
                    time.sleep(delay * (attempt + 1))
            return None
        return wrapper
    return decorator

class ExchangeAPI:
    def __init__(self, base_url: str = None, api_key: str = None):
        self.base_url = base_url or os.getenv('EXCHANGE_URL', 'http://localhost:8000')
        self.api_key = api_key or os.getenv('EXCHANGE_API_KEY')
        self.session = requests.Session()
        self.session.headers.update({
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json'
        })
        self.last_request_time = 0
        self.min_request_interval = 0.25  # 250ms between requests

    def _rate_limit(self):
        """Ensure we don't exceed rate limits."""
        current_time = time.time()
        time_since_last_request = current_time - self.last_request_time
        if time_since_last_request < self.min_request_interval:
            time.sleep(self.min_request_interval - time_since_last_request)
        self.last_request_time = time.time()

    @retry(max_retries=3)
    def get_order_book(self, symbol: str) -> Dict[str, List[Dict[str, Union[float, int]]]]:
        """Get the current order book for a symbol."""
        self._rate_limit()
        try:
            response = self.session.get(f'{self.base_url}/book/{symbol}')
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error getting order book for {symbol}: {e}")
            return {'bids': [], 'asks': []}

    @retry(max_retries=3)
    def place_order(self, symbol: str, direction: str, price: float, size: int) -> Dict[str, Union[str, float, int]]:
        """Place a new order."""
        self._rate_limit()
        try:
            data = {
                'symbol': symbol,
                'direction': direction,
                'price': price,
                'size': size
            }
            response = self.session.post(f'{self.base_url}/orders', json=data)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error placing order for {symbol}: {e}")
            return {}

    @retry(max_retries=3)
    def cancel_order(self, order_id: str) -> bool:
        """Cancel an existing order."""
        self._rate_limit()
        try:
            response = self.session.post(f'{self.base_url}/cancel', json={'order_id': order_id})
            response.raise_for_status()
            return True
        except requests.exceptions.RequestException as e:
            print(f"Error canceling order {order_id}: {e}")
            return False

    @retry(max_retries=3)
    def get_positions(self) -> List[Dict[str, Union[str, int]]]:
        """Get current positions."""
        self._rate_limit()
        try:
            response = self.session.get(f'{self.base_url}/positions')
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error getting positions: {e}")
            return []

    @retry(max_retries=3)
    def convert(self, symbol: str, direction: str, size: int) -> Dict[str, Union[str, int]]:
        """Convert between composite and base securities."""
        self._rate_limit()
        try:
            data = {
                'symbol': symbol,
                'direction': direction,
                'size': size
            }
            response = self.session.post(f'{self.base_url}/convert', json=data)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error converting {symbol}: {e}")
            return {} 