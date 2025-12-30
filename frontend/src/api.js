import axios from 'axios';

const API_URL = 'http://127.0.0.1:5001/api';

const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add token to requests
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

export const authAPI = {
  login: (username, password) => api.post('/auth/login', { username, password }),
  register: (data) => api.post('/auth/register', data),
};

export const restaurantAPI = {
  getAll: () => api.get('/restaurants'),
  getMenu: (restaurantId) => api.get(`/restaurants/${restaurantId}/menu`),
};

export const orderAPI = {
  create: (data) => api.post('/orders', data),
  getAll: () => api.get('/orders'),
  updateStatus: (orderId, status, deliveryGuyId = null) => 
    api.put(`/orders/${orderId}/status`, { status, delivery_guy_id: deliveryGuyId }),
};

export const adminAPI = {
  getUsers: () => api.get('/admin/users'),
  createRestaurant: (data) => api.post('/admin/restaurants', data),
};

export const restaurantOwnerAPI = {
  addMenuItem: (data) => api.post('/restaurant/menu', data),
};

export const deliveryAPI = {
  getAvailable: () => api.get('/delivery/available'),
};

export default api;

