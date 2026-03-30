# Self-Documentation Agent System

LangGraph workflow that analyzes, documents, and validates Python code using a three-node architecture.

## Features

- Three-Node Workflow: Research → Document → Analyze
- Intelligent Documentation Detection
- Comprehensive Code Documentation with docstrings and comments
- Automated Code Testing and Analysis
- Workflow Visualization (PNG/Mermaid)
- Output to `tests/generated_code.py` and `tests/analysis.txt`

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
# Copy .env.example to .env and add your API keys
cp .env.example .env
# Edit .env with your credentials
```

## Configuration

API keys required:
- **Google API Key**: For Gemini model access
- **Tavily API Key**: For web search functionality

## Usage

### Run Main Workflow

```bash
python main.py
```

This generates `tests/generated_code.py` and `tests/analysis.txt`.

### Run Web Interface (Optional)

1. Start the backend:
```bash
python src/backend.py
```

2. Start the frontend (new terminal):
```bash
source venv/bin/activate
streamlit run src/frontend.py
```

API endpoint: `POST /analyze` with `{ "code": "<python code>" }`

## Project Structure

```
├── main.py              # Main application script
├── code.py              # Generated documented code (output)
├── analysis.txt         # Generated analysis results (output)
├── prompts.yaml         # Node prompts configuration
├── requirements.txt     # Python dependencies
├── .env                 # Environment variables
└── README.md            # This workflow script (run this)
├── src/
│   ├── backend.py       # FastAPI backend
│   └── frontend.py      # Streamlit UI
├── tests/
│   ├── sample_code.py   # Sample code for testing
│   ├── generated_code.py # Output (generated at runtime)
│   └── analysis.txt    # Output (generated at runtime)
├── .env.example         # Environment variables template
├── requirements.txt     # Python dependencies
└── prompts.yaml         # Workflow promptsding libraries, issues, test results, and guidelines
Generated in `tests/` directory:
- **generated_code.py**: Documented source code with docstrings and comments
- **analysis.txt**: Analysis results with libraries, issues, and recommendation

- API Key Errors: Verify credentials in `.env` file
- Import Errors: Ensure all dependencies are installed in virtual environment
- Empty Output: Confirm workflow completed successfully
