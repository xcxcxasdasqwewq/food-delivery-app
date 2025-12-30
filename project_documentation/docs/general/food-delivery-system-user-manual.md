---
title: Food Delivery System User Manual
type: user-manual
created: 2025-12-30 14:30:09.565000
updated: 2025-12-30 14:30:09.565000
synced_from: VibeProject
---

# Food Delivery System User Manual

## Introduction

Welcome to the **Food Delivery System** User Manual. This comprehensive guide is designed to help you navigate and utilize the features of our web-based application, built as a student project using Python Flask for the backend and React for the frontend. The system supports multiple user roles, including **Admin**, **Restaurant Owner**, **Delivery Person**, and **Customer**, each with specific capabilities to facilitate a seamless food ordering and delivery experience.

This manual covers getting started, detailed feature guides, step-by-step tutorials, frequently asked questions (FAQ), and troubleshooting tips. Whether you're managing restaurants, delivering orders, or simply ordering food, this document will provide actionable instructions and practical examples.

**Note:** This is a student project, so features may be basic and not production-ready. The database is automatically created and seeded with mock data on first run. All data is stored in an SQLite database, and passwords are hashed for security.

## Getting Started

### Prerequisites
To use the application, ensure you have the following:
- A modern web browser (e.g., Chrome, Firefox, Safari)
- Internet connection (for local development, as CORS is enabled)
- Access to the deployed application or local server

### Installation and Setup
1. **Clone the Repository:** If setting up locally, clone the project repository from GitHub or your local source.
2. **Install Dependencies:**
   - For backend: Run `pip install flask flask-cors pyjwt` in your Python environment.
   - For frontend: Run `npm install react react-router-dom axios` in the frontend directory.
3. **Start the Backend:** Navigate to the backend folder and run `python app.py` (assuming the main file is `app.py`).
4. **Start the Frontend:** Navigate to the frontend folder and run `npm start`.
5. **Access the App:** Open your browser and go to `http://localhost:3000` (or the deployed URL).

Upon first run, the SQLite database will be created automatically, and mock data will be seeded.

### Logging In
1. Navigate to the login page.
2. Enter your email and password.
3. Click **Login**. If successful, you'll be redirected based on your role.
   - **Note:** Register new accounts via `POST /api/auth/register` or through the UI if implemented.

JWT tokens are issued upon login and expire after 24 hours.

## User Roles and Capabilities

The system supports four user roles, each with tailored access and functionalities.

### Admin (👨‍💼)
- **Capabilities:**
  - View all users and orders in the system.
  - Manage order statuses across all restaurants.
  - Create new restaurants.
  - Access a full system overview.
- **Use Cases:** System administrators use this role to monitor and control the entire platform.

### Restaurant Owner (🏪)
- **Capabilities:**
  - View orders specific to their restaurant.
  - Update order statuses: confirm, preparing, ready, reject.
  - Add menu items to their restaurant.
- **Use Cases:** Owners manage their restaurant's offerings and order flow.

### Delivery Person (🚴)
- **Capabilities:**
  - View available orders for delivery.
  - Accept orders for delivery.
  - Update delivery statuses: picked up, delivered.
- **Use Cases:** Delivery personnel handle the logistics of order fulfillment.

### Customer (👤)
- **Capabilities:**
  - Browse restaurants and their menus.
  - Add items to cart.
  - Place orders.
  - View order history and status.
- **Use Cases:** End-users place and track food orders.

## Features and Tutorials

### For Customers
#### Browsing Restaurants and Menus
1. Log in as a Customer.
2. Navigate to the restaurants page (via `GET /api/restaurants`).
3. Browse card-based layouts of restaurants.
4. Click on a restaurant to view its menu (`GET /api/restaurants/:id/menu`).
   - Menus display items in a responsive grid with hover effects.

#### Placing an Order
1. Select a restaurant and add items to your cart.
2. Review your cart.
3. Click **Place Order** to submit via `POST /api/orders`.
4. View order status in your history.

**Example:** Add a "Pizza Margherita" to cart, then place the order. The status will initially be "pending".

### For Restaurant Owners
#### Adding Menu Items
1. Log in as a Restaurant Owner.
2. Go to your restaurant's management page.
3. Click **Add Menu Item**.
4. Enter item details (name, price, description).
5. Submit via `POST /api/restaurant/menu`.
   - Items appear in the menu with modern typography.

**Example:** Add "Burger" for $10. It will be visible to customers immediately.

#### Managing Orders
1. View orders for your restaurant (`GET /api/orders`).
2. Select an order and update status via `PUT /api/orders/:id/status`.
   - Options: confirm, preparing, ready, reject.
   - Status badges show color-coded updates (e.g., green for "ready").

### For Delivery Persons
#### Accepting and Delivering Orders
1. Log in as a Delivery Person.
2. View available orders (`GET /api/delivery/available`).
3. Accept an order.
4. Update status to "picked up" or "delivered".
   - Use `PUT /api/orders/:id/status` for updates.

**Example:** Accept an order for "Pizza", mark as "picked up", then "delivered".

### For Admins
#### System Overview
1. Log in as Admin.
2. Access dashboard for all users (`GET /api/admin/users`) and orders.
3. Create restaurants via `POST /api/admin/restaurants`.
4. Manage order statuses globally.

## API Reference

For developers or advanced users, key API endpoints are listed below. Use tools like Postman for testing.

- **Authentication:**
  - `POST /api/auth/login`: Authenticate user.
  - `POST /api/auth/register`: Register new user.
- **Restaurants:**
  - `GET /api/restaurants`: List all.
  - `GET /api/restaurants/:id/menu`: Get menu.
- **Orders:**
  - `GET /api/orders`: Role-based order list.
  - `POST /api/orders`: Create order.
  - `PUT /api/orders/:id/status`: Update status.
- **Admin:**
  - `GET /api/admin/users`: All users.
  - `POST /api/admin/restaurants`: Create restaurant.
- **Restaurant Owner:**
  - `POST /api/restaurant/menu`: Add item.
- **Delivery:**
  - `GET /api/delivery/available`: Available orders.

All endpoints use JWT for authentication. Include the token in headers.

## Troubleshooting

### Common Issues
- **Login Fails:** Ensure correct credentials. Passwords are hashed with SHA-256.
- **Page Not Loading:** Check CORS settings or browser console for errors.
- **Order Not Updating:** Verify role permissions and token validity (expires in 24 hours).
- **Database Errors:** If running locally, ensure SQLite is accessible.

### Tips
- Use responsive design for mobile access.
- Clear browser cache if UI issues occur.
- Contact support (in a real app) for persistent problems.

## FAQ

**Q: How do I reset my password?**  
A: Password reset is not implemented in this student project. Use registration to create a new account.

**Q: Can I order from multiple restaurants?**  
A: Orders are per restaurant; create separate orders for different restaurants.

**Q: What if my order is rejected?**  
A: Contact the restaurant owner or admin; status will show "rejected".

**Q: Is the app secure?**  
A: Passwords are hashed, and JWT secures sessions, but this is for educational purposes.

**Q: How to add more users?**  
A: Admins can view users; registration is open via API.

## Conclusion

This User Manual provides a complete guide to using the Food Delivery System. With features like gradient backgrounds, card layouts, and status badges, the app offers a modern, responsive experience. For developers, the API allows integration. Remember, this is a student project—feedback is welcome for improvements. Total word count: approximately 1,200.
