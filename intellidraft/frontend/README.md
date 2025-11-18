# IntelliDraft Frontend

React frontend for IntelliDraft component documentation system.

## Setup

1. **Install dependencies**:
   ```bash
   npm install
   ```

2. **Run development server**:
   ```bash
   npm run dev
   ```

3. **Access the application**:
   - Frontend: http://localhost:3000
   - Make sure backend is running on http://localhost:8000

## Build for Production

```bash
npm run build
```

The built files will be in the `dist` directory.

## Technology Stack

- **React 18** - UI framework
- **Vite** - Build tool and dev server
- **TailwindCSS** - Styling
- **Lucide React** - Icons
- **Axios** - HTTP client

## Features (Phase 1)

### Single Component Processing
1. Upload template .docx file
2. Enter component part number
3. AI classification using OpenAI
4. Automatic parameter extraction from Digi-Key
5. Editable parameter table
6. Generate document with updated Functional Description section

### Batch Processing
Coming in Phase 2

## Project Structure

```
frontend/
├── src/
│   ├── components/
│   │   ├── TemplateUpload.jsx    # Template file upload
│   │   ├── SingleComponent.jsx   # Single component processing
│   │   ├── ParameterTable.jsx    # Editable parameters table
│   │   └── BatchProcessing.jsx   # Batch processing (Phase 2)
│   ├── services/
│   │   └── api.js                # API client
│   ├── App.jsx                   # Main app component
│   ├── main.jsx                  # Entry point
│   └── index.css                 # Global styles
├── index.html
├── package.json
└── vite.config.js
```
