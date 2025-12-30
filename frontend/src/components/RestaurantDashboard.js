import React, { useState, useEffect } from 'react';
import { orderAPI, restaurantOwnerAPI } from '../api';
import './Dashboard.css';

function RestaurantDashboard({ user, onLogout }) {
  const [orders, setOrders] = useState([]);
  const [loading, setLoading] = useState(true);
  const [showAddMenu, setShowAddMenu] = useState(false);
  const [menuForm, setMenuForm] = useState({
    restaurant_id: '',
    name: '',
    description: '',
    price: '',
    image_url: '',
    category: ''
  });

  useEffect(() => {
    fetchOrders();
  }, []);

  const fetchOrders = async () => {
    try {
      const response = await orderAPI.getAll();
      setOrders(response.data);
    } catch (err) {
      console.error('Error fetching orders:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleStatusUpdate = async (orderId, status) => {
    try {
      await orderAPI.updateStatus(orderId, status);
      fetchOrders();
    } catch (err) {
      alert('Error updating order status');
    }
  };

  const handleAddMenuItem = async (e) => {
    e.preventDefault();
    try {
      await restaurantOwnerAPI.addMenuItem(menuForm);
      alert('Menu item added successfully!');
      setShowAddMenu(false);
      setMenuForm({
        restaurant_id: '',
        name: '',
        description: '',
        price: '',
        image_url: '',
        category: ''
      });
    } catch (err) {
      alert('Error adding menu item: ' + (err.response?.data?.error || 'Unknown error'));
    }
  };

  return (
    <div className="dashboard">
      <div className="header">
        <div>
          <h1>🏪 Restaurant Dashboard</h1>
          <p>Welcome, {user.name}</p>
        </div>
        <div>
          <button onClick={() => setShowAddMenu(!showAddMenu)} className="btn btn-primary" style={{ marginRight: '10px' }}>
            {showAddMenu ? '❌ Cancel' : '➕ Add Menu Item'}
          </button>
          <button onClick={onLogout} className="btn btn-secondary">🚪 Logout</button>
        </div>
      </div>

      {showAddMenu && (
        <div className="card">
          <h2>➕ Add Menu Item</h2>
          <form onSubmit={handleAddMenuItem}>
            <div className="input-group">
              <label>Restaurant ID</label>
              <input
                type="number"
                value={menuForm.restaurant_id}
                onChange={(e) => setMenuForm({...menuForm, restaurant_id: e.target.value})}
                required
                placeholder="Enter restaurant ID"
              />
            </div>
            <div className="input-group">
              <label>Item Name</label>
              <input
                type="text"
                value={menuForm.name}
                onChange={(e) => setMenuForm({...menuForm, name: e.target.value})}
                required
              />
            </div>
            <div className="input-group">
              <label>Description</label>
              <textarea
                value={menuForm.description}
                onChange={(e) => setMenuForm({...menuForm, description: e.target.value})}
                rows="3"
              />
            </div>
            <div className="input-group">
              <label>Price</label>
              <input
                type="number"
                step="0.01"
                value={menuForm.price}
                onChange={(e) => setMenuForm({...menuForm, price: e.target.value})}
                required
              />
            </div>
            <div className="input-group">
              <label>Image URL</label>
              <input
                type="url"
                value={menuForm.image_url}
                onChange={(e) => setMenuForm({...menuForm, image_url: e.target.value})}
              />
            </div>
            <div className="input-group">
              <label>Category</label>
              <input
                type="text"
                value={menuForm.category}
                onChange={(e) => setMenuForm({...menuForm, category: e.target.value})}
              />
            </div>
            <button type="submit" className="btn btn-success">Add Item</button>
          </form>
        </div>
      )}

      <div className="card">
        <h2>📦 My Orders</h2>
        {loading ? (
          <p>Loading...</p>
        ) : (
          <table className="table">
            <thead>
              <tr>
                <th>Order ID</th>
                <th>Customer</th>
                <th>Items</th>
                <th>Amount</th>
                <th>Status</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
              {orders.map(order => (
                <tr key={order.id}>
                  <td>#{order.id}</td>
                  <td>{order.customer_name || 'N/A'}</td>
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
                  <td>
                    <select
                      value={order.status}
                      onChange={(e) => handleStatusUpdate(order.id, e.target.value)}
                      className="status-select"
                    >
                      <option value="pending">Pending</option>
                      <option value="confirmed">Confirm</option>
                      <option value="preparing">Preparing</option>
                      <option value="ready">Ready</option>
                      <option value="rejected">Reject</option>
                    </select>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </div>
    </div>
  );
}

export default RestaurantDashboard;

