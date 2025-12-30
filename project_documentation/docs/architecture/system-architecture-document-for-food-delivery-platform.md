---
title: System Architecture Document for Food Delivery Platform
type: architecture
created: 2025-12-30 14:30:09.398000
updated: 2025-12-30 14:30:09.398000
synced_from: VibeProject
---

# System Architecture Document for Food Delivery Platform

## Introduction

This System Architecture Document (SAD) provides a detailed overview of the architecture, design, and implementation of the Food Delivery Platform. The platform facilitates online food ordering, restaurant management, and delivery coordination with role-based access for administrators, restaurant owners, delivery personnel, and customers. The document covers the system's architecture, technology stack, design patterns, component interactions, data flow, and considerations for scalability, security, and deployment.

The project is implemented as a full-stack web application using Python with Flask for the backend and React for the frontend, backed by an SQLite database. It includes features like user authentication, order management, menu handling, and real-time status updates.

## System Overview

The Food Delivery Platform is a multi-role web application that connects customers with restaurants through an online ordering system. Key functionalities include:

- **User Management**: Role-based authentication and authorization for admins, restaurant owners, delivery persons, and customers.
- **Restaurant Management**: Admins can create restaurants; owners can manage menus and orders.
- **Order Processing**: Customers place orders, restaurant owners update statuses, and delivery personnel handle deliveries.
- **Data Persistence**: All data is stored in an SQLite database with automatic schema creation and mock data seeding.
- **Security**: Password hashing with SHA-256 and JWT-based authentication with 24-hour token expiry.

The system is designed for simplicity in a student project context, emphasizing clean architecture and modern web development practices.

## Architecture Overview

The system follows a **client-server architecture** with a layered backend and a component-based frontend. The overall architecture can be visualized as follows:

```
[Frontend (React)] <--HTTP/AJAX--> [Backend (Flask API)] <--SQL--> [Database (SQLite)]
```

- **Frontend Layer**: Handles user interactions, rendering UI components, and making API calls.
- **Backend Layer**: Processes business logic, handles authentication, and interacts with the database.
- **Database Layer**: Stores persistent data using a relational model.

The architecture emphasizes separation of concerns, with the backend providing RESTful APIs for the frontend. CORS is enabled for local development to allow cross-origin requests.

### High-Level Component Diagram

```
+----------------+       +-----------------+
|   React App    |       |   Flask Server  |
|                |       |                 |
| - Components   |       | - Routes        |
| - Router       |       | - Controllers   |
| - Axios        |       | - Models        |
+----------------+       +-----------------+
          |                        |
          | HTTP                   | SQL
          |                        |
          v                        v
+----------------+       +-----------------+
|   Browser      |       |   SQLite DB     |
+----------------+       +-----------------+
```

This diagram illustrates the main components: the React frontend communicates with the Flask backend via HTTP requests, while the backend queries the SQLite database.

## Technology Stack

The tech stack is chosen for simplicity, performance, and ease of development in a student project:

- **Backend**:
  - **Python 3**: Core programming language.
  - **Flask**: Lightweight web framework for building RESTful APIs.
  - **SQLite**: Embedded relational database for data persistence.
  - **JWT (JSON Web Tokens)**: For stateless authentication.
  - **Flask-CORS**: To handle cross-origin resource sharing during development.
  - **Werkzeug**: For password hashing using SHA-256.

- **Frontend**:
  - **React 18**: JavaScript library for building user interfaces with hooks and functional components.
  - **React Router**: For client-side routing and navigation.
  - **Axios**: HTTP client for making API requests.
  - **CSS3**: Custom styles for responsive design, gradients, hover effects, and modern typography (Inter font).

No external CSS frameworks are used to keep the implementation custom and educational. The database is automatically created and seeded with mock data on first run.

## Design Patterns

The system employs several design patterns to ensure maintainable and scalable code:

- **MVC (Model-View-Controller)**: Separates data (Model), user interface (View), and control logic (Controller). In Flask, routes act as controllers, while React components serve as views.
- **Repository Pattern**: Data access logic is abstracted in models that interact with the database.
- **Observer Pattern**: Implicit in React's state management for updating UI on data changes (e.g., order status updates).
- **RESTful Design**: APIs follow REST principles with resource-based endpoints and HTTP methods.
- **Singleton Pattern**: SQLite connection is managed as a single instance within the Flask app.
- **Component-Based Architecture**: React components encapsulate UI logic, promoting reusability.

For example, the `Order` model in Flask encapsulates database operations, while React's `OrderCard` component handles rendering order details.

## Component Diagrams

### Backend Component Diagram

The backend is structured into modules:

