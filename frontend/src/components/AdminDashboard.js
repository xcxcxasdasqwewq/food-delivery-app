import React, { useState, useEffect } from 'react';
import { adminAPI, orderAPI } from '../api';
import './Dashboard.css';

function AdminDashboard({ user, onLogout }) {
  const [users, setUsers] = useState([]);
  const [orders, setOrders] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    try {
      const [usersRes, ordersRes] = await Promise.all([
        adminAPI.getUsers(),
        orderAPI.getAll()
      ]);
      setUsers(usersRes.data);
      setOrders(ordersRes.data);
    } catch (err) {
      console.error('Error fetching data:', err);
    } finally {
      setLoading(false);
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
          <h1>👨‍💼 Admin Dashboard</h1>
          <p>Welcome, {user.name}</p>
        </div>
        <button onClick={onLogout} className="btn btn-secondary">🚪 Logout</button>
      </div>

      <div className="stats-grid">
        <div className="stat-card">
          <h3>👥 Total Users</h3>
          <p className="stat-number">{users.length}</p>
        </div>
        <div className="stat-card">
          <h3>📦 Total Orders</h3>
          <p className="stat-number">{orders.length}</p>
        </div>
        <div className="stat-card">
          <h3>⏳ Pending Orders</h3>
          <p className="stat-number">{orders.filter(o => o.status === 'pending').length}</p>
        </div>
        <div className="stat-card">
          <h3>✅ Delivered Orders</h3>
          <p className="stat-number">{orders.filter(o => o.status === 'delivered').length}</p>
        </div>
      </div>

      <div className="card">
        <h2>📋 All Orders</h2>
        {loading ? (
          <p>Loading...</p>
        ) : (
          <table className="table">
            <thead>
              <tr>
                <th>ID</th>
                <th>Customer</th>
                <th>Restaurant</th>
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
                  <td>{order.restaurant_name || 'N/A'}</td>
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
                      <option value="confirmed">Confirmed</option>
                      <option value="preparing">Preparing</option>
                      <option value="ready">Ready</option>
                      <option value="delivered">Delivered</option>
                      <option value="rejected">Rejected</option>
                    </select>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </div>

      <div className="card">
        <h2>👥 All Users</h2>
        <table className="table">
          <thead>
            <tr>
              <th>ID</th>
              <th>Username</th>
              <th>Name</th>
              <th>Role</th>
              <th>Email</th>
              <th>Phone</th>
            </tr>
          </thead>
          <tbody>
            {users.map(u => (
              <tr key={u.id}>
                <td>{u.id}</td>
                <td>{u.username}</td>
                <td>{u.name}</td>
                <td><span className="role-badge">{u.role}</span></td>
                <td>{u.email || 'N/A'}</td>
                <td>{u.phone || 'N/A'}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}

export default AdminDashboard;

