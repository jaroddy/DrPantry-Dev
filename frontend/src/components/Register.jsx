import { useState } from 'react';
import { authAPI } from '../services/api';
import '../styles/Auth.css';

function Register({ onSuccess, onToggle }) {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');

    // Validate passwords match
    if (password !== confirmPassword) {
      setError('Passwords do not match');
      console.error('Registration error: Passwords do not match');
      return;
    }

    // Validate password length
    if (password.length < 8) {
      setError('Password must be at least 8 characters');
      console.error('Registration error: Password must be at least 8 characters');
      return;
    }

    setLoading(true);

    try {
      console.log('Attempting to register user:', username);
      await authAPI.register(username, password);
      console.log('Registration successful, attempting auto-login');
      
      // Auto-login after registration
      const loginResponse = await authAPI.login(username, password);
      const { access_token } = loginResponse.data;
      console.log('Login successful, retrieving user info');
      
      // Set token in localStorage before calling getMe()
      localStorage.setItem('token', access_token);
      
      // Get user info
      const userResponse = await authAPI.getMe();
      console.log('User info retrieved successfully');
      onSuccess(userResponse.data, access_token);
    } catch (err) {
      const errorMessage = err.response?.data?.detail || 'Registration failed';
      console.error('Registration error:', {
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
      <h2>Create Account</h2>
      <form onSubmit={handleSubmit}>
        <div className="form-group">
          <label>Username</label>
          <input
            type="text"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            required
            minLength={3}
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
            minLength={8}
          />
        </div>
        <div className="form-group">
          <label>Confirm Password</label>
          <input
            type="password"
            value={confirmPassword}
            onChange={(e) => setConfirmPassword(e.target.value)}
            required
            minLength={8}
          />
        </div>
        {error && <div className="error">{error}</div>}
        <button type="submit" disabled={loading}>
          {loading ? 'Creating account...' : 'Create Account'}
        </button>
      </form>
      <p className="toggle-link">
        Already have an account? <a onClick={onToggle}>Login here</a>
      </p>
    </div>
  );
}

export default Register;
