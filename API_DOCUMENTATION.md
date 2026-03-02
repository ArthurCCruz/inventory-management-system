# Inventory Management System - API Documentation

## Overview

This document provides comprehensive documentation for the Inventory Management System REST API.

**Base URL:** `http://localhost:8000/v1/`

**Authentication:** JWT (JSON Web Tokens) with HttpOnly cookie-based refresh tokens

**Content Type:** `application/json`

## Table of Contents

- [Health Check](#health-check)
- [Authentication](#authentication)
- [Users](#users)
- [Products](#products)
- [Purchase Orders](#purchase-orders)
- [Sale Orders](#sale-orders)
- [Dashboard](#dashboard)
- [Common Response Codes](#common-response-codes)

---

## Health Check

### Health Check

**GET** `/v1/health/`

Check if the API is running and healthy.

**Authentication Required:** No

**Success Response (200 OK):**
```json
{
  "status": "healthy"
}
```

---

## Authentication

The API uses JWT tokens for authentication. Access tokens are returned in the response body and should be included in the `Authorization` header. Refresh tokens are stored as HttpOnly cookies for security.

### Login

**POST** `/v1/auth/login/`

Authenticate a user and receive access token.

**Authentication Required:** No

**Request Body:**
```json
{
  "username": "johndoe",
  "password": "securepassword123"
}
```

**Success Response (200 OK):**
```json
{
  "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "user": {
    "id": 1,
    "username": "johndoe",
    "name": "John Doe"
  }
}
```

**Response Headers:**
- `Set-Cookie`: `refresh_token=<token>; HttpOnly; Secure; SameSite=None`

**Error Responses:**
- **400 Bad Request:** Invalid credentials
```json
{
  "detail": "Invalid credentials"
}
```

---

### Refresh Access Token

**POST** `/v1/auth/refresh/`

Get a new access token using the refresh token stored in cookies.

**Authentication Required:** No (uses HttpOnly cookie)

**Request Headers:**
- `Cookie`: `refresh_token=<token>` (automatically sent by browser)

**Success Response (200 OK):**
```json
{
  "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

**Error Responses:**
- **401 Unauthorized:** Invalid or expired refresh token
```json
{
  "detail": "Token is invalid or expired"
}
```

---

### Logout

**POST** `/v1/auth/logout/`

Logout the user and clear the refresh token cookie.

**Authentication Required:** No

**Success Response (200 OK):**
```json
{
  "detail": "Logged out"
}
```

---

### Get Current User

**GET** `/v1/auth/me/`

Get information about the currently authenticated user.

**Authentication Required:** Yes

**Request Headers:**
```
Authorization: Bearer <access_token>
```

**Success Response (200 OK):**
```json
{
  "id": 1,
  "username": "johndoe",
  "name": "John Doe"
}
```

**Error Responses:**
- **401 Unauthorized:** Missing or invalid token
```json
{
  "detail": "Authentication credentials were not provided."
}
```

---

## Users

### User Signup

**POST** `/v1/users/`

Register a new user account.

**Authentication Required:** No

**Request Body:**
```json
{
  "username": "johndoe",
  "first_name": "John",
  "last_name": "Doe",
  "password": "securepassword123"
}
```

**Success Response (201 Created):**
```json
{
  "id": 1,
  "username": "johndoe",
  "first_name": "John",
  "last_name": "Doe"
}
```

**Error Responses:**
- **400 Bad Request:** Validation errors
```json
{
  "username": ["A user with that username already exists."]
}
```

---

## Products

All product endpoints require authentication. Products are user-scoped (each user only sees their own products).

### List Products

**GET** `/v1/products/`

Get a list of all products for the authenticated user.

**Authentication Required:** Yes

**Request Headers:**
```
Authorization: Bearer <access_token>
```

**Success Response (200 OK):**
```json
[
  {
    "id": 1,
    "name": "Organic Coffee Beans",
    "sku": "COFFEE-001",
    "description": "Premium arabica coffee beans",
    "unit": "kg",
    "created_at": "2026-03-01T10:30:00Z",
    "updated_at": "2026-03-01T10:30:00Z",
    "created_by": {
      "id": 1,
      "name": "John Doe"
    },
    "stock_quantity_totals": {
      "quantity": 150.00,
      "reserved_quantity": 20.00,
      "available_quantity": 130.00,
      "forecasted_quantity": 0
    }
  },
  {
    "id": 2,
    "name": "Whole Milk",
    "sku": "MILK-001",
    "description": "Fresh whole milk",
    "unit": "l",
    "created_at": "2026-03-02T08:15:00Z",
    "updated_at": "2026-03-02T08:15:00Z",
    "created_by": {
      "id": 1,
      "name": "John Doe"
    },
    "stock_quantity_totals": {
      "quantity": 150.00,
      "reserved_quantity": 20.00,
      "available_quantity": 130.00,
      "forecasted_quantity": 0
    }
  }
]
```

---

### Create Product

**POST** `/v1/products/`

Create a new product.

**Authentication Required:** Yes

**Request Headers:**
```
Authorization: Bearer <access_token>
```

**Request Body:**
```json
{
  "name": "Organic Coffee Beans",
  "sku": "COFFEE-001",
  "description": "Premium arabica coffee beans",
  "unit": "kg"
}
```

**Available Units:** `kg`, `g`, `unit`, `l`, `ml`

**Success Response (201 Created):**
```json
{
  "id": 1,
  "name": "Organic Coffee Beans",
  "sku": "COFFEE-001",
  "description": "Premium arabica coffee beans",
  "unit": "kg",
  "created_at": "2026-03-01T10:30:00Z",
  "updated_at": "2026-03-01T10:30:00Z",
  "created_by": 1
}
```

**Error Responses:**
- **400 Bad Request:** Validation errors
```json
{
  "sku": ["SKU must be unique."]
}
```

---

### Get Product Details

**GET** `/v1/products/{id}/`

Get details of a specific product.

**Authentication Required:** Yes

**Request Headers:**
```
Authorization: Bearer <access_token>
```

**Success Response (200 OK):**
```json
{
  "id": 1,
  "name": "Organic Coffee Beans",
  "sku": "COFFEE-001",
  "description": "Premium arabica coffee beans",
  "unit": "kg",
  "created_at": "2026-03-01T10:30:00Z",
  "updated_at": "2026-03-01T10:30:00Z",
  "created_by": {
    "id": 1,
    "name": "John Doe"
  },
  "stock_quantity_totals": {
    "quantity": 0.0,
    "reserved_quantity": 0.0,
    "available_quantity": 0.0,
    "forecasted_quantity": 0.0
  }
}
```

**Error Responses:**
- **404 Not Found:** Product does not exist or does not belong to user

---

### Update Product

**PATCH** `/v1/products/{id}/`

Update an existing product.

**Authentication Required:** Yes

**Request Headers:**
```
Authorization: Bearer <access_token>
```

**Request Body (partial update):**
```json
{
  "name": "Premium Organic Coffee Beans",
  "description": "Premium single-origin arabica coffee beans"
}
```

**Success Response (200 OK):**
```json
{
  "id": 1,
  "name": "Premium Organic Coffee Beans",
  "sku": "COFFEE-001",
  "description": "Premium single-origin arabica coffee beans",
  "unit": "kg",
  "created_at": "2026-03-01T10:30:00Z",
  "updated_at": "2026-03-02T14:20:00Z",
  "created_by": 1
}
```

---

### Delete Product

**DELETE** `/v1/products/{id}/`

Delete a product.

**Authentication Required:** Yes

**Request Headers:**
```
Authorization: Bearer <access_token>
```

**Success Response (204 No Content)**

**Error Responses:**
- **404 Not Found:** Product does not exist or does not belong to user

---

### Get Product Stock Quantity

**GET** `/v1/products/{id}/stock-quantity/`

Get detailed stock quantities by lot for a product.

**Authentication Required:** Yes

**Request Headers:**
```
Authorization: Bearer <access_token>
```

**Success Response (200 OK):**
```json
{
  "stock_quantity": [
    {
      "id": 1,
      "quantity": "100.00",
      "reserved_quantity": "10.00",
      "available_quantity": "90.00",
      "stock_lot": {
        "id": 1,
        "name": "LOT-1"
      }
    },
    {
      "id": 2,
      "quantity": "50.00",
      "reserved_quantity": "10.00",
      "available_quantity": "40.00",
      "stock_lot": {
        "id": 2,
        "name": "LOT-2"
      }
    }
  ]
}
```

---

### Get Product Stock Moves

**GET** `/v1/products/{id}/moves/`

Get stock movement history for a product.

**Authentication Required:** Yes

**Request Headers:**
```
Authorization: Bearer <access_token>
```

**Success Response (200 OK):**
```json
[
  {
    "id": 1,
    "quantity": "100.00",
    "from_location": "supplier",
    "to_location": "stock",
    "status": "done",
    "origin": "PO-5",
    "name": "IN-1",
    "updated_at": "2026-03-01T11:00:00Z",
    "stock_move_lines": [
      {
        "id": 1,
        "quantity": "100.00",
        "stock_lot": {
          "id": 1,
          "name": "LOT-1"
        }
      }
    ]
  },
  {
    "id": 2,
    "quantity": "20.00",
    "from_location": "stock",
    "to_location": "customer",
    "status": "done",
    "origin": "SO-3",
    "name": "OUT-2",
    "updated_at": "2026-03-02T09:30:00Z",
    "stock_move_lines": [
      {
        "id": 2,
        "quantity": "20.00",
        "stock_lot": {
          "id": 1,
          "name": "LOT-1"
        }
      }
    ]
  }
]
```

**Location Types:** `supplier`, `customer`, `stock`, `adjustment`

**Status Types:** `pending`, `reserved`, `done`

---

### Get Product Lots

**GET** `/v1/products/{id}/lots/`

Get all stock lots for a product.

**Authentication Required:** Yes

**Request Headers:**
```
Authorization: Bearer <access_token>
```

**Success Response (200 OK):**
```json
{
  "stock_lots": [
    {
      "id": 1,
      "name": "LOT-1"
    },
    {
      "id": 2,
      "name": "LOT-2"
    }
  ]
}
```

---

### Update Product Quantity

**PATCH** `/v1/products/{id}/update-quantity/`

Adjust stock quantity for a product (manual stock adjustment).

**Authentication Required:** Yes

**Request Headers:**
```
Authorization: Bearer <access_token>
```

**Request Body:**
```json
[
    {
        "stock_lot_id": 25,
        "quantity": 200,
        "create_new_lot": false
    },
    {
        "create_new_lot": true,
        "quantity": 200,
        "unit_price": 100
    }
]
```

**Parameters:**
- `quantity` (required): Amount to add (positive) or subtract (negative)
- `stock_lot_id` (optional): Existing lot ID to adjust
- `create_new_lot` (required): Create a new lot for this adjustment
- `unit_price` (optional): Unit price for the lot to be creayed

**Success Response (200 OK):**
```json
{
  "message": "Quantity updated successfully"
}
```

**Notes:**
- While adjusting quantity of existing lots, it can't be lower than the reserved amount

---

### Get Product Financial Data

**GET** `/v1/products/{id}/financial-data/`

Get financial metrics for a product.

**Authentication Required:** Yes

**Request Headers:**
```
Authorization: Bearer <access_token>
```

**Success Response (200 OK):**
```json
{
  "stock_value": 0.0,
  "stock_units": 0.0,
  "stock_unit_price": 0.0,
  "purchased_units": 0.0,
  "purchased_value": 0.0,
  "sold_units": 0.0,
  "sold_value": 0.0,
  "cogs": 0.0,
  "gross_profit": 0.0,
  "margin": 0.0,
  "write_off_units": 0.0,
  "write_off_value": 0.0,
  "adjustment_in_value": 0.0
}
```

---

## Purchase Orders

Purchase orders manage incoming inventory from suppliers. They follow a workflow: `draft` → `confirmed` → `received`.

### List Purchase Orders

**GET** `/v1/purchase-orders/`

Get a list of all purchase orders for the authenticated user.

**Authentication Required:** Yes

**Request Headers:**
```
Authorization: Bearer <access_token>
```

**Query Parameters:**
- `status` (optional): Filter by status (`draft`, `confirmed`, `received`)
- `ordering` (optional): Sort by field (e.g., `created_at`, `-created_at`)

**Example:** `/v1/purchase-orders/?status=confirmed&ordering=-created_at`

**Success Response (200 OK):**
```json
[
  {
    "id": 1,
    "name": "PO-1",
    "supplier_name": "ABC Suppliers Inc.",
    "status": "received",
    "total_price": "2500.00",
    "created_by": {
      "id": 1,
      "name": "John Doe"
    },
    "created_at": "2026-03-01T09:00:00Z",
    "updated_at": "2026-03-01T15:30:00Z"
  },
  {
    "id": 2,
    "name": "PO-2",
    "supplier_name": "XYZ Trading Co.",
    "status": "confirmed",
    "total_price": "1800.00",
    "created_by": {
      "id": 1,
      "name": "John Doe"
    },
    "created_at": "2026-03-02T10:15:00Z",
    "updated_at": "2026-03-02T10:20:00Z"
  }
]
```

**Status Types:** `draft`, `confirmed`, `received`

---

### Create Purchase Order

**POST** `/v1/purchase-orders/`

Create a new purchase order in draft status.

**Authentication Required:** Yes

**Request Headers:**
```
Authorization: Bearer <access_token>
```

**Request Body:**
```json
{
  "supplier_name": "ABC Suppliers Inc.",
  "lines": [
    {
      "product": 1,
      "quantity": "100.00",
      "unit_price": "20.00"
    },
    {
      "product": 2,
      "quantity": "50.00",
      "unit_price": "15.00"
    }
  ]
}
```

**Success Response (201 Created):**
```json
{
  "id": 3,
  "name": "PO-3",
  "supplier_name": "ABC Suppliers Inc.",
  "lines": [
    {
      "id": 5,
      "product": {
        "id": 1,
        "name": "Organic Coffee Beans"
      },
      "quantity": "100.00",
      "unit_price": "20.00",
      "total_price": "2000.00"
    },
    {
      "id": 6,
      "product": {
        "id": 2,
        "name": "Whole Milk"
      },
      "quantity": "50.00",
      "unit_price": "15.00",
      "total_price": "750.00"
    }
  ],
  "status": "draft",
  "total_price": "2750.00",
  "created_by": {
    "id": 1,
    "name": "John Doe"
  },
  "created_at": "2026-03-02T16:00:00Z",
  "updated_at": "2026-03-02T16:00:00Z"
}
```

**Error Responses:**
- **400 Bad Request:** Validation errors
```json
{
  "lines": ["Purchase order must have at least one line."]
}
```

**Notes:**
- Purchase orders are created in `draft` status by default
- `total_price` is automatically calculated from line items
- All products must belong to the authenticated user

---

### Get Purchase Order Details

**GET** `/v1/purchase-orders/{id}/`

Get details of a specific purchase order.

**Authentication Required:** Yes

**Request Headers:**
```
Authorization: Bearer <access_token>
```

**Success Response (200 OK):**
```json
{
  "id": 1,
  "name": "PO-1",
  "supplier_name": "ABC Suppliers Inc.",
  "status": "received",
  "total_price": "2500.00",
  "created_by": {
    "id": 1,
    "name": "John Doe"
  },
  "created_at": "2026-03-01T09:00:00Z",
  "updated_at": "2026-03-01T15:30:00Z",
  "lines": [
    {
      "id": 1,
      "product": {
        "id": 1,
        "name": "Organic Coffee Beans"
      },
      "quantity": "100.00",
      "unit_price": "25.00",
      "total_price": "2500.00"
    }
  ]
}
```

---

### Update Purchase Order

**PATCH** `/v1/purchase-orders/{id}/`

Update a purchase order. Only draft orders can be updated.

**Authentication Required:** Yes

**Request Headers:**
```
Authorization: Bearer <access_token>
```

**Request Body:**
```json
{
  "supplier_name": "ABC Suppliers Inc. (Updated)",
  "lines": [
    {
      "product": 1,
      "quantity": "120.00",
      "unit_price": "22.00"
    }
  ]
}
```

**Success Response (200 OK):**
```json
{
  "id": 3,
  "name": "PO-3",
  "supplier_name": "ABC Suppliers Inc. (Updated)",
  "status": "draft",
  "total_price": "2640.00",
  "created_by": {
    "id": 1,
    "name": "John Doe"
  },
  "created_at": "2026-03-02T16:00:00Z",
  "updated_at": "2026-03-02T16:30:00Z",
  "lines": [
    {
      "id": 7,
      "product": {
        "id": 1,
        "name": "Organic Coffee Beans"
      },
      "quantity": "120.00",
      "unit_price": "22.00",
      "total_price": "2640.00"
    }
  ]
}
```

**Notes:**
- Only purchase orders in `draft` status can be updated
- Updating lines replaces all existing lines with the new ones

---

### Delete Purchase Order

**DELETE** `/v1/purchase-orders/{id}/`

Delete a purchase order. Only draft orders can be deleted.

**Authentication Required:** Yes

**Request Headers:**
```
Authorization: Bearer <access_token>
```

**Success Response (204 No Content)**

**Error Responses:**
- **400 Bad Request:** Cannot delete non-draft order
```json
{
  "detail": "Only draft orders can be deleted."
}
```

---

### Confirm Purchase Order

**PATCH** `/v1/purchase-orders/{id}/confirm/`

Confirm a purchase order. This creates pending stock moves for receiving inventory.

**Authentication Required:** Yes

**Request Headers:**
```
Authorization: Bearer <access_token>
```

**Success Response (200 OK):**
```json
{
  "id": 3,
  "name": "PO-3",
  "supplier_name": "ABC Suppliers Inc.",
  "status": "confirmed",
  "total_price": "2640.00",
  "created_by": {
    "id": 1,
    "name": "John Doe"
  },
  "created_at": "2026-03-02T16:00:00Z",
  "updated_at": "2026-03-02T16:45:00Z",
  "lines": [
    {
      "id": 7,
      "product": {
        "id": 1,
        "name": "Organic Coffee Beans"
      },
      "quantity": "120.00",
      "unit_price": "22.00",
      "total_price": "2640.00"
    }
  ]
}
```

**Notes:**
- Only `draft` purchase orders can be confirmed
- Confirmation creates stock moves from `supplier` to `stock` with `pending` status

---

### Receive Purchase Order

**PATCH** `/v1/purchase-orders/{id}/receive/`

Mark a purchase order as received. This processes the stock moves and creates stock lots.

**Authentication Required:** Yes

**Request Headers:**
```
Authorization: Bearer <access_token>
```

**Success Response (200 OK):**
```json
{
  "id": 3,
  "name": "PO-3",
  "supplier_name": "ABC Suppliers Inc.",
  "status": "received",
  "total_price": "2640.00",
  "created_by": {
    "id": 1,
    "name": "John Doe"
  },
  "created_at": "2026-03-02T16:00:00Z",
  "updated_at": "2026-03-02T17:00:00Z",
  "lines": [
    {
      "id": 7,
      "product": {
        "id": 1,
        "name": "Organic Coffee Beans"
      },
      "quantity": "120.00",
      "unit_price": "22.00",
      "total_price": "2640.00"
    }
  ]
}
```

**Notes:**
- Only `confirmed` purchase orders can be received
- Receiving creates new stock lots with the unit price from the purchase order line
- Stock quantities are increased accordingly

---

## Sale Orders

Sale orders manage outgoing inventory to customers. They follow a workflow: `draft` → `confirmed` → `reserved` → `delivered`.

### List Sale Orders

**GET** `/v1/sale-orders/`

Get a list of all sale orders for the authenticated user.

**Authentication Required:** Yes

**Request Headers:**
```
Authorization: Bearer <access_token>
```

**Query Parameters:**
- `status` (optional): Filter by status (`draft`, `confirmed`, `reserved`, `delivered`)
- `ordering` (optional): Sort by field (e.g., `created_at`, `-created_at`)

**Example:** `/v1/sale-orders/?status=delivered&ordering=-created_at`

**Success Response (200 OK):**
```json
[
  {
    "id": 1,
    "name": "SO-1",
    "customer_name": "Acme Corporation",
    "status": "delivered",
    "total_price": "3200.00",
    "created_by": {
      "id": 1,
      "name": "John Doe"
    },
    "created_at": "2026-03-01T11:00:00Z",
    "updated_at": "2026-03-01T16:45:00Z"
  },
  {
    "id": 2,
    "name": "SO-2",
    "customer_name": "Best Retailers",
    "status": "reserved",
    "total_price": "1500.00",
    "created_by": {
      "id": 1,
      "name": "John Doe"
    },
    "created_at": "2026-03-02T09:30:00Z",
    "updated_at": "2026-03-02T10:00:00Z"
  }
]
```

**Status Types:** `draft`, `confirmed`, `reserved`, `delivered`

---

### Create Sale Order

**POST** `/v1/sale-orders/`

Create a new sale order in draft status.

**Authentication Required:** Yes

**Request Headers:**
```
Authorization: Bearer <access_token>
```

**Request Body:**
```json
{
  "customer_name": "Acme Corporation",
  "lines": [
    {
      "product": 1,
      "quantity": "50.00",
      "unit_price": "30.00"
    },
    {
      "product": 2,
      "quantity": "25.00",
      "unit_price": "20.00"
    }
  ]
}
```

**Success Response (201 Created):**
```json
{
  "id": 3,
  "name": "SO-3",
  "customer_name": "Acme Corporation",
  "lines": [
    {
      "id": 5,
      "product": {
        "id": 1,
        "name": "Organic Coffee Beans"
      },
      "quantity": "50.00",
      "unit_price": "30.00",
      "total_price": "1500.00"
    },
    {
      "id": 6,
      "product": {
        "id": 2,
        "name": "Whole Milk"
      },
      "quantity": "25.00",
      "unit_price": "20.00",
      "total_price": "500.00"
    }
  ],
  "status": "draft",
  "total_price": "2000.00",
  "created_by": {
    "id": 1,
    "name": "John Doe"
  },
  "created_at": "2026-03-02T14:00:00Z",
  "updated_at": "2026-03-02T14:00:00Z"
}
```

**Error Responses:**
- **400 Bad Request:** Validation errors
```json
{
  "lines": ["Sale order must have at least one line."]
}
```

**Notes:**
- Sale orders are created in `draft` status by default
- `total_price` is automatically calculated from line items
- All products must belong to the authenticated user

---

### Get Sale Order Details

**GET** `/v1/sale-orders/{id}/`

Get details of a specific sale order.

**Authentication Required:** Yes

**Request Headers:**
```
Authorization: Bearer <access_token>
```

**Success Response (200 OK):**
```json
{
  "id": 1,
  "name": "SO-1",
  "customer_name": "Acme Corporation",
  "status": "delivered",
  "total_price": "3200.00",
  "created_by": {
    "id": 1,
    "name": "John Doe"
  },
  "created_at": "2026-03-01T11:00:00Z",
  "updated_at": "2026-03-01T16:45:00Z",
  "lines": [
    {
      "id": 1,
      "product": {
        "id": 1,
        "name": "Organic Coffee Beans"
      },
      "quantity": "100.00",
      "unit_price": "32.00",
      "total_price": "3200.00"
    }
  ]
}
```

---

### Update Sale Order

**PATCH** `/v1/sale-orders/{id}/`

Update a sale order. Only draft orders can be updated.

**Authentication Required:** Yes

**Request Headers:**
```
Authorization: Bearer <access_token>
```

**Request Body:**
```json
{
  "customer_name": "Acme Corporation (Updated)",
  "lines": [
    {
      "product": 1,
      "quantity": "60.00",
      "unit_price": "32.00"
    }
  ]
}
```

**Success Response (200 OK):**
```json
{
  "id": 3,
  "name": "SO-3",
  "customer_name": "Acme Corporation (Updated)",
  "status": "draft",
  "total_price": "1920.00",
  "created_by": {
    "id": 1,
    "name": "John Doe"
  },
  "created_at": "2026-03-02T14:00:00Z",
  "updated_at": "2026-03-02T14:30:00Z",
  "lines": [
    {
      "id": 7,
      "product": {
        "id": 1,
        "name": "Organic Coffee Beans"
      },
      "quantity": "60.00",
      "unit_price": "32.00",
      "total_price": "1920.00"
    }
  ]
}
```

**Notes:**
- Only sale orders in `draft` status can be updated
- Updating lines replaces all existing lines with the new ones

---

### Delete Sale Order

**DELETE** `/v1/sale-orders/{id}/`

Delete a sale order. Only draft orders can be deleted.

**Authentication Required:** Yes

**Request Headers:**
```
Authorization: Bearer <access_token>
```

**Success Response (204 No Content)**

**Error Responses:**
- **400 Bad Request:** Cannot delete non-draft order
```json
{
  "detail": "Only draft orders can be deleted."
}
```

---

### Confirm Sale Order

**PATCH** `/v1/sale-orders/{id}/confirm/`

Confirm a sale order. This creates pending stock moves for delivering inventory.

**Authentication Required:** Yes

**Request Headers:**
```
Authorization: Bearer <access_token>
```

**Success Response (200 OK):**
```json
{
  "id": 3,
  "name": "SO-3",
  "customer_name": "Acme Corporation",
  "status": "confirmed",
  "total_price": "1920.00",
  "created_by": {
    "id": 1,
    "name": "John Doe"
  },
  "created_at": "2026-03-02T14:00:00Z",
  "updated_at": "2026-03-02T14:45:00Z",
  "lines": [
    {
      "id": 7,
      "product": {
        "id": 1,
        "name": "Organic Coffee Beans"
      },
      "quantity": "60.00",
      "unit_price": "32.00",
      "total_price": "1920.00"
    }
  ]
}
```

**Notes:**
- Only `draft` sale orders can be confirmed
- Confirmation creates stock moves from `stock` to `customer` with `pending` status

---

### Reserve Sale Order

**PATCH** `/v1/sale-orders/{id}/reserve/`

Reserve inventory for a sale order. This uses FIFO (First In, First Out) to allocate stock from available lots.

**Authentication Required:** Yes

**Request Headers:**
```
Authorization: Bearer <access_token>
```

**Success Response (200 OK):**
```json
{
  "id": 3,
  "name": "SO-3",
  "customer_name": "Acme Corporation",
  "status": "reserved",
  "total_price": "1920.00",
  "created_by": {
    "id": 1,
    "name": "John Doe"
  },
  "created_at": "2026-03-02T14:00:00Z",
  "updated_at": "2026-03-02T15:00:00Z",
  "lines": [
    {
      "id": 7,
      "product": {
        "id": 1,
        "name": "Organic Coffee Beans"
      },
      "quantity": "60.00",
      "unit_price": "32.00",
      "total_price": "1920.00"
    }
  ]
}
```

**Notes:**
- Only `confirmed` sale orders can be reserved
- Uses FIFO methodology to allocate stock from the oldest lots first
- Stock moves transition from `pending` to `reserved` status
- Reserved quantities are tracked separately from available quantities

---

### Deliver Sale Order

**PATCH** `/v1/sale-orders/{id}/deliver/`

Mark a sale order as delivered. This processes the stock moves and reduces inventory.

**Authentication Required:** Yes

**Request Headers:**
```
Authorization: Bearer <access_token>
```

**Success Response (200 OK):**
```json
{
  "id": 3,
  "name": "SO-3",
  "customer_name": "Acme Corporation",
  "status": "delivered",
  "total_price": "1920.00",
  "created_by": {
    "id": 1,
    "name": "John Doe"
  },
  "created_at": "2026-03-02T14:00:00Z",
  "updated_at": "2026-03-02T16:00:00Z",
  "lines": [
    {
      "id": 7,
      "product": {
        "id": 1,
        "name": "Organic Coffee Beans"
      },
      "quantity": "60.00",
      "unit_price": "32.00",
      "total_price": "1920.00"
    }
  ]
}
```

**Notes:**
- Only `reserved` sale orders can be delivered
- Stock moves transition from `reserved` to `done` status
- Stock quantities are decreased accordingly

---

## Dashboard

### Get Dashboard Data

**GET** `/v1/dashboard/`

Get dashboard statistics and analytics for the authenticated user.

**Authentication Required:** Yes

**Request Headers:**
```
Authorization: Bearer <access_token>
```

**Success Response (200 OK):**
```json
{
  "inventory": {
    "total_products": 42,
    "total_stock_value": 98250.00,
    "out_of_stock_items": 5
  },
  "orders": {
    "purchase_orders": {
      "draft": 3,
      "confirmed": 7,
      "received": 12
    },
    "sale_orders": {
      "draft": 2,
      "confirmed": 7,
      "reserved": 4,
      "delivered": 15
    }
  },
  "financial": {
    "cogs": 35000.00,
    "purchase_value": 48000.00,
    "sales_value": 91500.00,
    "gross_profit": 56500.00,
    "margin": 60.00
  }
}
```

**Notes:**
- Response structure may vary based on implementation
- Provides summary metrics and recent activity for quick overview

---

## Common Response Codes

### Success Codes

- **200 OK:** Request succeeded
- **201 Created:** Resource created successfully
- **204 No Content:** Request succeeded with no content to return (typically for DELETE)

### Client Error Codes

- **400 Bad Request:** Invalid request data or validation error
- **401 Unauthorized:** Missing or invalid authentication credentials
- **403 Forbidden:** User doesn't have permission to access the resource
- **404 Not Found:** Resource not found or doesn't belong to user

### Server Error Codes

- **500 Internal Server Error:** Server encountered an unexpected error

### Common Error Response Format

```json
{
  "detail": "Error message describing what went wrong"
}
```

**OR (validation errors):**

```json
{
  "field_name": ["Error message for this field"],
  "another_field": ["Error message for this field"]
}
```

---

## Notes

### User Scoping

All resources (products, purchase orders, sale orders) are automatically scoped to the authenticated user. Users can only see and interact with resources they created.

### FIFO Inventory Management

The system uses FIFO (First In, First Out) methodology for stock management. When reserving inventory for sale orders, the system automatically allocates from the oldest stock lots first.

### Order Workflows

**Purchase Order Workflow:**
1. Create order in `draft` status
2. Confirm order → status changes to `confirmed`, creates stock moves. These moves are included on products' forecasted amounts
3. Receive order → status changes to `received`, processes stock moves and creates lots

**Sale Order Workflow:**
1. Create order in `draft` status
2. Confirm order → status changes to `confirmed`, creates stock moves. These moves are included on products' forecasted amounts
3. Reserve inventory → status changes to `reserved`, allocates stock using FIFO
4. Deliver order → status changes to `delivered`, processes stock moves

### Stock Lots

Each purchase order line creates a new stock lot when received. Lots track the unit price of inventory batches for accurate cost accounting.

### Decimal Precision

All quantity and price fields use decimal precision with 2 decimal places for accuracy in financial calculations.
