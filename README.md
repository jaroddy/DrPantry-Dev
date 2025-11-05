# Pantry Manager - Smart Food Inventory & Meal Planning App

A modern web application that helps you manage your pantry inventory and create intelligent meal plans using AI. Features receipt scanning with OCR, automated food item tracking, and ChatGPT-powered meal recommendations.

## Features

### 🔐 User Authentication
- Secure login and account creation
- Username and password authentication
- JWT-based session management

### 📦 Pantry Management
- Track all your food items with detailed information:
  - Item Name & Receipt Name
  - Expiration tracking
  - Type, Units, Volume
  - Calorie information
  - UPC codes
- Visual table interface with sorting and filtering
- Color-coded expiration warnings

### 📷 Receipt Scanning
- Camera/photo upload integration
- OCR text extraction from receipts
- Automatic item detection and parsing
- AI-powered item name normalization
- Auto-population of item details using ChatGPT

### 🌍 Global Knowledge Base
- Shared database of common food items
- Reduces API calls by reusing known item data
- Automatically updated as users add items
- Tracks typical expiration times and nutritional info

### 🍽️ Meal Planning
- AI-generated meal plans based on:
  - Your pantry contents
  - Your dietary preferences
  - Time constraints
- Detailed meal information:
  - Ingredients list
  - Step-by-step directions
  - Prep and cook times
  - Serving sizes and calories
- 7-day meal planning support

### 💬 AI Chat Assistant
- Natural language interaction
- Ask questions about your pantry
- Request custom meal plans
- Get cooking suggestions
- Powered by ChatGPT

## Tech Stack

### Backend (Python)
- **FastAPI** - High-performance async web framework
- **SQLAlchemy** - ORM with async support
- **SQLite** - Database (with aiosqlite for async)
- **OpenAI API** - ChatGPT integration
- **Tesseract OCR** - Receipt text extraction
- **Pillow** - Image processing
- **PassLib** - Password hashing
- **Python-JOSE** - JWT token handling

### Frontend (JavaScript)
- **React 18** - UI framework
- **Vite** - Fast build tool and dev server
- **Axios** - HTTP client
- **CSS3** - Modern styling with gradients and animations

## Installation

### Prerequisites
- Python 3.9+
- Node.js 16+
- npm or yarn
- Tesseract OCR installed on your system

### Backend Setup

1. Navigate to the backend directory:
```bash
cd backend
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
```bash
export OPENAI_API_KEY="your-openai-api-key"
```

5. Run the backend server:
```bash
python main.py
```

The API will be available at `http://localhost:8000`
API documentation at `http://localhost:8000/docs`

### Frontend Setup

1. Navigate to the frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Run the development server:
```bash
npm run dev
```

The app will be available at `http://localhost:3000`

## Usage

1. **Create an Account**: Register with a username and password
2. **Scan Receipts**: Use the camera button to upload grocery receipts
3. **Manage Pantry**: View and track all your food items with expiration dates
4. **Chat with AI**: Ask for meal suggestions or cooking advice
5. **Generate Meal Plans**: Request custom meal plans based on your inventory
6. **View Meal Details**: Click on meals to see full recipes with ingredients and directions

## API Endpoints

### Authentication
- `POST /api/auth/register` - Create new account
- `POST /api/auth/login` - Login and get JWT token
- `GET /api/auth/me` - Get current user info

### Pantry
- `GET /api/pantry` - List all pantry items
- `POST /api/pantry` - Add new pantry item
- `GET /api/pantry/{id}` - Get specific item
- `PUT /api/pantry/{id}` - Update item
- `DELETE /api/pantry/{id}` - Delete item
- `POST /api/receipt/scan` - Scan receipt and add items

### Meal Plans
- `GET /api/meal-plans` - List all meal plans
- `POST /api/meal-plans` - Create new meal plan
- `GET /api/meal-plans/{id}` - Get specific meal plan
- `DELETE /api/meal-plans/{id}` - Delete meal plan

### Chat
- `POST /api/chat` - Send message to AI assistant

## Database Schema

### Users
- id, username, hashed_password, created_at

### Pantry Items
- id, user_id, item_name, receipt_name, date_added
- days_before_expiry, date_estimated_expiry, perishable
- type, units, volume, calories, upc

### Global Knowledge Items
- id, item_name, typical_days_before_expiry, perishable
- type, typical_units, calories_per_unit, usage_count

### Meal Plans
- id, user_id, name, description, meals (JSON)
- created_at, updated_at

## Security Features

- Password hashing with bcrypt
- JWT token authentication
- Bearer token authorization
- CORS protection
- Input validation with Pydantic
- SQL injection prevention with SQLAlchemy ORM

## Performance Optimizations

- Async/await throughout backend
- Database query optimization with indexing
- Global knowledge cache to reduce API calls
- Efficient React re-rendering
- Vite's fast HMR for development
- Image compression for receipt uploads

## Future Enhancements

- Barcode scanning for UPC codes
- Nutrition analysis and tracking
- Shopping list generation
- Recipe sharing between users
- Mobile app version
- Multiple language support
- Integration with grocery delivery services
- Voice interface support

## License

MIT License - Feel free to use and modify as needed.