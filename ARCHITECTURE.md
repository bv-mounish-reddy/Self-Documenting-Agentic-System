# System Architecture & Setup Guide

## Overview

The Self-Documentation Agent System now has a three-layer architecture:

1. **Core Engine (main.py)**: LangGraph workflow for code analysis and documentation
2. **FastAPI Backend (backend.py)**: REST API exposing the workflow functions
3. **Streamlit Frontend (frontend.py)**: Interactive UI for users to analyze code

## Files Created/Updated

### New Files
- **backend.py**: FastAPI server with `/analyze` endpoint
- **frontend.py**: Streamlit web interface
- **.env**: Environment variables configuration

### Updated Files
- **README.md**: Shortened and made more professional
- **requirements.txt**: Added fastapi, uvicorn, and streamlit

## Architecture Diagram

```
┌─────────────────────┐
│  Streamlit Frontend │  (frontend.py)
│   - Code Editor     │
│   - Result Display  │
└──────────┬──────────┘
           │ HTTP
           ▼
┌─────────────────────┐
│   FastAPI Backend   │  (backend.py)
│   - /analyze        │
│   - /health         │
└──────────┬──────────┘
           │ Import
           ▼
┌─────────────────────┐
│   LangGraph Engine  │  (main.py)
│   - Research Node   │
│   - Document Node   │
│   - Analyze Node    │
└─────────────────────┘
```

## How to Run

### 1. Activate Virtual Environment
```bash
source venv/bin/activate  # macOS/Linux
# or
venv\Scripts\activate  # Windows
```

### 2. Install Dependencies (One-time)
```bash
pip install -r requirements.txt
```

### 3. Configure API Keys
Edit `.env` file with your API keys:
```
GOOGLE_API_KEY=your_google_api_key_here
TAVILY_API_KEY=your_tavily_api_key_here
```

### 4. Start Backend Server
```bash
python backend.py
```
The API will run on http://localhost:8000

### 5. Start Frontend (in a new terminal)
```bash
source venv/bin/activate  # Activate venv in new terminal
streamlit run frontend.py
```
The UI will open on http://localhost:8501

## API Endpoints

### Health Check
```bash
GET /
GET /health
```

### Code Analysis
```bash
POST /analyze
Content-Type: application/json

{
    "code": "def hello():\n    print('Hello')"
}
```

Response:
```json
{
    "status": "success",
    "documented_code": "...",
    "analysis": "...",
    "libraries": ["math", "random"],
    "issues": ["Warning: unused import"]
}
```

## User Workflow

1. Open Streamlit UI (http://localhost:8501)
2. Paste Python code in the editor
3. Click "Analyze Code" button
4. View results in tabs:
   - **Documented Code**: Enhanced code with docstrings and comments
   - **Analysis**: Detailed testing results and recommendations
   - **Libraries**: Detected dependencies
   - **Issues**: Potential problems and warnings
5. Download results as needed

## Next Steps

1. Add your API keys to the `.env` file
2. Activate the virtual environment
3. Start the backend: `python backend.py`
4. In another terminal, start the frontend: `streamlit run frontend.py`
5. Access the UI and start analyzing code

The original code files (code.py, main.py, prompts.yaml) remain unchanged.
