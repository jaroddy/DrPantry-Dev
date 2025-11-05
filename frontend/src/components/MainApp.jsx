import { useState, useEffect } from 'react';
import PantryTable from './PantryTable';
import MealPlansTable from './MealPlansTable';
import ChatBox from './ChatBox';
import ReceiptScanner from './ReceiptScanner';
import { pantryAPI, mealPlanAPI } from '../services/api';
import '../styles/MainApp.css';

function MainApp({ user, onLogout }) {
  const [view, setView] = useState('pantry'); // 'pantry' or 'mealplans'
  const [pantryItems, setPantryItems] = useState([]);
  const [mealPlans, setMealPlans] = useState([]);
  const [loading, setLoading] = useState(true);
  const [showScanner, setShowScanner] = useState(false);

  useEffect(() => {
    loadData();
  }, []);

  const loadData = async () => {
    setLoading(true);
    try {
      const [pantryResponse, mealPlansResponse] = await Promise.all([
        pantryAPI.getAll(),
        mealPlanAPI.getAll()
      ]);
      setPantryItems(pantryResponse.data);
      setMealPlans(mealPlansResponse.data);
    } catch (err) {
      console.error('Error loading data:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleDeletePantryItem = async (id) => {
    try {
      await pantryAPI.delete(id);
      setPantryItems(pantryItems.filter(item => item.id !== id));
    } catch (err) {
      console.error('Error deleting item:', err);
      alert('Failed to delete item');
    }
  };

  const handleDeleteMealPlan = async (id) => {
    try {
      await mealPlanAPI.delete(id);
      setMealPlans(mealPlans.filter(plan => plan.id !== id));
    } catch (err) {
      console.error('Error deleting meal plan:', err);
      alert('Failed to delete meal plan');
    }
  };

  const handleReceiptScan = async (scannedItems) => {
    // Reload pantry items after scan
    await loadData();
    setShowScanner(false);
  };

  const handleChatResponse = (response) => {
    // If a meal plan was created, reload meal plans
    if (response.meal_plan) {
      loadData();
    }
  };

  return (
    <div className="main-app">
      <header className="app-header">
        <h1>🍽️ Pantry Manager</h1>
        <div className="header-actions">
          <span className="username">Welcome, {user.username}!</span>
          <button onClick={onLogout} className="logout-btn">Logout</button>
        </div>
      </header>

      <div className="app-content">
        <div className="main-section">
          <div className="view-controls">
            <button 
              className={view === 'pantry' ? 'active' : ''} 
              onClick={() => setView('pantry')}
            >
              📦 My Pantry ({pantryItems.length})
            </button>
            <button 
              className={view === 'mealplans' ? 'active' : ''} 
              onClick={() => setView('mealplans')}
            >
              🍲 Meal Plans ({mealPlans.length})
            </button>
            {view === 'pantry' && (
              <button 
                className="scan-btn"
                onClick={() => setShowScanner(!showScanner)}
              >
                📷 Scan Receipt
              </button>
            )}
          </div>

          {showScanner && (
            <ReceiptScanner 
              onSuccess={handleReceiptScan}
              onClose={() => setShowScanner(false)}
            />
          )}

          <div className="table-container">
            {loading ? (
              <div className="loading">Loading...</div>
            ) : view === 'pantry' ? (
              <PantryTable 
                items={pantryItems} 
                onDelete={handleDeletePantryItem}
                onRefresh={loadData}
              />
            ) : (
              <MealPlansTable 
                mealPlans={mealPlans} 
                onDelete={handleDeleteMealPlan}
              />
            )}
          </div>
        </div>

        <div className="chat-section">
          <ChatBox 
            pantryItems={pantryItems}
            onResponse={handleChatResponse}
          />
        </div>
      </div>
    </div>
  );
}

export default MainApp;
