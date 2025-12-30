from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3
import hashlib
import jwt
import datetime
from functools import wraps
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-change-in-production'

# Configure CORS to allow all origins and methods
CORS(app, 
     origins="*",
     methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
     allow_headers=["Content-Type", "Authorization"],
     supports_credentials=False)

# Add CORS headers to all responses
@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    return response

DATABASE = 'food_delivery.db'

# Database initialization
def init_db():
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    
    # Users table
    c.execute('''CREATE TABLE IF NOT EXISTS users
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  username TEXT UNIQUE NOT NULL,
                  password TEXT NOT NULL,
                  role TEXT NOT NULL,
                  name TEXT NOT NULL,
                  email TEXT,
                  phone TEXT)''')
    
    # Restaurants table
    c.execute('''CREATE TABLE IF NOT EXISTS restaurants
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  name TEXT NOT NULL,
                  description TEXT,
                  cuisine_type TEXT,
                  address TEXT,
                  phone TEXT,
                  image_url TEXT,
                  owner_id INTEGER,
                  is_active INTEGER DEFAULT 1)''')
    
    # Menu items table
    c.execute('''CREATE TABLE IF NOT EXISTS menu_items
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  restaurant_id INTEGER NOT NULL,
                  name TEXT NOT NULL,
                  description TEXT,
                  price REAL NOT NULL,
                  image_url TEXT,
                  category TEXT,
                  FOREIGN KEY (restaurant_id) REFERENCES restaurants(id))''')
    
    # Orders table
    c.execute('''CREATE TABLE IF NOT EXISTS orders
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  user_id INTEGER,
                  restaurant_id INTEGER NOT NULL,
                  delivery_guy_id INTEGER,
                  status TEXT DEFAULT 'pending',
                  total_amount REAL NOT NULL,
                  delivery_address TEXT NOT NULL,
                  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                  FOREIGN KEY (user_id) REFERENCES users(id),
                  FOREIGN KEY (restaurant_id) REFERENCES restaurants(id),
                  FOREIGN KEY (delivery_guy_id) REFERENCES users(id))''')
    
    # Order items table
    c.execute('''CREATE TABLE IF NOT EXISTS order_items
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  order_id INTEGER NOT NULL,
                  menu_item_id INTEGER NOT NULL,
                  quantity INTEGER NOT NULL,
                  price REAL NOT NULL,
                  FOREIGN KEY (order_id) REFERENCES orders(id),
                  FOREIGN KEY (menu_item_id) REFERENCES menu_items(id))''')
    
    conn.commit()
    conn.close()

# Helper functions
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def generate_token(user_id, role):
    payload = {
        'user_id': user_id,
        'role': role,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1)
    }
    return jwt.encode(payload, app.config['SECRET_KEY'], algorithm='HS256')

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({'error': 'Token is missing'}), 401
        try:
            token = token.replace('Bearer ', '')
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
            request.current_user = data
        except:
            return jsonify({'error': 'Token is invalid'}), 401
        return f(*args, **kwargs)
    return decorated

