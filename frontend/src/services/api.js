import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8001/api';

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

// Add error interceptor to log errors to backend
api.interceptors.response.use(
  (response) => response,
  async (error) => {
    // Log error to backend if we have a token (user is logged in)
    const token = localStorage.getItem('token');
    if (token && error.config && !error.config.url?.includes('/log/frontend-error')) {
      try {
        // Extract error details
        const errorLog = {
          error_message: error.message || 'Unknown error',
          error_stack: error.stack || null,
          url: window.location.href,
          user_agent: navigator.userAgent,
          timestamp: new Date().toISOString(),
          additional_data: {
            request_url: error.config.url,
            request_method: error.config.method,
            response_status: error.response?.status,
            response_data: error.response?.data
          }
        };

        // Send to backend (don't await to avoid blocking)
        api.post('/log/frontend-error', errorLog).catch(() => {
          // Silently fail if logging fails
          console.warn('Failed to log error to backend');
        });
      } catch (loggingError) {
        // Don't let logging errors break the app
        console.warn('Error while logging to backend:', loggingError);
      }
    }
    
    return Promise.reject(error);
  }
);

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
  sendMessage: (message, context = null) => 
    api.post('/chat', { message, context })
};

export default api;
