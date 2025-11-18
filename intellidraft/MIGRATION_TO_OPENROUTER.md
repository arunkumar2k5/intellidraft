# Migration to OpenRouter API - Summary

## Changes Made

The application has been successfully updated to use **OpenRouter API** instead of direct OpenAI API.

## What Changed

### 1. Backend Code
**File: `backend/services/openai_service.py`**
- Replaced `openai` library with direct HTTP requests using `requests`
- Updated API endpoint to OpenRouter: `https://openrouter.ai/api/v1/chat/completions`
- Changed authentication to use OpenRouter API key
- Added OpenRouter-specific headers (`HTTP-Referer`, `X-Title`)
- Model specification now uses OpenRouter format: `openai/gpt-3.5-turbo`

### 2. Configuration
**File: `backend/config.py`**
- Changed `openai_api_key` to `openrouter_api_key`

**File: `backend/.env.example`**
- Updated to reference OpenRouter API key
- Added link to get API key: https://openrouter.ai/keys

### 3. Dependencies
**File: `backend/requirements.txt`**
- Removed `openai==1.3.0` package (no longer needed)
- Kept `requests==2.31.0` (already present)

### 4. Documentation
Updated all documentation files:
- `README.md` - Main documentation
- `QUICKSTART.md` - Quick start guide
- `backend/README.md` - Backend setup
- `NOTES.md` - Development notes
- `setup.bat` - Setup script

### 5. New Files
- `OPENROUTER_INFO.md` - Comprehensive OpenRouter guide
- `MIGRATION_TO_OPENROUTER.md` - This file

## What You Need to Do

### 1. Get OpenRouter API Key
1. Visit https://openrouter.ai/
2. Sign up for a free account
3. Go to https://openrouter.ai/keys
4. Create a new API key
5. Copy the key (format: `sk-or-v1-...`)

### 2. Update Environment File
Edit `backend/.env` and add:
```
OPENROUTER_API_KEY=sk-or-v1-your-actual-key-here
```

### 3. Reinstall Dependencies (if needed)
```bash
cd backend
pip install -r requirements.txt
```

### 4. Restart Backend
```bash
python main.py
```

## Benefits of OpenRouter

✅ **Multiple Models**: Access GPT-3.5, GPT-4, Claude, Llama, and more  
✅ **Cost-Effective**: Choose cheaper models for simple tasks  
✅ **Reliable**: Automatic fallback if one model fails  
✅ **Flexible**: Switch models without code changes  
✅ **No Vendor Lock-in**: Not tied to a single provider  

## Current Model

The application currently uses:
```
openai/gpt-3.5-turbo
```

This is the same model as before, but accessed through OpenRouter.

## Switching Models

To use a different model (e.g., Claude-3-haiku):

1. Edit `backend/services/openai_service.py`
2. Find line 51 and 115 (in both functions)
3. Change:
   ```python
   "model": "openai/gpt-3.5-turbo",
   ```
   to:
   ```python
   "model": "anthropic/claude-3-haiku",
   ```
4. Restart backend

### Recommended Models

| Model | Use Case | Cost |
|-------|----------|------|
| `openai/gpt-3.5-turbo` | Balanced (current) | Low |
| `anthropic/claude-3-haiku` | Fast & cheap | Very Low |
| `anthropic/claude-3-sonnet` | Better accuracy | Medium |
| `openai/gpt-4` | Best accuracy | High |

## Pricing Comparison

For component classification (~50-100 tokens per request):

| Model | Cost per Classification |
|-------|------------------------|
| GPT-3.5-turbo | ~$0.00005 |
| Claude-3-haiku | ~$0.00001 |
| GPT-4 | ~$0.003 |

## Testing

After migration, test with a sample part number:
```
GCM1885C1H180JA16D
```

Expected behavior:
1. Classification should work exactly as before
2. Response time: 1-3 seconds
3. Component type: "capacitor"

## Troubleshooting

### Error: "Invalid API key"
- Check `.env` file exists in `backend/` folder
- Verify key format: `sk-or-v1-...`
- Ensure no extra spaces or quotes

### Error: "Model not found"
- Check model name spelling in `openai_service.py`
- Verify model is available: https://openrouter.ai/models

### Error: "Rate limit exceeded"
- Free tier: 60 requests/minute
- Wait a minute or upgrade account

## Rollback (if needed)

If you need to revert to direct OpenAI:

1. Edit `requirements.txt`, add: `openai==1.3.0`
2. Run: `pip install openai`
3. Restore original `openai_service.py` from git history
4. Change `.env` to use `OPENAI_API_KEY`

## Support

- OpenRouter Docs: https://openrouter.ai/docs
- OpenRouter Discord: https://discord.gg/openrouter
- IntelliDraft Issues: Check project documentation

## Summary

✅ Migration complete  
✅ All code updated  
✅ All documentation updated  
✅ Ready to use with OpenRouter API  

**Next Step**: Get your OpenRouter API key and add it to `backend/.env`
