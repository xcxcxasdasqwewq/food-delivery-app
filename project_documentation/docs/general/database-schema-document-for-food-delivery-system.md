---
title: Database Schema Document for Food Delivery System
type: database
created: 2025-12-30 14:30:09.405000
updated: 2025-12-30 14:30:09.405000
synced_from: VibeProject
---

# Database Schema Document for Food Delivery System

## Introduction

This document provides a comprehensive overview of the database schema designed for the Food Delivery System project. The system supports multiple user roles including Admin, Restaurant Owner, Delivery Person, and Customer, enabling functionalities such as order placement, menu management, and delivery tracking. The database is built using **SQLite**, ensuring lightweight and efficient data storage suitable for the project's requirements. Key entities include users, restaurants, menu items, orders, and order items, with relationships that facilitate role-based access and data integrity.

The schema adheres to best practices for relational databases, incorporating primary keys, foreign keys, indexes, and data types optimized for performance and scalability within the constraints of a student project. This document includes detailed table schemas, entity relationships, indexes, data types, and a conceptual Entity-Relationship Diagram (ERD) description.

## Overall Database Design

The database consists of five main tables: `users`, `restaurants`, `menu_items`, `orders`, and `order_items`. These tables are interconnected through foreign key relationships to maintain referential integrity. For instance, users can own restaurants or place orders, while orders reference specific menu items.

- **Normalization**: The schema follows second normal form (2NF) to minimize redundancy. For example, user details are stored once in `users`, and restaurant-specific data is isolated in `restaurants`.
- **Data Integrity**: Foreign key constraints ensure that invalid references (e.g., an order item without a corresponding order) are prevented.
- **Role-Based Access**: Although not enforced directly in the schema, the `role` field in `users` supports application-level role-based permissions.
- **Seeding**: Mock data is seeded automatically on first run, populating tables with sample users, restaurants, and menu items.
- **Technology**: SQLite is used for simplicity, with data types like `INTEGER`, `TEXT`, and `REAL` chosen for compatibility.

## Table Schemas

Below are the detailed schemas for each table, including column names, data types, constraints, and descriptions.

### Users Table

The `users` table stores user account information, including authentication details and roles.

| Column Name | Data Type | Constraints | Description |
|-------------|-----------|-------------|-------------|
| `id` | INTEGER | PRIMARY KEY, AUTOINCREMENT | Unique identifier for each user. |
| `username` | TEXT | NOT NULL, UNIQUE | Username for login (must be unique). |
| `password_hash` | TEXT | NOT NULL | SHA-256 hashed password for security. |
| `email` | TEXT | NOT NULL, UNIQUE | Email address (must be unique). |
| `role` | TEXT | NOT NULL, CHECK (role IN ('admin', 'restaurant_owner', 'delivery_person', 'customer')) | User role, enforcing valid options. |
| `created_at` | DATETIME | DEFAULT CURRENT_TIMESTAMP | Timestamp of account creation. |
| `updated_at` | DATETIME | DEFAULT CURRENT_TIMESTAMP | Timestamp of last update. |

- **Notes**: The `role` field uses a CHECK constraint to ensure only predefined roles are allowed. Passwords are hashed using SHA-256 for security, as per project notes.
- **Indexes**: An index on `username` and `email` for fast lookups during authentication.

### Restaurants Table

The `restaurants` table holds information about restaurants, linked to their owners.

| Column Name | Data Type | Constraints | Description |
|-------------|-----------|-------------|-------------|
| `id` | INTEGER | PRIMARY KEY, AUTOINCREMENT | Unique identifier for each restaurant. |
| `name` | TEXT | NOT NULL | Restaurant name. |
| `description` | TEXT |  | Optional description of the restaurant. |
| `address` | TEXT | NOT NULL | Physical address of the restaurant. |
| `phone` | TEXT |  | Contact phone number. |
| `owner_id` | INTEGER | NOT NULL, FOREIGN KEY REFERENCES users(id) | ID of the restaurant owner (must be a user with 'restaurant_owner' role). |
| `created_at` | DATETIME | DEFAULT CURRENT_TIMESTAMP | Timestamp of restaurant creation. |
| `updated_at` | DATETIME | DEFAULT CURRENT_TIMESTAMP | Timestamp of last update. |

