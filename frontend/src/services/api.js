import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api';

// Create axios instance
const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json'
  }
});

// Add auth token to requests
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Auth API
export const authAPI = {
  register: (username, password) => 
    api.post('/auth/register', { username, password }),
  
  login: (username, password) => 
    api.post('/auth/login', { username, password }),
  
  getMe: () => 
    api.get('/auth/me')
};

// Pantry API
export const pantryAPI = {
  getAll: () => 
    api.get('/pantry'),
  
  getById: (id) => 
    api.get(`/pantry/${id}`),
  
  create: (item) => 
    api.post('/pantry', item),
  
  update: (id, item) => 
    api.put(`/pantry/${id}`, item),
  
  delete: (id) => 
    api.delete(`/pantry/${id}`),
  
  scanReceipt: (imageBase64) => 
    api.post('/receipt/scan', { image_base64: imageBase64 })
};

// Meal Plan API
export const mealPlanAPI = {
  getAll: () => 
    api.get('/meal-plans'),
  
  getById: (id) => 
    api.get(`/meal-plans/${id}`),
  
  create: (mealPlan) => 
    api.post('/meal-plans', mealPlan),
  
  delete: (id) => 
    api.delete(`/meal-plans/${id}`)
};

// Chat API
export const chatAPI = {
  sendMessage: (message, context = null, conversationHistory = null) => 
    api.post('/chat', { 
      message, 
      context,
      conversation_history: conversationHistory 
    })
};

export default api;
