# Sample Shop API Requirements

This document describes a small e-commerce service used for AI Test Agent demos.

## GET /health

Description: Check whether the service is alive.

Success: 200
Response Keys: status

## POST /login

Description: Login with demo credentials and receive an access token.

Request JSON:
```json
{"username": "demo", "password": "secret"}
```

Success: 200
Response Keys: token, user_id

## GET /products

Description: Query all available products.

Success: 200
Response Keys: items, total

## POST /orders

Description: Create an order for an existing product.

Request JSON:
```json
{"product_id": 1, "quantity": 2}
```

Success: 201
Response Keys: order_id, status
