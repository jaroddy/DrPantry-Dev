import React from 'react'
import ReactDOM from 'react-dom/client'
import App from './App.jsx'
import api from './services/api.js'

// Global error handler for uncaught JavaScript errors
window.addEventListener('error', (event) => {
  const token = localStorage.getItem('token');
  if (token) {
    const errorLog = {
      error_message: event.message || 'Uncaught error',
      error_stack: event.error?.stack || null,
      component: 'Global',
      url: window.location.href,
      user_agent: navigator.userAgent,
      timestamp: new Date().toISOString(),
      additional_data: {
        filename: event.filename,
        lineno: event.lineno,
        colno: event.colno
      }
    };

    // Send to backend
    api.post('/log/frontend-error', errorLog).catch(() => {
      console.warn('Failed to log error to backend');
    });
  }
});

// Global handler for unhandled promise rejections
window.addEventListener('unhandledrejection', (event) => {
  const token = localStorage.getItem('token');
  if (token) {
    const errorLog = {
      error_message: event.reason?.message || 'Unhandled promise rejection',
      error_stack: event.reason?.stack || null,
      component: 'Global',
      url: window.location.href,
      user_agent: navigator.userAgent,
      timestamp: new Date().toISOString(),
      additional_data: {
        reason: String(event.reason)
      }
    };

    // Send to backend
    api.post('/log/frontend-error', errorLog).catch(() => {
      console.warn('Failed to log error to backend');
    });
  }
});

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>,
)
