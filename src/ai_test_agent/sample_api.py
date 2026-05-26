"""A small FastAPI service used by generated tests and demos."""

from __future__ import annotations

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field


app = FastAPI(title="Sample Shop API", version="0.1.0")


class LoginRequest(BaseModel):
    username: str
    password: str


class OrderRequest(BaseModel):
    product_id: int
    quantity: int = Field(ge=1, le=99)


PRODUCTS = {
    1: {"id": 1, "name": "Keyboard", "price": 299},
    2: {"id": 2, "name": "Mouse", "price": 129},
}


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/login")
def login(payload: LoginRequest) -> dict[str, object]:
    if payload.username != "demo" or payload.password != "secret":
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return {"token": "demo-token", "user_id": 1001}


@app.get("/products")
def list_products() -> dict[str, object]:
    items = list(PRODUCTS.values())
    return {"items": items, "total": len(items)}


@app.post("/orders", status_code=201)
def create_order(payload: OrderRequest) -> dict[str, object]:
    if payload.product_id not in PRODUCTS:
        raise HTTPException(status_code=404, detail="Product not found")
    return {"order_id": "ORD-10001", "status": "created"}
