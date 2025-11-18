# Development Notes

## IDE Warnings (Can be Ignored)

### TailwindCSS @tailwind Directives
The CSS linter shows warnings for `@tailwind` directives in `frontend/src/index.css`:
```
Unknown at rule @tailwind
```

**This is expected and safe to ignore.** These are TailwindCSS directives that get processed during build time by PostCSS. The warnings appear because the IDE's CSS linter doesn't recognize TailwindCSS syntax, but the application will work correctly.

The directives are:
```css
@tailwind base;
@tailwind components;
@tailwind utilities;
```

These are standard TailwindCSS imports and are required for the styling to work.

---

## Important Configuration Steps

### 1. OpenRouter API Key
Before running the backend, you MUST:
1. Get an API key from https://openrouter.ai/keys
2. Copy `backend/.env.example` to `backend/.env`
3. Add your key: `OPENROUTER_API_KEY=sk-or-v1-your-key-here`

OpenRouter provides access to multiple AI models (GPT-3.5, GPT-4, Claude, etc.) through a single API.

### 2. Digi-Key API
Credentials are already configured in `Library/digikey.py`:
- Client ID: `0dhv3AZgnR9XJnjvVs8RMwI5c2aWbUNA`
- Client Secret: `bKXnVOBACsXedDa5`

If these credentials expire, update them in the file or move them to `.env`.

---

## Template Requirements

Your .docx template MUST have:
- A section starting with "2" or "2." 
- Followed by "Functional Description" (case-insensitive)
- Example: "2. Functional Description" or "2 FUNCTIONAL DESCRIPTION"

The application will:
1. Find this section
2. Clear existing content
3. Insert a professional parameter table
4. Keep all other sections unchanged

---

## File Paths

### Backend
- **Uploads**: `backend/uploads/` - Stores uploaded templates
- **Outputs**: `backend/outputs/` - Generated documents saved here
- **Library**: `Library/` - Shared resources (digikey.py, parameters.json)

### Frontend
- **Build Output**: `frontend/dist/` - Production build (after `npm run build`)

---

## Port Configuration

- **Backend**: Port 8000 (configurable in `backend/main.py`)
- **Frontend Dev**: Port 3000 (configurable in `frontend/vite.config.js`)

If ports are in use, you can change them:

**Backend** (`main.py`):
```python
uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
```

**Frontend** (`vite.config.js`):
```javascript
server: {
  port: 3000,
  ...
}
```

---

## Adding New Component Types

Edit `Library/parameters.json`:

```json
{
  "new_component_type": {
    "description": "Brief description of the component",
    "key_parameters": [
      "parameter_name_1",
      "parameter_name_2",
      "parameter_name_3"
    ]
  }
}
```

The parameter names should match (or be similar to) the parameter names returned by Digi-Key API. The system uses fuzzy matching to map them.

---

## Troubleshooting

### Backend Issues

**"Module not found" errors**
```bash
cd backend
pip install -r requirements.txt
```

**"OpenRouter API key not found"**
- Check `backend/.env` exists
- Verify `OPENROUTER_API_KEY=sk-or-v1-...` is set
- Restart backend server

**"Template section not found"**
- Ensure template has "2. Functional Description" section
- Check section numbering and text exactly

### Frontend Issues

**"Cannot find module" errors**
```bash
cd frontend
rm -rf node_modules
npm install
```

**"Port 3000 already in use"**
- Change port in `vite.config.js`
- Or kill process using port 3000

**API calls failing**
- Ensure backend is running on port 8000
- Check browser console for CORS errors
- Verify proxy settings in `vite.config.js`

---

## Development Tips

### Hot Reload
Both backend and frontend support hot reload:
- **Backend**: Changes to Python files auto-reload (uvicorn --reload)
- **Frontend**: Changes to React files auto-refresh (Vite HMR)

### API Testing
Use the interactive API docs at http://localhost:8000/docs to test endpoints directly.

### Debugging
- **Backend**: Add `print()` statements or use Python debugger
- **Frontend**: Use browser DevTools console and React DevTools extension

---

## Production Deployment

### Backend
```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --host 0.0.0.0 --port 8000
```

### Frontend
```bash
cd frontend
npm run build
# Serve the 'dist' folder with any static file server
```

---

## Security Notes

1. **Never commit `.env` file** - It's in `.gitignore`
2. **API Keys**: Keep OpenRouter and Digi-Key keys secure
3. **File Uploads**: Only .docx files are accepted
4. **CORS**: Currently allows localhost - restrict in production

---

## Performance Considerations

- **OpenRouter API**: ~1-3 seconds per classification (varies by model)
- **Digi-Key API**: ~2-5 seconds per part lookup
- **Document Generation**: <1 second for typical documents
- **Total Time**: ~5-10 seconds per component

For batch processing (Phase 2), consider:
- Rate limiting for APIs
- Background job queue
- Progress tracking
- Caching results

---

## Known Limitations (Phase 1)

1. **Single component only** - Batch processing in Phase 2
2. **Template format** - Only .docx supported (not .doc, .pdf, etc.)
3. **Section 2 only** - Only updates Functional Description
4. **No authentication** - Anyone with access can use the app
5. **No history** - Previous generations not saved/tracked
6. **Basic error handling** - Some edge cases may not be covered

---

## Next Steps for Phase 2

1. Implement batch processing with CSV upload
2. Add user authentication and sessions
3. Create processing history/logs
4. Support multiple document formats
5. Add custom parameter mapping UI
6. Implement template library
7. Add advanced search and filters
8. Export to PDF, HTML, etc.

---

## Contact & Support

For issues or questions:
1. Check this NOTES.md file
2. Review README.md and QUICKSTART.md
3. Check API docs at http://localhost:8000/docs
4. Review error messages in browser console and backend logs

---

Last Updated: Phase 1 Complete
