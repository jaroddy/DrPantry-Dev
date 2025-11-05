import { useState, useEffect } from 'react';
import Login from './components/Login';
import Register from './components/Register';
import MainApp from './components/MainApp';
import { authAPI } from './services/api';
import './styles/App.css';

function App() {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);
  const [showRegister, setShowRegister] = useState(false);

  useEffect(() => {
    // Check if user is already logged in
    const token = localStorage.getItem('token');
    if (token) {
      authAPI.getMe()
        .then(response => {
          setUser(response.data);
          setLoading(false);
        })
        .catch(() => {
          localStorage.removeItem('token');
          setLoading(false);
        });
    } else {
      setLoading(false);
    }
  }, []);

  const handleLogin = (userData, token) => {
    localStorage.setItem('token', token);
    setUser(userData);
  };

  const handleLogout = () => {
    localStorage.removeItem('token');
    setUser(null);
  };

  if (loading) {
    return <div className="loading">Loading...</div>;
  }

  if (!user) {
    return (
      <div className="auth-container">
        {showRegister ? (
          <Register 
            onSuccess={handleLogin}
            onToggle={() => setShowRegister(false)}
          />
        ) : (
          <Login 
            onSuccess={handleLogin}
            onToggle={() => setShowRegister(true)}
          />
        )}
      </div>
    );
  }

  return <MainApp user={user} onLogout={handleLogout} />;
}

export default App;
