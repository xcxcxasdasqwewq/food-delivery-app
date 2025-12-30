import sqlite3
import hashlib
import random
from datetime import datetime, timedelta

DATABASE = 'food_delivery.db'

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def seed_database():
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    
    # Clear existing data
    c.execute('DELETE FROM order_items')
    c.execute('DELETE FROM orders')
    c.execute('DELETE FROM menu_items')
    c.execute('DELETE FROM restaurants')
    c.execute('DELETE FROM users')
    
    # Create admin user
    c.execute('''INSERT INTO users (username, password, role, name, email, phone)
                 VALUES (?, ?, ?, ?, ?, ?)''',
              ('admin', hash_password('admin123'), 'admin', 'Admin User', 'admin@foodapp.com', '1234567890'))
    admin_id = c.lastrowid
    
    # Create restaurant owners
    restaurant_owners = [
        ('rest1', hash_password('rest123'), 'restaurant', 'Pizza Palace Owner', 'pizza@foodapp.com', '1111111111'),
        ('rest2', hash_password('rest123'), 'restaurant', 'Burger King Owner', 'burger@foodapp.com', '2222222222'),
        ('rest3', hash_password('rest123'), 'restaurant', 'Sushi Master Owner', 'sushi@foodapp.com', '3333333333'),
    ]
    
    owner_ids = []
    for owner in restaurant_owners:
        c.execute('''INSERT INTO users (username, password, role, name, email, phone)
                     VALUES (?, ?, ?, ?, ?, ?)''', owner)
        owner_ids.append(c.lastrowid)
    
    # Create delivery guys
    delivery_guys = [
        ('delivery1', hash_password('delivery123'), 'delivery', 'John Delivery', 'john@foodapp.com', '4444444444'),
        ('delivery2', hash_password('delivery123'), 'delivery', 'Mike Rider', 'mike@foodapp.com', '5555555555'),
    ]
    
    delivery_ids = []
    for guy in delivery_guys:
        c.execute('''INSERT INTO users (username, password, role, name, email, phone)
                     VALUES (?, ?, ?, ?, ?, ?)''', guy)
        delivery_ids.append(c.lastrowid)
    
    # Create customer
    c.execute('''INSERT INTO users (username, password, role, name, email, phone)
                 VALUES (?, ?, ?, ?, ?, ?)''',
              ('customer1', hash_password('customer123'), 'customer', 'Customer One', 'customer@foodapp.com', '6666666666'))
    customer_id = c.lastrowid
    
    # Create restaurants
    restaurants_data = [
        ('Pizza Palace', 'Best pizza in town!', 'Italian', '123 Main St', '111-111-1111', 'https://images.unsplash.com/photo-1513104890138-7c749659a591?w=400', owner_ids[0]),
        ('Burger King', 'Juicy burgers and fries', 'American', '456 Oak Ave', '222-222-2222', 'https://images.unsplash.com/photo-1568901346375-23c9450c58cd?w=400', owner_ids[1]),
        ('Sushi Master', 'Fresh sushi daily', 'Japanese', '789 Pine Rd', '333-333-3333', 'https://images.unsplash.com/photo-1579584425555-c3ce17fd4351?w=400', owner_ids[2]),
    ]
    
    restaurant_ids = []
    for rest in restaurants_data:
        c.execute('''INSERT INTO restaurants (name, description, cuisine_type, address, phone, image_url, owner_id)
                     VALUES (?, ?, ?, ?, ?, ?, ?)''', rest)
        restaurant_ids.append(c.lastrowid)
    
    # Create menu items
    menu_items_data = [
        # Pizza Palace
        (restaurant_ids[0], 'Margherita Pizza', 'Classic tomato and mozzarella', 12.99, 'https://images.unsplash.com/photo-1574071318508-1cdbab80d002?w=300', 'Pizza'),
        (restaurant_ids[0], 'Pepperoni Pizza', 'Pepperoni and cheese', 14.99, 'https://images.unsplash.com/photo-1628840042765-356cda07504e?w=300', 'Pizza'),
        (restaurant_ids[0], 'Hawaiian Pizza', 'Ham and pineapple', 15.99, 'https://images.unsplash.com/photo-1604382354936-07c5d9983bd3?w=300', 'Pizza'),
        (restaurant_ids[0], 'Caesar Salad', 'Fresh romaine with caesar dressing', 8.99, 'https://images.unsplash.com/photo-1546793665-c74683f339c1?w=300', 'Salad'),
        # Burger King
        (restaurant_ids[1], 'Classic Burger', 'Beef patty with lettuce and tomato', 9.99, 'https://images.unsplash.com/photo-1568901346375-23c9450c58cd?w=300', 'Burgers'),
        (restaurant_ids[1], 'Cheeseburger', 'Beef patty with cheese', 10.99, 'https://images.unsplash.com/photo-1550547660-d9450f859349?w=300', 'Burgers'),
        (restaurant_ids[1], 'Bacon Burger', 'Beef patty with bacon', 12.99, 'https://images.unsplash.com/photo-1553979459-d2229ba7433a?w=400&h=300&fit=crop&q=80', 'Burgers'),
        (restaurant_ids[1], 'French Fries', 'Crispy golden fries', 4.99, 'https://images.unsplash.com/photo-1573080496219-bb080dd4f877?w=300', 'Sides'),
        # Sushi Master
        (restaurant_ids[2], 'Salmon Sushi', 'Fresh salmon nigiri', 6.99, 'https://images.unsplash.com/photo-1579584425555-c3ce17fd4351?w=300', 'Sushi'),
        (restaurant_ids[2], 'Tuna Roll', 'Tuna maki roll', 7.99, 'https://images.unsplash.com/photo-1611143669185-af800c5eabef?w=400&h=300&fit=crop&q=80', 'Sushi'),
        (restaurant_ids[2], 'Dragon Roll', 'Eel and cucumber roll', 9.99, 'https://images.unsplash.com/photo-1617196034796-73dfa7b1fd56?w=300', 'Sushi'),
        (restaurant_ids[2], 'Miso Soup', 'Traditional miso soup', 3.99, 'https://images.unsplash.com/photo-1574894709920-11b28e7367e3?w=300', 'Soup'),
    ]
    
    menu_item_ids = []
    for item in menu_items_data:
        c.execute('''INSERT INTO menu_items (restaurant_id, name, description, price, image_url, category)
                     VALUES (?, ?, ?, ?, ?, ?)''', item)
        menu_item_ids.append(c.lastrowid)
    
    # Create some sample orders
    orders_data = [
        (customer_id, restaurant_ids[0], None, 'pending', 27.98, '123 Customer St, City, State'),
        (customer_id, restaurant_ids[1], delivery_ids[0], 'confirmed', 14.98, '456 Delivery Ave, City, State'),
        (customer_id, restaurant_ids[2], delivery_ids[1], 'preparing', 16.98, '789 Food Blvd, City, State'),
    ]
    
    order_ids = []
    for order in orders_data:
        c.execute('''INSERT INTO orders (user_id, restaurant_id, delivery_guy_id, status, total_amount, delivery_address)
                     VALUES (?, ?, ?, ?, ?, ?)''', order)
        order_ids.append(c.lastrowid)
    
    # Create order items
    order_items_data = [
        (order_ids[0], menu_item_ids[0], 2, 12.99),  # 2x Margherita
        (order_ids[1], menu_item_ids[4], 1, 9.99),   # 1x Classic Burger
        (order_ids[1], menu_item_ids[7], 1, 4.99),   # 1x French Fries
        (order_ids[2], menu_item_ids[8], 2, 6.99),   # 2x Salmon Sushi
        (order_ids[2], menu_item_ids[11], 1, 3.99), # 1x Miso Soup
    ]
    
    for item in order_items_data:
        c.execute('''INSERT INTO order_items (order_id, menu_item_id, quantity, price)
                     VALUES (?, ?, ?, ?)''', item)
    
    conn.commit()
    conn.close()
    print("Database seeded successfully!")
    print("\nTest Accounts:")
    print("Admin: username=admin, password=admin123")
    print("Restaurant: username=rest1, password=rest123")
    print("Delivery: username=delivery1, password=delivery123")
    print("Customer: username=customer1, password=customer123")

if __name__ == '__main__':
    seed_database()

