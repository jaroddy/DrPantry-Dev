import { useState } from 'react';
import { authAPI } from '../services/api';
import '../styles/Auth.css';

function Login({ onSuccess, onToggle }) {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    try {
      console.log('Attempting to login user:', username);
      const response = await authAPI.login(username, password);
      const { access_token } = response.data;
      console.log('Login successful, retrieving user info');
      
      // Get user info
      const userResponse = await authAPI.getMe();
      console.log('User info retrieved successfully');
      onSuccess(userResponse.data, access_token);
    } catch (err) {
      const errorMessage = err.response?.data?.detail || 'Login failed';
      console.error('Login error:', {
        message: errorMessage,
        status: err.response?.status,
        statusText: err.response?.statusText,
        data: err.response?.data
      });
      setError(errorMessage);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="auth-box">
      <h1>Welcome to Pantry Manager</h1>
      <h2>Login</h2>
      <form onSubmit={handleSubmit}>
        <div className="form-group">
          <label>Username</label>
          <input
            type="text"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            required
            autoFocus
          />
        </div>
        <div className="form-group">
          <label>Password</label>
          <input
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
          />
        </div>
        {error && <div className="error">{error}</div>}
        <button type="submit" disabled={loading}>
          {loading ? 'Logging in...' : 'Login'}
        </button>
      </form>
      <p className="toggle-link">
        Don't have an account? <a onClick={onToggle}>Register here</a>
      </p>
    </div>
  );
}

export default Login;
