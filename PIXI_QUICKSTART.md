# Quick Reference: Pixi vs Traditional Setup

## Installation Comparison

### Traditional Setup
```bash
# 1. Install Python 3.9+ manually
# 2. Install Node.js 16+ manually  
# 3. Install Tesseract OCR manually (platform-specific)
cd backend
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
cd ../frontend
npm install
```

### Pixi Setup
```bash
# 1. Install Pixi once
curl -fsSL https://pixi.sh/install.sh | bash

# 2. Clone and setup everything
pixi install
```

## Running the Application

### Traditional
```bash
# Terminal 1
cd backend
source venv/bin/activate
python main.py

# Terminal 2
cd frontend
npm run dev
```

### Pixi
```bash
# Terminal 1
pixi run backend

# Terminal 2
pixi run frontend
```

## Available Pixi Commands

| Command | Description |
|---------|-------------|
| `pixi install` | Install all dependencies (Python, Node.js, packages) |
| `pixi run backend` | Start the FastAPI backend server |
| `pixi run frontend` | Start the React frontend dev server |
| `pixi run start` | Alternative command to start backend |
| `pixi run setup` | Install both Python and frontend dependencies |
| `pixi run install` | Install Python packages from requirements.txt |
| `pixi run install-frontend` | Install frontend npm dependencies |
| `pixi shell` | Open a shell in the pixi environment |
| `pixi info` | Show project and environment information |
| `pixi task list` | List all available tasks |

## Key Benefits of Pixi

✅ **Consistent Python version** - Everyone uses Python 3.12  
✅ **Automatic system dependencies** - Tesseract OCR installed automatically  
✅ **No virtual environment management** - Pixi handles it  
✅ **Cross-platform** - Same commands on Linux, macOS, Windows  
✅ **Locked dependencies** - pixi.lock ensures reproducibility  
✅ **Fast setup** - One command installs everything  

## Environment Variables

Both methods require setting `OPENAI_API_KEY`:

```bash
# Create .env file
cp .env.example .env
# Edit .env and add: OPENAI_API_KEY=your-key-here
```

## Troubleshooting

### Pixi not found
```bash
export PATH="$HOME/.pixi/bin:$PATH"
```

### Reset environment
```bash
rm -rf .pixi/
pixi install
```

### Check what's installed
```bash
pixi info
pixi list
```

## Migration from venv to Pixi

1. Backup any local changes
2. Delete old virtual environment: `rm -rf backend/venv`
3. Install pixi: `curl -fsSL https://pixi.sh/install.sh | bash`
4. Install dependencies: `pixi install`
5. Run with: `pixi run backend` and `pixi run frontend`

The old `requirements.txt` is still used and should be maintained!

## Documentation

- Full setup guide: [PIXI_SETUP.md](PIXI_SETUP.md)
- Traditional setup: [README.md](README.md#traditional-backend-setup)
- Pixi documentation: https://pixi.sh/
