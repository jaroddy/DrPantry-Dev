import { useState } from 'react';
import '../styles/Table.css';

function PantryTable({ items, onDelete, onRefresh }) {
  const [selectedItem, setSelectedItem] = useState(null);

  const formatDate = (dateString) => {
    const date = new Date(dateString);
    return date.toLocaleDateString();
  };

  const getDaysUntilExpiry = (expiryDate) => {
    if (!expiryDate) return 'N/A';
    const today = new Date();
    const expiry = new Date(expiryDate);
    const days = Math.ceil((expiry - today) / (1000 * 60 * 60 * 24));
    if (days < 0) return <span className="expired">Expired</span>;
    if (days === 0) return <span className="expiring-soon">Today!</span>;
    if (days <= 3) return <span className="expiring-soon">{days} days</span>;
    return `${days} days`;
  };

  if (items.length === 0) {
    return (
      <div className="empty-state">
        <p>Your pantry is empty!</p>
        <p>Scan a receipt or add items to get started.</p>
      </div>
    );
  }

  return (
    <div className="table-wrapper">
      <table className="data-table">
        <thead>
          <tr>
            <th>Item Name</th>
            <th>Receipt Name</th>
            <th>Type</th>
            <th>Volume</th>
            <th>Units</th>
            <th>Calories</th>
            <th>Perishable</th>
            <th>Days Until Expiry</th>
            <th>Date Added</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          {items.map(item => (
            <tr key={item.id} onClick={() => setSelectedItem(item)}>
              <td className="item-name">{item.item_name}</td>
              <td>{item.receipt_name || '-'}</td>
              <td>{item.type || '-'}</td>
              <td>{item.volume || '-'}</td>
              <td>{item.units || '-'}</td>
              <td>{item.calories ? Math.round(item.calories) : '-'}</td>
              <td>{item.perishable ? '✓' : '✗'}</td>
              <td>{getDaysUntilExpiry(item.date_estimated_expiry)}</td>
              <td>{formatDate(item.date_added)}</td>
              <td>
                <button 
                  className="delete-btn"
                  onClick={(e) => {
                    e.stopPropagation();
                    if (confirm(`Delete ${item.item_name}?`)) {
                      onDelete(item.id);
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

      {selectedItem && (
        <div className="item-modal" onClick={() => setSelectedItem(null)}>
          <div className="modal-content" onClick={(e) => e.stopPropagation()}>
            <h3>{selectedItem.item_name}</h3>
            <div className="item-details">
              <p><strong>Receipt Name:</strong> {selectedItem.receipt_name || 'N/A'}</p>
              <p><strong>Type:</strong> {selectedItem.type || 'N/A'}</p>
              <p><strong>Volume:</strong> {selectedItem.volume} {selectedItem.units}</p>
              <p><strong>Calories:</strong> {selectedItem.calories ? Math.round(selectedItem.calories) : 'N/A'}</p>
              <p><strong>Perishable:</strong> {selectedItem.perishable ? 'Yes' : 'No'}</p>
              <p><strong>Days Before Expiry:</strong> {selectedItem.days_before_expiry || 'N/A'}</p>
              <p><strong>Estimated Expiry:</strong> {selectedItem.date_estimated_expiry ? formatDate(selectedItem.date_estimated_expiry) : 'N/A'}</p>
              <p><strong>Date Added:</strong> {formatDate(selectedItem.date_added)}</p>
              {selectedItem.upc && <p><strong>UPC:</strong> {selectedItem.upc}</p>}
            </div>
            <button onClick={() => setSelectedItem(null)}>Close</button>
          </div>
        </div>
      )}
    </div>
  );
}

export default PantryTable;