def role_required(*roles):
    def decorator(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            if request.current_user['role'] not in roles:
                return jsonify({'error': 'Insufficient permissions'}), 403
            return f(*args, **kwargs)
        return decorated
    return decorator

# Authentication routes
@app.route('/api/auth/register', methods=['POST'])
def register():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    role = data.get('role')
    name = data.get('name')
    email = data.get('email')
    phone = data.get('phone')
    
    if not all([username, password, role, name]):
        return jsonify({'error': 'Missing required fields'}), 400
    
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    
    try:
        hashed_password = hash_password(password)
        c.execute('INSERT INTO users (username, password, role, name, email, phone) VALUES (?, ?, ?, ?, ?, ?)',
                  (username, hashed_password, role, name, email, phone))
        user_id = c.lastrowid
        conn.commit()
        token = generate_token(user_id, role)
        return jsonify({'token': token, 'user': {'id': user_id, 'username': username, 'role': role, 'name': name}}), 201
    except sqlite3.IntegrityError:
        return jsonify({'error': 'Username already exists'}), 400
    finally:
        conn.close()

@app.route('/api/auth/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    
    if not username or not password:
        return jsonify({'error': 'Username and password required'}), 400
    
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    hashed_password = hash_password(password)
    
    c.execute('SELECT id, username, role, name FROM users WHERE username = ? AND password = ?',
              (username, hashed_password))
    user = c.fetchone()
    conn.close()
    
    if user:
        token = generate_token(user[0], user[2])
        return jsonify({
            'token': token,
            'user': {'id': user[0], 'username': user[1], 'role': user[2], 'name': user[3]}
        }), 200
    else:
        return jsonify({'error': 'Invalid credentials'}), 401

# Restaurant routes
@app.route('/api/restaurants', methods=['GET'])
def get_restaurants():
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute('SELECT * FROM restaurants WHERE is_active = 1')
    restaurants = []
    for row in c.fetchall():
        restaurants.append({
            'id': row[0],
            'name': row[1],
            'description': row[2],
            'cuisine_type': row[3],
            'address': row[4],
            'phone': row[5],
            'image_url': row[6],
            'owner_id': row[7]
        })
    conn.close()
    return jsonify(restaurants), 200

@app.route('/api/restaurants/<int:restaurant_id>/menu', methods=['GET'])
def get_menu(restaurant_id):
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute('SELECT * FROM menu_items WHERE restaurant_id = ?', (restaurant_id,))
    menu_items = []
    for row in c.fetchall():
        menu_items.append({
            'id': row[0],
            'restaurant_id': row[1],
            'name': row[2],
            'description': row[3],
            'price': row[4],
            'image_url': row[5],
            'category': row[6]
        })
    conn.close()
    return jsonify(menu_items), 200

# Order routes
@app.route('/api/orders', methods=['POST'])
@token_required
def create_order():
    data = request.json
    user_id = request.current_user['user_id']
    restaurant_id = data.get('restaurant_id')
    items = data.get('items')
    delivery_address = data.get('delivery_address')
    
    if not all([restaurant_id, items, delivery_address]):
        return jsonify({'error': 'Missing required fields'}), 400
    
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    
    # Calculate total
    total = 0
    for item in items:
        c.execute('SELECT price FROM menu_items WHERE id = ?', (item['menu_item_id'],))
        price_row = c.fetchone()
        if price_row:
            total += price_row[0] * item['quantity']
    
    # Create order
    c.execute('INSERT INTO orders (user_id, restaurant_id, total_amount, delivery_address, status) VALUES (?, ?, ?, ?, ?)',
              (user_id, restaurant_id, total, delivery_address, 'pending'))
    order_id = c.lastrowid
    
    # Add order items
    for item in items:
        c.execute('SELECT price FROM menu_items WHERE id = ?', (item['menu_item_id'],))
        price_row = c.fetchone()
        if price_row:
            c.execute('INSERT INTO order_items (order_id, menu_item_id, quantity, price) VALUES (?, ?, ?, ?)',
                      (order_id, item['menu_item_id'], item['quantity'], price_row[0]))
    
    conn.commit()
    conn.close()
    return jsonify({'message': 'Order created', 'order_id': order_id}), 201

@app.route('/api/orders', methods=['GET'])
@token_required
def get_orders():
    role = request.current_user['role']
    user_id = request.current_user['user_id']
    
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    
    if role == 'admin':
        c.execute('''SELECT o.*, r.name as restaurant_name, u.name as customer_name 
                     FROM orders o 
                     LEFT JOIN restaurants r ON o.restaurant_id = r.id
                     LEFT JOIN users u ON o.user_id = u.id
                     ORDER BY o.created_at DESC''')
    elif role == 'restaurant':
        c.execute('''SELECT o.*, r.name as restaurant_name, u.name as customer_name 
                     FROM orders o 
                     LEFT JOIN restaurants r ON o.restaurant_id = r.id
                     LEFT JOIN users u ON o.user_id = u.id
                     WHERE o.restaurant_id IN (SELECT id FROM restaurants WHERE owner_id = ?)
                     ORDER BY o.created_at DESC''', (user_id,))
    elif role == 'delivery':
        c.execute('''SELECT o.*, r.name as restaurant_name, u.name as customer_name 
                     FROM orders o 
                     LEFT JOIN restaurants r ON o.restaurant_id = r.id
                     LEFT JOIN users u ON o.user_id = u.id
                     WHERE o.delivery_guy_id = ? OR (o.delivery_guy_id IS NULL AND o.status = 'confirmed')
                     ORDER BY o.created_at DESC''', (user_id,))
    else:
        c.execute('''SELECT o.*, r.name as restaurant_name, u.name as customer_name 
                     FROM orders o 
                     LEFT JOIN restaurants r ON o.restaurant_id = r.id
                     LEFT JOIN users u ON o.user_id = u.id
                     WHERE o.user_id = ?
                     ORDER BY o.created_at DESC''', (user_id,))
    
    orders = []
    for row in c.fetchall():
        # Get order items
        c.execute('''SELECT mi.name, oi.quantity, oi.price 
                     FROM order_items oi 
                     JOIN menu_items mi ON oi.menu_item_id = mi.id 
                     WHERE oi.order_id = ?''', (row[0],))
        items = [{'name': item[0], 'quantity': item[1], 'price': item[2]} for item in c.fetchall()]
        
        orders.append({
            'id': row[0],
            'user_id': row[1],
            'restaurant_id': row[2],
            'delivery_guy_id': row[3],
            'status': row[4],
            'total_amount': row[5],
            'delivery_address': row[6],
            'created_at': row[7],
            'restaurant_name': row[8] if len(row) > 8 else None,
            'customer_name': row[9] if len(row) > 9 else None,
            'items': items
        })
    
    conn.close()
    return jsonify(orders), 200

@app.route('/api/orders/<int:order_id>/status', methods=['PUT'])
@token_required
def update_order_status(order_id):
    data = request.json
    new_status = data.get('status')
    role = request.current_user['role']
    user_id = request.current_user['user_id']
    
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    
    # Check permissions
    c.execute('SELECT restaurant_id, delivery_guy_id FROM orders WHERE id = ?', (order_id,))
    order = c.fetchone()
    if not order:
        conn.close()
        return jsonify({'error': 'Order not found'}), 404
    
    # Restaurant can confirm or reject
    if role == 'restaurant':
        c.execute('SELECT owner_id FROM restaurants WHERE id = ?', (order[0],))
        owner = c.fetchone()
        if owner and owner[0] == user_id:
            if new_status in ['confirmed', 'rejected', 'preparing', 'ready']:
                c.execute('UPDATE orders SET status = ? WHERE id = ?', (new_status, order_id))
                conn.commit()
                conn.close()
                return jsonify({'message': 'Order status updated'}), 200
    
    # Delivery guy can accept and update delivery status
    if role == 'delivery':
        if new_status == 'accepted':
            c.execute('UPDATE orders SET delivery_guy_id = ?, status = ? WHERE id = ? AND delivery_guy_id IS NULL',
                      (user_id, 'accepted', order_id))
        elif new_status in ['picked_up', 'delivered']:
            c.execute('UPDATE orders SET status = ? WHERE id = ? AND delivery_guy_id = ?',
                      (new_status, order_id, user_id))
        conn.commit()
        conn.close()
        return jsonify({'message': 'Order status updated'}), 200
    
    # Admin can do anything
    if role == 'admin':
        delivery_guy_id = data.get('delivery_guy_id')
        if delivery_guy_id:
            c.execute('UPDATE orders SET delivery_guy_id = ?, status = ? WHERE id = ?',
                      (delivery_guy_id, new_status, order_id))
        else:
            c.execute('UPDATE orders SET status = ? WHERE id = ?', (new_status, order_id))
        conn.commit()
        conn.close()
        return jsonify({'message': 'Order status updated'}), 200
    
    conn.close()
    return jsonify({'error': 'Insufficient permissions'}), 403

# Admin routes
@app.route('/api/admin/users', methods=['GET'])
@token_required
@role_required('admin')
def get_all_users():
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute('SELECT id, username, role, name, email, phone FROM users')
    users = []
    for row in c.fetchall():
        users.append({
            'id': row[0],
            'username': row[1],
            'role': row[2],
            'name': row[3],
            'email': row[4],
            'phone': row[5]
        })
    conn.close()
    return jsonify(users), 200

@app.route('/api/admin/restaurants', methods=['POST'])
@token_required
@role_required('admin')
def create_restaurant():
    data = request.json
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute('''INSERT INTO restaurants (name, description, cuisine_type, address, phone, image_url, owner_id)
                 VALUES (?, ?, ?, ?, ?, ?, ?)''',
              (data.get('name'), data.get('description'), data.get('cuisine_type'),
               data.get('address'), data.get('phone'), data.get('image_url'), data.get('owner_id')))
    conn.commit()
    restaurant_id = c.lastrowid
    conn.close()
    return jsonify({'message': 'Restaurant created', 'id': restaurant_id}), 201

# Restaurant owner routes
@app.route('/api/restaurant/menu', methods=['POST'])
@token_required
@role_required('restaurant')
def add_menu_item():
    data = request.json
    user_id = request.current_user['user_id']
    
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    
    # Verify ownership
    c.execute('SELECT id FROM restaurants WHERE owner_id = ? AND id = ?',
              (user_id, data.get('restaurant_id')))
    if not c.fetchone():
        conn.close()
        return jsonify({'error': 'Not your restaurant'}), 403
    
    c.execute('''INSERT INTO menu_items (restaurant_id, name, description, price, image_url, category)
                 VALUES (?, ?, ?, ?, ?, ?)''',
              (data.get('restaurant_id'), data.get('name'), data.get('description'),
               data.get('price'), data.get('image_url'), data.get('category')))
    conn.commit()
    item_id = c.lastrowid
    conn.close()
    return jsonify({'message': 'Menu item added', 'id': item_id}), 201

@app.route('/api/delivery/available', methods=['GET'])
@token_required
@role_required('delivery')
def get_available_orders():
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute('''SELECT o.*, r.name as restaurant_name, u.name as customer_name 
                 FROM orders o 
                 LEFT JOIN restaurants r ON o.restaurant_id = r.id
                 LEFT JOIN users u ON o.user_id = u.id
                 WHERE o.status = 'confirmed' AND o.delivery_guy_id IS NULL
                 ORDER BY o.created_at DESC''')
    orders = []
    for row in c.fetchall():
        orders.append({
            'id': row[0],
            'restaurant_name': row[8] if len(row) > 8 else None,
            'customer_name': row[9] if len(row) > 9 else None,
            'total_amount': row[5],
            'delivery_address': row[6],
            'created_at': row[7]
        })
    conn.close()
    return jsonify(orders), 200

if __name__ == '__main__':
    init_db()
    print("Database initialized!")
    print("Server running on http://127.0.0.1:5001")
    app.run(debug=True, host='127.0.0.1', port=5001)

