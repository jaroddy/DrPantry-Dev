import { useState } from 'react';
import '../styles/Table.css';

function MealPlansTable({ mealPlans, onDelete }) {
  const [selectedPlan, setSelectedPlan] = useState(null);
  const [selectedMeal, setSelectedMeal] = useState(null);

  const formatDate = (dateString) => {
    const date = new Date(dateString);
    return date.toLocaleDateString();
  };

  if (mealPlans.length === 0) {
    return (
      <div className="empty-state">
        <p>No meal plans yet!</p>
        <p>Chat with the AI assistant to create one.</p>
      </div>
    );
  }

  return (
    <div className="table-wrapper">
      <table className="data-table">
        <thead>
          <tr>
            <th>Plan Name</th>
            <th>Description</th>
            <th>Number of Meals</th>
            <th>Created</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          {mealPlans.map(plan => (
            <tr key={plan.id} onClick={() => setSelectedPlan(plan)}>
              <td className="item-name">{plan.name}</td>
              <td>{plan.description || 'No description'}</td>
              <td>{plan.meals.length}</td>
              <td>{formatDate(plan.created_at)}</td>
              <td>
                <button 
                  className="delete-btn"
                  onClick={(e) => {
                    e.stopPropagation();
                    if (confirm(`Delete ${plan.name}?`)) {
                      onDelete(plan.id);
                    }
                  }}
                >
                  🗑️
                </button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>

      {selectedPlan && (
        <div className="item-modal" onClick={() => setSelectedPlan(null)}>
          <div className="modal-content large" onClick={(e) => e.stopPropagation()}>
            <h3>{selectedPlan.name}</h3>
            <p className="description">{selectedPlan.description}</p>
            
            <div className="meals-grid">
              {selectedPlan.meals.map((meal, index) => (
                <div 
                  key={index} 
                  className="meal-card"
                  onClick={(e) => {
                    e.stopPropagation();
                    setSelectedMeal(meal);
                  }}
                >
                  <h4>{meal.name}</h4>
                  <p className="meal-type">{meal.meal_type}</p>
                  <p className="meal-date">{meal.date}</p>
                  {meal.prep_time && <p>⏱️ Prep: {meal.prep_time}</p>}
                  {meal.servings && <p>🍽️ Servings: {meal.servings}</p>}
                </div>
              ))}
            </div>
            
            <button onClick={() => setSelectedPlan(null)}>Close</button>
          </div>
        </div>
      )}

      {selectedMeal && (
        <div className="item-modal" onClick={() => setSelectedMeal(null)}>
          <div className="modal-content large" onClick={(e) => e.stopPropagation()}>
            <h3>{selectedMeal.name}</h3>
            <p className="meal-type-badge">{selectedMeal.meal_type}</p>
            {selectedMeal.description && <p className="description">{selectedMeal.description}</p>}
            
            <div className="meal-details">
              <div className="meal-info">
                {selectedMeal.prep_time && <p>⏱️ Prep Time: {selectedMeal.prep_time}</p>}
                {selectedMeal.cook_time && <p>🔥 Cook Time: {selectedMeal.cook_time}</p>}
                {selectedMeal.servings && <p>🍽️ Servings: {selectedMeal.servings}</p>}
                {selectedMeal.calories && <p>📊 Calories: {Math.round(selectedMeal.calories)}</p>}
              </div>

              <h4>Ingredients</h4>
              <ul className="ingredients-list">
                {selectedMeal.ingredients.map((ing, i) => (
                  <li key={i}>
                    {ing.quantity} {ing.unit} {ing.item_name}
                  </li>
                ))}
              </ul>

              <h4>Directions</h4>
              <ol className="directions-list">
                {selectedMeal.directions.map((step, i) => (
                  <li key={i}>{step}</li>
                ))}
              </ol>
            </div>
            
            <button onClick={() => setSelectedMeal(null)}>Close</button>
          </div>
        </div>
      )}
    </div>
  );
}

export default MealPlansTable;
