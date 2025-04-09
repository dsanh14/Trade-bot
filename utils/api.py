import requests
import os
from typing import Dict, List, Optional
from dotenv import load_dotenv

load_dotenv()

class ExchangeAPI:
    def __init__(self, base_url: str = None, api_key: str = None):
        self.base_url = base_url or os.getenv('EXCHANGE_URL', 'http://localhost:8000')
        self.api_key = api_key or os.getenv('EXCHANGE_API_KEY')
        self.session = requests.Session()
        self.session.headers.update({
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json'
        })

    def get_order_book(self, symbol: str) -> Dict:
        """Get the current order book for a symbol."""
        try:
            response = self.session.get(f'{self.base_url}/book/{symbol}')
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error getting order book for {symbol}: {e}")
            return {}

    def place_order(self, symbol: str, direction: str, price: float, size: int) -> Dict:
        """Place a new order."""
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

    def cancel_order(self, order_id: str) -> bool:
        """Cancel an existing order."""
        try:
            response = self.session.post(f'{self.base_url}/cancel', json={'order_id': order_id})
            response.raise_for_status()
            return True
        except requests.exceptions.RequestException as e:
            print(f"Error canceling order {order_id}: {e}")
            return False

    def get_positions(self) -> List[Dict]:
        """Get current positions."""
        try:
            response = self.session.get(f'{self.base_url}/positions')
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error getting positions: {e}")
            return []

    def convert(self, symbol: str, direction: str, size: int) -> Dict:
        """Convert between composite and base securities."""
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