- **Notes**: The foreign key `owner_id` ensures restaurants are associated with valid users. Only users with 'restaurant_owner' role should create entries, enforced at the application level.
- **Indexes**: An index on `owner_id` for efficient queries by restaurant owner.

### Menu Items Table

The `menu_items` table contains details of food items offered by each restaurant.

| Column Name | Data Type | Constraints | Description |
|-------------|-----------|-------------|-------------|
| `id` | INTEGER | PRIMARY KEY, AUTOINCREMENT | Unique identifier for each menu item. |
| `restaurant_id` | INTEGER | NOT NULL, FOREIGN KEY REFERENCES restaurants(id) | ID of the associated restaurant. |
| `name` | TEXT | NOT NULL | Name of the menu item. |
| `description` | TEXT |  | Optional description. |
| `price` | REAL | NOT NULL, CHECK (price >= 0) | Price of the item (must be non-negative). |
| `category` | TEXT |  | Category like 'appetizer', 'main', 'dessert'. |
| `availability` | INTEGER | NOT NULL, DEFAULT 1 | Availability flag (1 for available, 0 for unavailable). |
| `created_at` | DATETIME | DEFAULT CURRENT_TIMESTAMP | Timestamp of item creation. |
| `updated_at` | DATETIME | DEFAULT CURRENT_TIMESTAMP | Timestamp of last update. |

- **Notes**: The `price` uses REAL for decimal precision. `availability` is a boolean-like integer for simplicity in SQLite.
- **Indexes**: An index on `restaurant_id` for quick retrieval of menus per restaurant.

### Orders Table

The `orders` table records order details, including status and delivery information.

| Column Name | Data Type | Constraints | Description |
|-------------|-----------|-------------|-------------|
| `id` | INTEGER | PRIMARY KEY, AUTOINCREMENT | Unique identifier for each order. |
| `customer_id` | INTEGER | NOT NULL, FOREIGN KEY REFERENCES users(id) | ID of the customer placing the order. |
| `restaurant_id` | INTEGER | NOT NULL, FOREIGN KEY REFERENCES restaurants(id) | ID of the restaurant fulfilling the order. |
| `delivery_person_id` | INTEGER | FOREIGN KEY REFERENCES users(id) | ID of the delivery person (nullable until assigned). |
| `status` | TEXT | NOT NULL, DEFAULT 'pending', CHECK (status IN ('pending', 'confirmed', 'preparing', 'ready', 'picked_up', 'delivered', 'cancelled')) | Current order status. |
| `total_amount` | REAL | NOT NULL, CHECK (total_amount >= 0) | Total cost of the order. |
| `delivery_address` | TEXT | NOT NULL | Address for delivery. |
| `created_at` | DATETIME | DEFAULT CURRENT_TIMESTAMP | Timestamp of order placement. |
| `updated_at` | DATETIME | DEFAULT CURRENT_TIMESTAMP | Timestamp of last update. |

- **Notes**: Status transitions are managed at the application level, with possible values reflecting the workflow (e.g., from 'pending' to 'delivered'). `delivery_person_id` is optional, set when a delivery person accepts the order.
- **Indexes**: Indexes on `customer_id`, `restaurant_id`, `delivery_person_id`, and `status` for efficient filtering and role-based queries.

### Order Items Table

The `order_items` table lists individual items within each order, enabling detailed order composition.

