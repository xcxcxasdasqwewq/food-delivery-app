---
title: Food Delivery System API Documentation
type: api
created: 2025-12-30 14:30:09.400000
updated: 2025-12-30 14:30:09.400000
synced_from: VibeProject
---

# Food Delivery System API Documentation

## Introduction

This API documentation provides a comprehensive guide to the RESTful API endpoints for the Food Delivery System project. The system supports multiple user roles: Admin, Restaurant Owner, Delivery Person, and Customer. Each role has specific capabilities and access to endpoints.

The API is built using Flask (Python) with SQLite database, JWT for authentication, and CORS enabled for local development. The frontend is developed with React.

### Base URL
```
http://localhost:5000
```

### Key Features
- **Role-based access control**: Endpoints are protected based on user roles.
- **JWT Authentication**: Secure token-based authentication.
- **Role Capabilities**:
  - **Admin**: Full system overview, manage users and orders, create restaurants.
  - **Restaurant Owner**: Manage their restaurant's orders and menu.
  - **Delivery Person**: Handle deliveries.
  - **Customer**: Browse, order, and track.

### Database Schema
- **users**: Stores user accounts with roles (admin, restaurant_owner, delivery_person, customer).
- **restaurants**: Restaurant information.
- **menu_items**: Menu items linked to restaurants.
- **orders**: Order records.
- **order_items**: Items within orders.

## Authentication

All API requests require authentication via JWT tokens, except for registration and login.

### JWT Token
- Obtained via login endpoint.
- Include in headers: `Authorization: Bearer <token>`
- Tokens expire after 24 hours.

### Endpoints

#### POST /api/auth/login
Authenticate a user and return a JWT token.

**Request Body:**
```json
{
  "username": "string",
  "password": "string"
}
```

**Response:**
```json
{
  "token": "jwt_token_here",
  "user": {
    "id": 1,
    "username": "string",
    "role": "customer"
  }
}
```

**Status Codes:**
- 200: Success
- 401: Invalid credentials

#### POST /api/auth/register
Register a new user.

**Request Body:**
```json
{
  "username": "string",
  "password": "string",
  "role": "customer"  // Options: admin, restaurant_owner, delivery_person, customer
}
```

**Response:**
```json
{
  "message": "User created successfully",
  "user_id": 1
}
```

**Status Codes:**
- 201: Created
- 400: Bad request (e.g., missing fields)

## Restaurants

Endpoints for browsing restaurants and menus. Accessible to all authenticated users.

### GET /api/restaurants
Retrieve a list of all restaurants.

**Request:** None (GET)

**Response:**
```json
[
  {
    "id": 1,
    "name": "Restaurant Name",
    "description": "Description",
    "location": "Location"
  }
]
```

**Status Codes:**
- 200: Success

### GET /api/restaurants/:id/menu
Get the menu for a specific restaurant.

**Parameters:**
- `id`: Restaurant ID (integer)

**Response:**
```json
[
  {
    "id": 1,
    "name": "Item Name",
    "description": "Description",
    "price": 10.99,
    "restaurant_id": 1
  }
]
```

**Status Codes:**
- 200: Success
- 404: Restaurant not found

## Orders

Endpoints for managing orders, with role-based access.

### GET /api/orders
Retrieve orders based on user role.
- **Customer**: Their own orders.
- **Restaurant Owner**: Orders for their restaurant.
- **Delivery Person**: Assigned deliveries.
- **Admin**: All orders.

**Request:** None (GET)

**Response:**
```json
[
  {
    "id": 1,
    "customer_id": 1,
    "restaurant_id": 1,
    "status": "pending",  // pending, confirmed, preparing, ready, rejected, picked_up, delivered
    "total": 25.99,
    "items": [
      {
        "menu_item_id": 1,
        "quantity": 2,
        "price": 10.99
      }
    ],
    "created_at": "2023-10-01T12:00:00Z"
  }
]
```

**Status Codes:**
- 200: Success

### POST /api/orders
Create a new order. Accessible to customers.

**Request Body:**
```json
{
  "restaurant_id": 1,
  "items": [
    {
      "menu_item_id": 1,
      "quantity": 2
    }
  ]
}
```

**Response:**
```json
{
  "message": "Order created successfully",
  "order_id": 1
}
```

**Status Codes:**
- 201: Created
- 400: Invalid data

### PUT /api/orders/:id/status
Update order status. Role-based:
- **Restaurant Owner**: confirm, preparing, ready, reject
- **Delivery Person**: picked_up, delivered

**Parameters:**
- `id`: Order ID

**Request Body:**
```json
{
  "status": "confirmed"
}
```

**Response:**
```json
{
  "message": "Status updated successfully"
}
```

**Status Codes:**
- 200: Success
- 403: Forbidden (wrong role)
- 404: Order not found

## Admin Endpoints

Accessible only to Admins.

### GET /api/admin/users
Get all users.

**Response:**
```json
[
  {
    "id": 1,
    "username": "string",
    "role": "customer"
  }
]
```

**Status Codes:**
- 200: Success

### POST /api/admin/restaurants
Create a new restaurant.

**Request Body:**
```json
{
  "name": "New Restaurant",
  "description": "Description",
  "location": "Location"
}
```

**Response:**
```json
{
  "message": "Restaurant created successfully",
  "restaurant_id": 1
}
```

**Status Codes:**
- 201: Created
- 400: Invalid data

## Restaurant Owner Endpoints

Accessible to Restaurant Owners.

### POST /api/restaurant/menu
Add a menu item to their restaurant.

**Request Body:**
```json
{
  "name": "New Item",
  "description": "Description",
  "price": 9.99
}
```

**Response:**
```json
{
  "message": "Menu item added successfully",
  "item_id": 1
}
```

**Status Codes:**
- 201: Created
- 400: Invalid data

## Delivery Endpoints

Accessible to Delivery Persons.

### GET /api/delivery/available
Get available orders for delivery (status: ready).

**Response:**
```json
[
  {
    "id": 1,
    "restaurant_id": 1,
    "status": "ready",
    "total": 25.99,
    "items": [...]
  }
]
```

**Status Codes:**
- 200: Success

## Error Handling

### Common Error Responses
```json
{
  "error": "Error message",
  "code": 400
}
```

### Status Codes
- **200**: OK
- **201**: Created
- **400**: Bad Request
- **401**: Unauthorized
- **403**: Forbidden
- **404**: Not Found
- **500**: Internal Server Error

### Authentication Errors
- Missing or invalid JWT: 401
- Expired token: 401
- Insufficient permissions: 403

## Example Requests

### Login Example (using curl)
```bash
curl -X POST http://localhost:5000/api/auth/login \
-H "Content-Type: application/json" \
-d '{"username": "customer1", "password": "password123"}'
```

### Create Order Example
```bash
curl -X POST http://localhost:5000/api/orders \
-H "Content-Type: application/json" \
-H "Authorization: Bearer <jwt_token>" \
-d '{"restaurant_id": 1, "items": [{"menu_item_id": 1, "quantity": 1}]}'
```

### Update Order Status Example
```bash
curl -X PUT http://localhost:5000/api/orders/1/status \
-H "Content-Type: application/json" \
-H "Authorization: Bearer <jwt_token>" \
-d '{"status": "confirmed"}'
```

## Security Notes
- Passwords are hashed using SHA-256.
- JWT tokens expire after 24 hours.
- CORS is enabled for local development.
- Ensure HTTPS in production.

## Conclusion

This documentation covers all API endpoints for the Food Delivery System. For frontend integration, use Axios with React. The database is auto-created with seeded data. Refer to the tech stack for implementation details.
