from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict, List
import random
import uvicorn
import time

app = FastAPI()

# Mock data with dynamic prices
class MockExchange:
    def __init__(self):
        self.base_price = 1000.0
        self.last_update = time.time()
        self.order_books = {
            "BOND": {
                "bids": [],
                "asks": []
            }
        }
        self.update_prices()

    def update_prices(self):
        current_time = time.time()
        if current_time - self.last_update >= 1.0:  # Update every second
            # Add some random movement to base price
            self.base_price += random.uniform(-1.0, 1.0)
            
            # Generate new order book
            self.order_books["BOND"] = {
                "bids": [
                    {"price": round(self.base_price - 0.5, 2), "size": random.randint(5, 15)},
                    {"price": round(self.base_price - 1.0, 2), "size": random.randint(5, 15)}
                ],
                "asks": [
                    {"price": round(self.base_price + 0.5, 2), "size": random.randint(5, 15)},
                    {"price": round(self.base_price + 1.0, 2), "size": random.randint(5, 15)}
                ]
            }
            self.last_update = current_time

mock_exchange = MockExchange()

class Order(BaseModel):
    symbol: str
    direction: str
    price: float
    size: int

class CancelOrder(BaseModel):
    order_id: str

class Convert(BaseModel):
    symbol: str
    direction: str
    size: int

@app.get("/book/{symbol}")
async def get_order_book(symbol: str):
    if symbol not in mock_exchange.order_books:
        raise HTTPException(status_code=404, detail="Symbol not found")
    mock_exchange.update_prices()
    return mock_exchange.order_books[symbol]

@app.post("/orders")
async def place_order(order: Order):
    # Simulate order placement
    order_id = f"order_{random.randint(1000, 9999)}"
    return {
        "order_id": order_id,
        "symbol": order.symbol,
        "direction": order.direction,
        "price": order.price,
        "size": order.size,
        "status": "filled"
    }

@app.post("/cancel")
async def cancel_order(cancel: CancelOrder):
    # Simulate order cancellation
    return {"status": "cancelled", "order_id": cancel.order_id}

@app.get("/positions")
async def get_positions():
    return {}

@app.post("/convert")
async def convert(convert: Convert):
    # Simulate conversion
    return {
        "status": "converted",
        "symbol": convert.symbol,
        "direction": convert.direction,
        "size": convert.size
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000) 