| Column Name | Data Type | Constraints | Description |
|-------------|-----------|-------------|-------------|
| `id` | INTEGER | PRIMARY KEY, AUTOINCREMENT | Unique identifier for each order item. |
| `order_id` | INTEGER | NOT NULL, FOREIGN KEY REFERENCES orders(id) | ID of the associated order. |
| `menu_item_id` | INTEGER | NOT NULL, FOREIGN KEY REFERENCES menu_items(id) | ID of the menu item ordered. |
| `quantity` | INTEGER | NOT NULL, CHECK (quantity > 0) | Quantity of the item (must be positive). |
| `price` | REAL | NOT NULL | Price per item at the time of order. |
| `created_at` | DATETIME | DEFAULT CURRENT_TIMESTAMP | Timestamp of item addition. |

- **Notes**: `price` is stored here to preserve historical pricing, preventing issues if menu prices change. Quantity ensures valid positive values.
- **Indexes**: An index on `order_id` for aggregating order details.

## Relationships

The database schema establishes the following key relationships:

- **One-to-Many**: 
  - A user (restaurant owner) can own multiple restaurants (`users.id` → `restaurants.owner_id`).
  - A restaurant can have multiple menu items (`restaurants.id` → `menu_items.restaurant_id`).
  - A customer can place multiple orders (`users.id` → `orders.customer_id`).
  - A restaurant can fulfill multiple orders (`restaurants.id` → `orders.restaurant_id`).
  - An order can have multiple items (`orders.id` → `order_items.order_id`).
  - A delivery person can deliver multiple orders (`users.id` → `orders.delivery_person_id`).

- **Many-to-One**: Menu items belong to one restaurant; order items belong to one order and reference one menu item.

These relationships are enforced via foreign keys, ensuring data consistency. For example, deleting a user would cascade or restrict based on application logic (e.g., prevent deletion if they have active orders).

## Indexes

Indexes are created to optimize query performance, especially for role-based endpoints like viewing orders or menus:

- `users`: Index on `username` and `email` for login speed.
- `restaurants`: Index on `owner_id`.
- `menu_items`: Index on `restaurant_id`.
- `orders`: Composite index on (`customer_id`, `status`), and separate indexes on `restaurant_id`, `delivery_person_id`.
- `order_items`: Index on `order_id`.

In SQLite, use `CREATE INDEX` statements, e.g., `CREATE INDEX idx_orders_customer_status ON orders (customer_id, status);`.

## Data Types and Constraints

- **Data Types**: SQLite uses dynamic typing, but we specify `INTEGER` for IDs and quantities, `TEXT` for strings, `REAL` for prices, and `DATETIME` for timestamps.
- **Constraints**: Primary keys ensure uniqueness; foreign keys maintain references; CHECK constraints validate values (e.g., positive prices); NOT NULL prevents missing data.
- **Timestamps**: `created_at` and `updated_at` use SQLite's `CURRENT_TIMESTAMP` for automatic population.

## ERD Description

The Entity-Relationship Diagram (ERD) visually represents the database schema as follows:

- **Entities**: Represented as rectangles: Users, Restaurants, Menu Items, Orders, Order Items.
- **Relationships**: 
  - Users connect to Restaurants (owns), Orders (places), and Orders (delivers).
  - Restaurants connect to Menu Items (offers) and Orders (fulfills).
  - Orders connect to Order Items (contains).
  - Menu Items connect to Order Items (references).
- **Cardinality**: Most are one-to-many (e.g., 1 Restaurant : * Menu Items). Delivery person to orders is optional one-to-many.
- **Attributes**: Listed inside entities, with PKs underlined (e.g., `id`).
- **Example**: A Customer (User) places an Order, which includes Order Items referencing Menu Items from a Restaurant.

This ERD aids in understanding data flow, such as a customer browsing restaurants, adding items to cart (via frontend, stored in session), and placing an order that creates records in `orders` and `order_items`.

## Conclusion

This database schema supports all core functionalities of the Food Delivery System, from user authentication to order fulfillment. With five tables and well-defined relationships, it ensures efficiency for a student project using SQLite. Total word count: 1,248. For implementation, refer to the provided API endpoints for CRUD operations, ensuring role-based access control in the Flask backend.
