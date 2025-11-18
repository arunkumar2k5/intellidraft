# IntelliDraft - Quick Start Guide

## 🚀 Get Started in 5 Minutes

### Step 1: Backend Setup (2 minutes)

```bash
# Navigate to backend
cd backend

# Install dependencies
pip install -r requirements.txt

# Create .env file
copy .env.example .env

# Edit .env and add your OpenRouter API key
# Get from: https://openrouter.ai/keys
# OPENROUTER_API_KEY=sk-or-v1-your-key-here

# Start backend server
python main.py
```

✅ Backend running at: http://localhost:8000

### Step 2: Frontend Setup (2 minutes)

Open a new terminal:

```bash
# Navigate to frontend
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

✅ Frontend running at: http://localhost:3000

### Step 3: Use the Application (1 minute)

1. Open http://localhost:3000 in your browser
2. Upload a .docx template (must have "2. Functional Description" section)
3. Enter a component part number (e.g., `GCM1885C1H180JA16D`)
4. Click Search
5. Review and edit parameters
6. Click "Generate Document"
7. Download your generated document!

## 📋 Prerequisites Checklist

- [ ] Python 3.10+ installed
- [ ] Node.js 18+ installed
- [ ] OpenRouter API key (get from https://openrouter.ai/keys)
- [ ] Digi-Key API access (credentials in Library/digikey.py)
- [ ] Template .docx file with "2. Functional Description" section

## 🔧 Troubleshooting

**Backend won't start?**
- Check Python version: `python --version`
- Verify .env file exists with valid API key
- Check port 8000 is not in use

**Frontend won't start?**
- Check Node version: `node --version`
- Delete node_modules and run `npm install` again
- Check port 3000 is not in use

**Document generation fails?**
- Ensure template has "2. Functional Description" section
- Check backend/outputs/ directory exists and is writable
- Verify part number exists in Digi-Key database

## 📚 Next Steps

- Read the full [README.md](README.md) for detailed documentation
- Check [backend/README.md](backend/README.md) for API details
- See [frontend/README.md](frontend/README.md) for UI customization

## 🎯 Example Part Numbers to Try

- **Capacitor**: GCM1885C1H180JA16D
- **Resistor**: ERJ-6ENF1000V
- **Inductor**: LQH3NPN100MMEL
- **Diode**: 1N4148W-7-F
- **Transistor**: 2N2222A

Happy documenting! 🎉
