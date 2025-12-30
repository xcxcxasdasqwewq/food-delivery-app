import React, { useState, useEffect } from 'react';
import { orderAPI, deliveryAPI } from '../api';
import './Dashboard.css';

function DeliveryDashboard({ user, onLogout }) {
  const [myOrders, setMyOrders] = useState([]);
  const [availableOrders, setAvailableOrders] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchData();
    const interval = setInterval(fetchData, 5000); // Refresh every 5 seconds
    return () => clearInterval(interval);
  }, []);

  const fetchData = async () => {
    try {
      const [myOrdersRes, availableRes] = await Promise.all([
        orderAPI.getAll(),
        deliveryAPI.getAvailable()
      ]);
      setMyOrders(myOrdersRes.data);
      setAvailableOrders(availableRes.data);
    } catch (err) {
      console.error('Error fetching data:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleAcceptOrder = async (orderId) => {
    try {
      await orderAPI.updateStatus(orderId, 'accepted');
      fetchData();
    } catch (err) {
      alert('Error accepting order');
    }
  };

  const handleStatusUpdate = async (orderId, status) => {
    try {
      await orderAPI.updateStatus(orderId, status);
      fetchData();
    } catch (err) {
      alert('Error updating order status');
    }
  };

  return (
    <div className="dashboard">
      <div className="header">
        <div>
          <h1>🚴 Delivery Dashboard</h1>
          <p>Welcome, {user.name}</p>
        </div>
        <button onClick={onLogout} className="btn btn-secondary">🚪 Logout</button>
      </div>

      <div className="card">
        <h2>📬 Available Orders</h2>
        {loading ? (
          <p>Loading...</p>
        ) : availableOrders.length === 0 ? (
          <p>No available orders at the moment.</p>
        ) : (
          <div className="grid">
            {availableOrders.map(order => (
              <div key={order.id} className="order-card">
                <h3>Order #{order.id}</h3>
                <p><strong>Restaurant:</strong> {order.restaurant_name}</p>
                <p><strong>Customer:</strong> {order.customer_name}</p>
                <p><strong>Amount:</strong> ${order.total_amount.toFixed(2)}</p>
                <p><strong>Address:</strong> {order.delivery_address}</p>
                <button
                  onClick={() => handleAcceptOrder(order.id)}
                  className="btn btn-success"
                  style={{ width: '100%', marginTop: '10px' }}
                >
                  ✅ Accept Order
                </button>
              </div>
            ))}
          </div>
        )}
      </div>

      <div className="card">
        <h2>🚚 My Active Orders</h2>
        {loading ? (
          <p>Loading...</p>
        ) : myOrders.length === 0 ? (
          <p>No active orders.</p>
        ) : (
          <table className="table">
            <thead>
              <tr>
                <th>Order ID</th>
                <th>Restaurant</th>
                <th>Customer</th>
                <th>Address</th>
                <th>Amount</th>
                <th>Status</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
              {myOrders.map(order => (
                <tr key={order.id}>
                  <td>#{order.id}</td>
                  <td>{order.restaurant_name || 'N/A'}</td>
                  <td>{order.customer_name || 'N/A'}</td>
                  <td>{order.delivery_address}</td>
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
                      <option value="accepted">Accepted</option>
                      <option value="picked_up">Picked Up</option>
                      <option value="delivered">Delivered</option>
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

export default DeliveryDashboard;