```
Flask App
├── app.py (Main application)
├── models/
│   ├── user.py
│   ├── restaurant.py
│   ├── menu_item.py
│   ├── order.py
│   └── order_item.py
├── routes/
│   ├── auth.py
│   ├── restaurants.py
│   ├── orders.py
│   ├── admin.py
│   └── delivery.py
└── utils/
    ├── auth.py (JWT handling)
    └── db.py (Database setup)
```

- **Models**: Define database interactions using SQLAlchemy (implied via Flask-SQLAlchemy, though not explicitly listed).
- **Routes**: Handle API endpoints with role-based authorization.
- **Utils**: Provide helper functions for authentication and database initialization.

### Frontend Component Diagram

The React app is organized by feature:

```
src/
├── components/
│   ├── Header.js
│   ├── RestaurantCard.js
│   ├── MenuItem.js
│   ├── OrderCard.js
│   └── StatusBadge.js
├── pages/
│   ├── Login.js
│   ├── Register.js
│   ├── Restaurants.js
│   ├── Menu.js
│   ├── Orders.js
│   └── AdminDashboard.js
├── services/
│   └── api.js (Axios instance)
└── App.js
```

- **Components**: Reusable UI elements like cards and badges.
- **Pages**: Route-based views for different user roles.
- **Services**: Centralized API calls.

## Data Flow

The data flow in the system follows a request-response pattern:

1. **User Interaction**: A customer browses restaurants via the React frontend.
2. **API Request**: Axios sends a GET request to `/api/restaurants`.
3. **Backend Processing**: Flask route queries the `restaurants` table in SQLite.
4. **Response**: JSON data is returned and rendered in React components.
5. **Order Placement**: Customer adds items to cart (client-side state) and posts to `/api/orders`.
6. **Status Updates**: Restaurant owner updates status via PUT to `/api/orders/:id/status`, triggering UI refresh.

For authentication:
- Login sends credentials to `/api/auth/login`.
- JWT token is issued and stored in localStorage for subsequent requests.

Data flows securely with JWT validation on protected routes.

## Database Schema

The database schema is relational and normalized:

- **users**: `id (PK), username, email, password_hash, role`
- **restaurants**: `id (PK), name, description, owner_id (FK to users)`
- **menu_items**: `id (PK), restaurant_id (FK), name, description, price`
- **orders**: `id (PK), customer_id (FK), restaurant_id (FK), status, total_price, created_at`
- **order_items**: `id (PK), order_id (FK), menu_item_id (FK), quantity`

Relationships: One-to-many between restaurants and menu_items/orders, orders and order_items.

Schema is created automatically on app startup.

## API Design

APIs are RESTful with JSON payloads:

- **Authentication**: POST `/api/auth/login`, POST `/api/auth/register`.
- **Restaurants**: GET `/api/restaurants`, GET `/api/restaurants/:id/menu`.
- **Orders**: GET `/api/orders` (filtered by role), POST `/api/orders`, PUT `/api/orders/:id/status`.
- **Admin**: GET `/api/admin/users`, POST `/api/admin/restaurants`.
- **Restaurant Owner**: POST `/api/restaurant/menu`.
- **Delivery**: GET `/api/delivery/available`.

All endpoints use JWT for authorization, with role checks in route handlers.

## Scalability Considerations

For a student project, scalability is limited by SQLite's single-writer model. Future enhancements:

- **Database**: Migrate to PostgreSQL or MySQL for concurrent access.
- **Backend**: Use Gunicorn for multi-threading, or deploy on cloud platforms like Heroku/AWS.
- **Frontend**: Implement code splitting in React for faster loads.
- **Caching**: Add Redis for session caching and API responses.
- **Load Balancing**: Use Nginx for distributing requests in a scaled setup.
- **Horizontal Scaling**: Containerize with Docker for microservices.

Current setup supports low-traffic scenarios; for higher loads, consider async processing with Celery.

## Security Considerations

- **Authentication**: JWT with 24-hour expiry; passwords hashed with SHA-256.
- **Authorization**: Role-based access control on API routes.
- **Input Validation**: Sanitize inputs to prevent SQL injection (though SQLite is less prone).
- **CORS**: Restricted to allowed origins in production.
- **Data Encryption**: Use HTTPS in deployment; store secrets securely.
- **Session Management**: Tokens stored in localStorage; implement refresh mechanisms.

## Deployment and Operations

- **Development**: Run Flask with `flask run`, React with `npm start`.
- **Production**: Build React with `npm run build`, serve static files; deploy Flask with WSGI.
- **Monitoring**: Basic logging in Flask; no advanced tools specified.
- **Testing**: Unit tests for models; integration tests for APIs.

This architecture provides a solid foundation for the food delivery platform, balancing functionality with simplicity for educational purposes.
