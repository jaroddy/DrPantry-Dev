# Quick Start Guide

This guide will help you get the Pantry Manager app up and running quickly.

## Prerequisites

- Python 3.9 or higher
- Node.js 16 or higher
- (Optional) Tesseract OCR for receipt scanning
- OpenAI API key for ChatGPT features

## Installation

### Option 1: Using the Setup Script (Linux/Mac)

```bash
./setup.sh
```

### Option 2: Manual Setup

#### Backend Setup

1. Navigate to backend directory:
```bash
cd backend
```

2. Create and activate virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

#### Frontend Setup

1. Navigate to frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

## Configuration

1. Copy the environment example file:
```bash
cp .env.example .env
```

2. Edit `.env` and add your OpenAI API key:
```
OPENAI_API_KEY=sk-your-api-key-here
```

**Note:** The app will work without an OpenAI API key, but ChatGPT-powered features (receipt scanning AI, meal planning, chat) will not function.

## Running the Application

You need to run both the backend and frontend servers:

### Terminal 1 - Backend

```bash
cd backend
source venv/bin/activate  # On Windows: venv\Scripts\activate
python main.py
```

The backend API will start on `http://localhost:8000`

### Terminal 2 - Frontend

```bash
cd frontend
npm run dev
```

The frontend will start on `http://localhost:3000`

## First Steps

1. Open your browser to `http://localhost:3000`
2. Click "Register here" to create a new account
3. Enter a username and password (password must be entered twice)
4. You'll be automatically logged in

## Using the App

### Managing Your Pantry

1. **Add Items Manually**: You can chat with the AI to add items, though this requires an API key
2. **Scan Receipts**: Click the "📷 Scan Receipt" button to upload a grocery receipt image
3. **View Items**: See all your pantry items in the table with expiration tracking
4. **Delete Items**: Click the trash icon to remove items

### Creating Meal Plans

1. Use the chat box on the right side
2. Ask for meal plans like:
   - "Create a 7-day meal plan"
   - "Suggest dinner ideas using chicken"
   - "I want healthy meals for this week"
3. Generated meal plans appear in the "Meal Plans" tab
4. Click on any meal to see full recipes with ingredients and directions

### Viewing Data

- Toggle between "📦 My Pantry" and "🍲 Meal Plans" views
- Click on any item or meal to see detailed information
- Items show color-coded expiration warnings

## Testing Without OpenAI API Key

Without an API key, you can still:
- Create an account and log in
- Manually manage pantry items (though you'll need to add them programmatically or via the API)
- View the UI and navigate the app
- Test the table views and modals

The following features require an API key:
- Receipt scanning with AI assistance
- ChatGPT-powered meal plan generation
- AI chat assistant

## API Documentation

Once the backend is running, visit `http://localhost:8000/docs` for interactive API documentation.

## Troubleshooting

### Backend won't start
- Make sure virtual environment is activated
- Check that all dependencies are installed: `pip list`
- Verify Python version: `python --version` (must be 3.9+)

### Frontend won't start
- Check Node.js version: `node --version` (must be 16+)
- Delete `node_modules` and reinstall: `rm -rf node_modules && npm install`

### Database errors
- The SQLite database is created automatically
- If you encounter issues, delete `backend/pantry_manager.db` and restart

### OpenAI API errors
- Verify your API key is correct in `.env`
- Check you have sufficient credits in your OpenAI account
- The app will show error messages in the console if API calls fail

## Development

### Backend Development
- The backend uses FastAPI with hot-reload enabled
- Changes to Python files will automatically reload the server

### Frontend Development
- Vite provides hot module replacement (HMR)
- Changes to React components update instantly in the browser

## Building for Production

### Frontend Build
```bash
cd frontend
npm run build
```

The production build will be in `frontend/dist/`

### Backend Production
Use a production ASGI server like Gunicorn:
```bash
pip install gunicorn
gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker
```

## Security Notes

- Change the `SECRET_KEY` in production (in `backend/auth.py` or via environment variable)
- Use HTTPS in production
- Set specific CORS origins instead of allowing all (`*`)
- Never commit your `.env` file or API keys to version control

## Support

For issues or questions, please refer to the main README.md for detailed documentation.
