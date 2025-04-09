from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict, List
import random
import uvicorn

app = FastAPI()

# Mock data
order_books = {
    "BOND": {
        "bids": [{"price": 999.5, "size": 10}, {"price": 999.0, "size": 20}],
        "asks": [{"price": 1000.5, "size": 10}, {"price": 1001.0, "size": 20}]
    }
}

positions = {}

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
    if symbol not in order_books:
        raise HTTPException(status_code=404, detail="Symbol not found")
    return order_books[symbol]

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
    return positions

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