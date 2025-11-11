# Pixi Setup Guide for DrPantry-Dev

This project now supports [Pixi](https://pixi.sh/), a modern package management tool that handles Python dependencies and environment management automatically. Pixi solves common Python version and dependency conflicts by creating isolated, reproducible environments.

## Why Pixi?

- **No more virtual environment headaches**: Pixi manages everything for you
- **Consistent Python versions**: Everyone on the team uses the same Python version
- **Locked dependencies**: `pixi.lock` ensures everyone has identical package versions
- **Cross-platform**: Works on Linux, macOS, and Windows
- **Fast and reliable**: Uses conda-forge and PyPI for packages

## Installation

### Install Pixi

**Linux & macOS:**
```bash
curl -fsSL https://pixi.sh/install.sh | bash
```

**Windows (PowerShell):**
```powershell
iwr -useb https://pixi.sh/install.ps1 | iex
```

**Alternative via Homebrew (macOS):**
```bash
brew install pixi
```

After installation, restart your terminal or run:
```bash
source ~/.bashrc  # Linux
source ~/.zshrc   # macOS with zsh
```

## Quick Start

### 1. Clone the repository
```bash
git clone https://github.com/jaroddy/DrPantry-Dev.git
cd DrPantry-Dev
```

### 2. Install dependencies
```bash
pixi install
```

This single command:
- Installs the correct Python version (3.12)
- Installs Node.js for the frontend
- Installs Tesseract OCR for receipt scanning
- Installs all Python packages from the `pixi.toml` and `backend/requirements.txt`

### 3. Set up environment variables
```bash
cp .env.example .env
# Edit .env and add your OPENAI_API_KEY
```

### 4. Run the application

**Option 1: Run backend and frontend separately**

Terminal 1 - Backend:
```bash
pixi run backend
```

Terminal 2 - Frontend:
```bash
pixi run frontend
```

**Option 2: Run setup and individual commands**
```bash
# First time setup (installs frontend dependencies)
pixi run setup

# Then run services
pixi run backend  # In one terminal
pixi run frontend # In another terminal
```

## Available Pixi Commands

Pixi tasks are defined in `pixi.toml`. Here are the available commands:

- `pixi install` - Install all dependencies (Python, Node.js, system packages)
- `pixi run install` - Install Python packages from requirements.txt
- `pixi run install-frontend` - Install frontend npm dependencies
- `pixi run setup` - Run both install commands above
- `pixi run backend` - Start the FastAPI backend server (port 8000)
- `pixi run frontend` - Start the React frontend dev server (port 3000)
- `pixi run start` - Alternative command to start backend

## How It Works

### pixi.toml
This file defines:
- **Project metadata**: Name, version, description
- **Dependencies**: Python 3.12, Node.js 20, Tesseract, pip
- **PyPI dependencies**: All Python packages with exact versions
- **Tasks**: Commands you can run with `pixi run <task>`

### pixi.lock
This file (auto-generated):
- Locks exact versions of ALL dependencies and sub-dependencies
- Ensures reproducible environments across different machines
- Should be committed to git

### .pixi/ directory
This folder (auto-generated):
- Contains the isolated environment
- Should NOT be committed to git (already in .gitignore)

## Comparing with Old Setup

### Old Way (venv)
```bash
# Install Python manually
# Create virtual environment
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows

# Install dependencies
pip install -r backend/requirements.txt

# Install frontend deps separately
cd frontend && npm install && cd ..

# Install Tesseract OCR system-wide
# (platform-specific instructions...)

# Run backend
cd backend && python main.py

# Run frontend (in another terminal)
cd frontend && npm run dev
```

### New Way (Pixi)
```bash
# Install everything
pixi install

# Run backend
pixi run backend

# Run frontend
pixi run frontend
```

## Troubleshooting

### Command not found: pixi
Make sure Pixi is installed and your PATH is updated. Try:
```bash
export PATH="$HOME/.pixi/bin:$PATH"
```

### Dependency resolution takes too long
Pixi uses conda-forge which can be slow on first install. Subsequent installs use a cache and are much faster.

### OpenAI API Key not set
Make sure you have a `.env` file with your `OPENAI_API_KEY`:
```bash
echo "OPENAI_API_KEY=your-key-here" > .env
```

### Port already in use
If port 8000 or 3000 is taken:
- Backend: Edit `backend/main.py` to change the port
- Frontend: Edit `frontend/vite.config.js` to change the port

## Advanced Usage

### Running commands in the Pixi environment
```bash
# Run any command in the pixi environment
pixi run python --version
pixi run node --version
pixi run tesseract --version

# Open a shell in the pixi environment
pixi shell
# Now you can run commands directly:
python --version
cd backend && python main.py
```

### Adding new Python dependencies
1. Add to `backend/requirements.txt`
2. Optionally add to `[pypi-dependencies]` in `pixi.toml` for version locking
3. Run: `pixi run install` or `pixi install`

### Updating dependencies
```bash
# Update all dependencies
pixi update

# Install after updating
pixi install
```

## Migration Notes

If you're migrating from the old venv setup:

1. You can delete your old virtual environment:
   ```bash
   rm -rf backend/venv
   ```

2. The `requirements.txt` file is still used and should be kept up-to-date

3. Pixi manages Python versions, so you don't need pyenv or system Python version management

4. All team members should use Pixi for consistency

## More Resources

- [Pixi Documentation](https://pixi.sh/)
- [Pixi GitHub](https://github.com/prefix-dev/pixi)
- [Pixi Examples](https://github.com/prefix-dev/pixi/tree/main/examples)
