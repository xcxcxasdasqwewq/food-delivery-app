import React, { useState, useEffect } from 'react';
import { restaurantAPI, orderAPI } from '../api';
import './Dashboard.css';

function CustomerDashboard({ user, onLogout }) {
  const [restaurants, setRestaurants] = useState([]);
  const [selectedRestaurant, setSelectedRestaurant] = useState(null);
  const [menu, setMenu] = useState([]);
  const [cart, setCart] = useState([]);
  const [orders, setOrders] = useState([]);
  const [showCheckout, setShowCheckout] = useState(false);
  const [deliveryAddress, setDeliveryAddress] = useState('');

  useEffect(() => {
    fetchRestaurants();
    fetchOrders();
  }, []);

  const fetchRestaurants = async () => {
    try {
      const response = await restaurantAPI.getAll();
      setRestaurants(response.data);
    } catch (err) {
      console.error('Error fetching restaurants:', err);
    }
  };

  const fetchMenu = async (restaurantId) => {
    try {
      const response = await restaurantAPI.getMenu(restaurantId);
      setMenu(response.data);
      setSelectedRestaurant(restaurantId);
    } catch (err) {
      console.error('Error fetching menu:', err);
    }
  };

  const fetchOrders = async () => {
    try {
      const response = await orderAPI.getAll();
      setOrders(response.data);
    } catch (err) {
      console.error('Error fetching orders:', err);
    }
  };

  const addToCart = (item) => {
    const existingItem = cart.find(c => c.menu_item_id === item.id);
    if (existingItem) {
      setCart(cart.map(c => 
        c.menu_item_id === item.id 
          ? { ...c, quantity: c.quantity + 1 }
          : c
      ));
    } else {
      setCart([...cart, { menu_item_id: item.id, quantity: 1, name: item.name, price: item.price }]);
    }
  };

  const removeFromCart = (itemId) => {
    setCart(cart.filter(c => c.menu_item_id !== itemId));
  };

  const updateQuantity = (itemId, quantity) => {
    if (quantity <= 0) {
      removeFromCart(itemId);
    } else {
      setCart(cart.map(c => 
        c.menu_item_id === itemId 
          ? { ...c, quantity }
          : c
      ));
    }
  };

  const getTotal = () => {
    return cart.reduce((sum, item) => sum + (item.price * item.quantity), 0);
  };

  const handleCheckout = async (e) => {
    e.preventDefault();
    if (!deliveryAddress) {
      alert('Please enter delivery address');
      return;
    }

    try {
      await orderAPI.create({
        restaurant_id: selectedRestaurant,
        items: cart,
        delivery_address: deliveryAddress
      });
      alert('Order placed successfully!');
      setCart([]);
      setShowCheckout(false);
      setDeliveryAddress('');
      fetchOrders();
    } catch (err) {
      alert('Error placing order: ' + (err.response?.data?.error || 'Unknown error'));
    }
  };

  return (
    <div className="dashboard">
      <div className="header">
        <div>
          <h1>🍔 Food Delivery</h1>
          <p>Welcome, {user.name}</p>
        </div>
        <div>
          <button 
            onClick={() => setShowCheckout(true)} 
            className="btn btn-primary"
            style={{ marginRight: '10px' }}
            disabled={cart.length === 0}
          >
            🛒 Cart ({cart.length})
          </button>
          <button onClick={onLogout} className="btn btn-secondary">🚪 Logout</button>
        </div>
      </div>

      {showCheckout && (
        <div className="card">
          <h2>🛒 Checkout</h2>
          <div className="cart-items">
            {cart.map(item => (
              <div key={item.menu_item_id} className="cart-item">
                <div>
                  <strong>{item.name}</strong>
                  <p>${item.price.toFixed(2)} each</p>
                </div>
                <div className="cart-controls">
                  <button onClick={() => updateQuantity(item.menu_item_id, item.quantity - 1)}>-</button>
                  <span>{item.quantity}</span>
                  <button onClick={() => updateQuantity(item.menu_item_id, item.quantity + 1)}>+</button>
                  <button onClick={() => removeFromCart(item.menu_item_id)} className="btn btn-danger" style={{ marginLeft: '10px' }}>
                    Remove
                  </button>
                </div>
              </div>
            ))}
          </div>
          <div className="cart-total">
            <strong>Total: ${getTotal().toFixed(2)}</strong>
          </div>
          <form onSubmit={handleCheckout}>
            <div className="input-group">
              <label>Delivery Address</label>
              <input
                type="text"
                value={deliveryAddress}
                onChange={(e) => setDeliveryAddress(e.target.value)}
                required
                placeholder="Enter your delivery address"
              />
            </div>
            <div style={{ display: 'flex', gap: '10px' }}>
              <button type="submit" className="btn btn-success">✅ Place Order</button>
              <button type="button" onClick={() => setShowCheckout(false)} className="btn btn-secondary">
                ❌ Cancel
              </button>
            </div>
          </form>
        </div>
      )}

      <div className="card">
        <h2>🏪 Restaurants</h2>
        <div className="grid">
            {restaurants.map(restaurant => (
              <div key={restaurant.id} className="restaurant-card">
                <img 
                  src={restaurant.image_url || 'https://via.placeholder.com/300'} 
                  alt={restaurant.name}
                  onError={(e) => {
                    e.target.onerror = null;
                    e.target.src = 'https://via.placeholder.com/300/667eea/ffffff?text=' + encodeURIComponent(restaurant.name);
                  }}
                />
              <h3>{restaurant.name}</h3>
              <p>{restaurant.description}</p>
              <p><strong>Cuisine:</strong> {restaurant.cuisine_type}</p>
              <button onClick={() => fetchMenu(restaurant.id)} className="btn btn-primary">
                👀 View Menu
              </button>
            </div>
          ))}
        </div>
      </div>

      {selectedRestaurant && menu.length > 0 && (
        <div className="card">
          <h2>🍽️ Menu</h2>
          <button onClick={() => { setSelectedRestaurant(null); setMenu([]); }} className="btn btn-secondary" style={{ marginBottom: '20px' }}>
            ← Back to Restaurants
          </button>
          <div className="grid">
            {menu.map(item => (
              <div key={item.id} className="menu-item-card">
                <img 
                  src={item.image_url || 'https://via.placeholder.com/200'} 
                  alt={item.name}
                  onError={(e) => {
                    e.target.onerror = null;
                    e.target.src = 'https://via.placeholder.com/200/667eea/ffffff?text=' + encodeURIComponent(item.name);
                  }}
                />
                <h3>{item.name}</h3>
                <p>{item.description}</p>
                <p className="price">${item.price.toFixed(2)}</p>
                <button onClick={() => addToCart(item)} className="btn btn-primary">
                  ➕ Add to Cart
                </button>
              </div>
            ))}
          </div>
        </div>
      )}

      <div className="card">
        <h2>📋 My Orders</h2>
        {orders.length === 0 ? (
          <p>No orders yet.</p>
        ) : (
          <table className="table">
            <thead>
              <tr>
                <th>Order ID</th>
                <th>Restaurant</th>
                <th>Items</th>
                <th>Amount</th>
                <th>Status</th>
                <th>Address</th>
              </tr>
            </thead>
            <tbody>
              {orders.map(order => (
                <tr key={order.id}>
                  <td>#{order.id}</td>
                  <td>{order.restaurant_name || 'N/A'}</td>
                  <td>
                    {order.items?.map((item, idx) => (
                      <div key={idx}>{item.name} x{item.quantity}</div>
                    ))}
                  </td>
                  <td>${order.total_amount.toFixed(2)}</td>
                  <td>
                    <span className={`status-badge status-${order.status}`}>
                      {order.status}
                    </span>
                  </td>
                  <td>{order.delivery_address}</td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </div>
    </div>
  );
}

export default CustomerDashboard;

