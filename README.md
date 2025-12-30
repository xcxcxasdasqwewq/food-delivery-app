# 🍔 Food Delivery App

A beautiful and simple food delivery web application with role-based access control for Admin, Restaurant, Delivery, and Customer roles.

## ✨ Features

- **Multi-role System**: Admin, Restaurant Owner, Delivery Person, and Customer
- **Beautiful UI**: Modern, responsive design with gradient backgrounds and smooth animations
- **Real-time Updates**: Order status updates across all roles
- **SQLite Database**: Simple local database with pre-seeded mock data
- **RESTful API**: Clean Python Flask backend
- **React Frontend**: Modern React with routing and role-based views

## 🚀 Quick Start

### Option 1: One-Command Start (Recommended)

Simply run the startup script:

```bash
chmod +x start.sh
./start.sh
```

This script will:
1. Set up Python virtual environment
2. Install backend dependencies
3. Initialize and seed the database
4. Install frontend dependencies
5. Start both backend and frontend servers

### Option 2: Manual Setup

#### Backend Setup

```bash
cd backend
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
python3 -c "from app import init_db; init_db()"
python3 seed_data.py
python3 app.py
```

Backend will run on `http://127.0.0.1:5001`

#### Frontend Setup

```bash
cd frontend
npm install
npm start
```

Frontend will run on `http://localhost:3000`

## 👤 Test Accounts

| Role | Username | Password |
|------|----------|----------|
| Admin | `admin` | `admin123` |
| Restaurant | `rest1` | `rest123` |
| Delivery | `delivery1` | `delivery123` |
| Customer | `customer1` | `customer123` |

## 📁 Project Structure

```
food-delivery-app/
├── backend/
│   ├── app.py              # Flask backend application
│   ├── seed_data.py        # Database seeding script
│   ├── requirements.txt    # Python dependencies
│   └── food_delivery.db    # SQLite database (created on first run)
├── frontend/
│   ├── public/
│   ├── src/
│   │   ├── components/     # React components
│   │   ├── App.js          # Main app component
│   │   ├── api.js          # API client
│   │   └── index.js        # Entry point
│   └── package.json
├── start.sh                # Startup script
└── README.md
```

## 🎯 Role Capabilities

### 👨‍💼 Admin
- View all users and orders
- Manage order statuses
- Create restaurants
- Full system overview

### 🏪 Restaurant Owner
- View orders for their restaurant
- Update order status (confirm, preparing, ready, reject)
- Add menu items to their restaurant

### 🚴 Delivery Person
- View available orders
- Accept orders for delivery
- Update delivery status (picked up, delivered)

### 👤 Customer
- Browse restaurants and menus
- Add items to cart
- Place orders
- View order history and status

## 🗄️ Database Schema

- **users**: User accounts with roles
- **restaurants**: Restaurant information
- **menu_items**: Menu items for each restaurant
- **orders**: Order records
- **order_items**: Items in each order

## 🔧 API Endpoints

### Authentication
- `POST /api/auth/login` - User login
- `POST /api/auth/register` - User registration

### Restaurants
- `GET /api/restaurants` - Get all restaurants
- `GET /api/restaurants/:id/menu` - Get restaurant menu

### Orders
- `GET /api/orders` - Get orders (role-based)
- `POST /api/orders` - Create new order
- `PUT /api/orders/:id/status` - Update order status

### Admin
- `GET /api/admin/users` - Get all users
- `POST /api/admin/restaurants` - Create restaurant

### Restaurant Owner
- `POST /api/restaurant/menu` - Add menu item

### Delivery
- `GET /api/delivery/available` - Get available orders

## 🎨 Design Features

- Gradient backgrounds
- Card-based layouts
- Smooth hover effects
- Responsive grid layouts
- Status badges with color coding
- Modern typography (Inter font)

## 🛠️ Technologies Used

### Backend
- Python 3
- Flask
- SQLite
- JWT for authentication
- Flask-CORS

### Frontend
- React 18
- React Router
- Axios
- CSS3 (no frameworks for simplicity)

## 📝 Notes

- The database is automatically created on first run
- Mock data is seeded automatically
- All passwords are hashed using SHA-256
- JWT tokens expire after 24 hours
- CORS is enabled for local development

## 🐛 Troubleshooting

**Backend won't start:**
- Make sure Python 3 is installed
- Check if port 5000 is available
- Verify virtual environment is activated

**Frontend won't start:**
- Make sure Node.js is installed
- Delete `node_modules` and run `npm install` again
- Check if port 3000 is available

**Database issues:**
- Delete `food_delivery.db` and run `seed_data.py` again
- Make sure you have write permissions in the backend directory

## 📄 License

This project is open source and available for educational purposes.

---

**Enjoy your food delivery app! 🍕🍔🍜**

