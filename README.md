# Self-Documentation Agent System

LangGraph workflow that analyzes, documents, and validates Python code using a three-node architecture.

## Features

- Three-Node Workflow: Research → Document → Analyze
- Intelligent Documentation Detection
- Comprehensive Code Documentation with docstrings and comments
- Automated Code Testing and Analysis
- Workflow Visualization (PNG/Mermaid)
- Output to `code.py` and `analysis.txt`

## Installation

### Prerequisites

- Python 3.8+
- Virtual environment (recommended)

### Setup

```bash
# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure environment variables
# Create .env file with your API keys:
# GOOGLE_API_KEY=your_key
# TAVILY_API_KEY=your_key
```

## Configuration

API keys required:
- **Google API Key**: For Gemini model access
- **Tavily API Key**: For web search functionality

## Usage

Run the FastAPI backend and Streamlit UI to use the system interactively.

1. Activate the virtual environment

```bash
source venv/bin/activate
```

2. Start the backend (foreground)

```bash
python backend.py
# or with uvicorn: uvicorn backend:app --reload --host 127.0.0.1 --port 8000
```

3. Start the frontend (new terminal)

```bash
source venv/bin/activate
streamlit run frontend.py
```

Endpoints:

- Health check: `GET /health`
- Analyze: `POST /analyze` with JSON `{ "code": "<python code>" }`

Add your API keys to the `.env` file before running the backend if required. The original `main.py` workflow is used by the backend and was not modified.

## Project Structure

```
├── main.py              # Main application script
├── code.py              # Generated documented code (output)
├── analysis.txt         # Generated analysis results (output)
├── prompts.yaml         # Node prompts configuration
├── requirements.txt     # Python dependencies
├── .env                 # Environment variables
└── README.md            # This documentation
```

## Output Files

- **code.py**: Original code enhanced with docstrings, inline comments, and warnings
- **analysis.txt**: Structured analysis including libraries, issues, test results, and guidelines

## Troubleshooting

- API Key Errors: Verify credentials in `.env` file
- Import Errors: Ensure all dependencies are installed in virtual environment
- Empty Output: Confirm workflow completed successfully
