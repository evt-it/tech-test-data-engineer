"""Event source: serves one new sales event per GET /event request."""

import random
import uuid
from datetime import datetime, timezone

from fastapi import FastAPI

from catalogue import PRODUCTS

app = FastAPI(title="event-source")


@app.get("/event")
def event() -> dict:
    product = random.choice(PRODUCTS)
    quantity = random.randint(1, 5)
    total_amount = round(quantity * product["unit_price"], 2)
    return {
        "order_id": str(uuid.uuid4()),
        "customer_id": str(uuid.uuid4()),
        "product_id": product["product_id"],
        "product_name": product["product_name"],
        "category": product["category"],
        "quantity": quantity,
        "unit_price": product["unit_price"],
        "total_amount": total_amount,
        "order_ts": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
    }


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}
