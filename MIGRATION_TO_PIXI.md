# Migration Guide: venv to Pixi

This guide is for existing DrPantry-Dev users who are currently using the traditional virtual environment setup and want to migrate to Pixi.

## Why Migrate?

If you're experiencing any of these issues:
- ❌ Python version conflicts
- ❌ Different team members have different package versions
- ❌ "Works on my machine" problems
- ❌ Complex setup with multiple manual installation steps
- ❌ Platform-specific dependency issues

Pixi solves all of these! ✨

## Quick Migration (5 minutes)

### Step 1: Install Pixi

**Linux & macOS:**
```bash
curl -fsSL https://pixi.sh/install.sh | bash
```

**Windows (PowerShell):**
```powershell
iwr -useb https://pixi.sh/install.ps1 | iex
```

Restart your terminal after installation.

### Step 2: Backup and Clean

```bash
# Make sure you're in the DrPantry-Dev directory
cd /path/to/DrPantry-Dev

# Backup any local database or config changes (optional)
# cp .env .env.backup

# Deactivate current venv if active
deactivate 2>/dev/null || true

# Remove old virtual environment
rm -rf backend/venv
```

### Step 3: Install with Pixi

```bash
# Pull latest changes if you haven't
git pull

# Install everything with Pixi
pixi install
```

This will:
- Install Python 3.12
- Install Node.js 20
- Install Tesseract OCR
- Install all Python packages
- Set up the complete environment

### Step 4: Verify Installation

```bash
# Check pixi info
pixi info

# Should show:
# - Name: drpantry-dev
# - Python, Node.js, Tesseract in dependencies
# - 6 tasks available
```

### Step 5: Run the Application

```bash
# Terminal 1 - Backend
pixi run backend

# Terminal 2 - Frontend (after frontend deps are installed)
pixi run install-frontend  # First time only
pixi run frontend
```

## What Changed?

### Before (venv)
```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python main.py
```

### After (Pixi)
```bash
pixi run backend
```

## Common Questions

### Q: Do I need to uninstall my system Python?
**A:** No! Pixi manages its own Python installation. Your system Python remains untouched.

### Q: What about my .env file?
**A:** Keep it! Your `.env` file with `OPENAI_API_KEY` is still used the same way.

### Q: Can I still use the old method?
**A:** Yes! The traditional setup still works. Both methods are supported.

### Q: What if I have local changes to requirements.txt?
**A:** The `requirements.txt` file is still used! Pixi reads from it. Your changes are preserved.

### Q: Where did my packages go?
**A:** They're in `.pixi/envs/default/`. This folder is managed by Pixi and excluded from git.

### Q: How do I add new Python packages?
**A:** Add to `backend/requirements.txt`, then run `pixi run install` or `pixi install`.

### Q: Can I still use `pip install` directly?
**A:** You can, but it's better to use Pixi's environment. Run `pixi shell` first to get a shell in the pixi environment, then use pip.

## Troubleshooting

### "Command not found: pixi"
```bash
export PATH="$HOME/.pixi/bin:$PATH"
# Add to ~/.bashrc or ~/.zshrc for permanent fix
```

### "Port already in use"
Same as before - change the port in backend/main.py or frontend config.

### "Dependencies taking too long"
First install can be slow. Subsequent installs are much faster due to caching.

### "Want to go back to venv"
```bash
# Remove pixi environment
rm -rf .pixi/

# Recreate venv
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Side-by-Side Comparison

| Task | Old Method (venv) | New Method (Pixi) |
|------|-------------------|-------------------|
| **Setup** | Multiple steps (install Python, create venv, activate, install packages) | `pixi install` |
| **Run Backend** | `cd backend && source venv/bin/activate && python main.py` | `pixi run backend` |
| **Run Frontend** | `cd frontend && npm run dev` | `pixi run frontend` |
| **Add Package** | Activate venv, pip install, update requirements.txt | Add to requirements.txt, `pixi run install` |
| **Team Sync** | "Make sure you have Python 3.9+, Node 16+, Tesseract..." | "Run `pixi install`" |
| **Cleanup** | `deactivate`, manage venv manually | Automatic |

## Advanced: Hybrid Approach

You can use both methods simultaneously if needed:

```bash
# Use Pixi for development
pixi run backend

# Use venv for testing/debugging
cd backend
source venv/bin/activate
python main.py
```

## Getting Help

- **Pixi isn't working?** See [PIXI_SETUP.md](PIXI_SETUP.md#troubleshooting)
- **Need quick commands?** Check [PIXI_QUICKSTART.md](PIXI_QUICKSTART.md)
- **Still prefer traditional?** That's fine! See [README.md](README.md#traditional-backend-setup)

## Next Steps

After migration:
1. ✅ Delete your old venv: `rm -rf backend/venv`
2. ✅ Update your README/notes with pixi commands
3. ✅ Share with your team: "We're now using Pixi!"
4. ✅ Enjoy easier dependency management! 🎉

## Rollback Plan

If you need to rollback:
```bash
# Remove pixi files
rm -rf .pixi/
rm pixi.toml pixi.lock

# Recreate venv as before
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

The `requirements.txt` is still maintained, so rolling back is always safe.
