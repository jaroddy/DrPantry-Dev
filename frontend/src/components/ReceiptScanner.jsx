import { useState, useRef } from 'react';
import { pantryAPI } from '../services/api';
import '../styles/Scanner.css';

function ReceiptScanner({ onSuccess, onClose }) {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [preview, setPreview] = useState(null);
  const fileInputRef = useRef(null);

  const handleFileSelect = (e) => {
    const file = e.target.files[0];
    if (file) {
      const reader = new FileReader();
      reader.onloadend = () => {
        setPreview(reader.result);
      };
      reader.readAsDataURL(file);
    }
  };

  const handleScan = async () => {
    if (!preview) {
      setError('Please select an image first');
      return;
    }

    setLoading(true);
    setError('');

    try {
      const response = await pantryAPI.scanReceipt(preview);
      alert(response.data.message);
      onSuccess(response.data.items);
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to scan receipt');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="scanner-container">
      <div className="scanner-box">
        <h3>📷 Scan Receipt</h3>
        <p className="scanner-info">
          Upload a photo of your grocery receipt and we'll automatically add items to your pantry!
        </p>

        <div className="scanner-actions">
          <input
            ref={fileInputRef}
            type="file"
            accept="image/*"
            capture="environment"
            onChange={handleFileSelect}
            style={{ display: 'none' }}
          />
          
          <button 
            onClick={() => fileInputRef.current.click()}
            className="select-btn"
          >
            📸 Take Photo / Select Image
          </button>
        </div>

        {preview && (
          <div className="preview-container">
            <img src={preview} alt="Receipt preview" />
          </div>
        )}

        {error && <div className="error">{error}</div>}

        <div className="scanner-footer">
          <button 
            onClick={handleScan} 
            disabled={!preview || loading}
            className="scan-btn-primary"
          >
            {loading ? 'Scanning...' : 'Scan & Add Items'}
          </button>
          <button onClick={onClose} className="cancel-btn">
            Cancel
          </button>
        </div>
      </div>
    </div>
  );
}

export default ReceiptScanner;
