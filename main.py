"""
Simplified Self-Documenting Code Analysis System

A streamlined LangGraph workflow with three nodes:
1. Research - Understand code and check documentation
2. Document - Add simple documentation
3. Analyze - Run tests and capture issues/results
"""

import os
import yaml
import getpass
import ast
import datetime
from typing import TypedDict, List, Dict, Any
from dotenv import load_dotenv

from langgraph.graph import StateGraph, END
from langgraph.prebuilt import create_react_agent
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain.tools import tool
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import HumanMessage
from langchain_experimental.tools import PythonREPLTool

# Load environment variables
load_dotenv()

# Environment Setup
def setup_environment():
    """Set up API keys for the agents"""
    if "GOOGLE_API_KEY" not in os.environ:
        os.environ["GOOGLE_API_KEY"] = getpass.getpass("Enter your Google API Key: ")
    if "TAVILY_API_KEY" not in os.environ:
        os.environ["TAVILY_API_KEY"] = getpass.getpass("Enter your Tavily API Key: ")

# Simplified State Definition
class CodeState(TypedDict):
    """Simplified state for the workflow"""
    original_code: str
    documented_code: str
    has_documentation: bool
    libraries_used: List[str]
    test_results: List[str]
    issues_found: List[str]
    current_step: str

# Tools Definition
@tool
def search_library_info(library_name: str) -> str:
    """Search for library documentation and usage examples"""
    search_tool = TavilySearchResults(max_results=2)
    query = f"{library_name} python library documentation examples"
    results = search_tool.invoke(query)

    formatted_results = []
    for result in results:
        content = result.get('content', 'No content')[:200]
        formatted_results.append(f"Source: {result.get('url', 'N/A')}\nContent: {content}...")

    return "\n---\n".join(formatted_results)

@tool
def execute_code(code: str) -> str:
    """Execute Python code and return results"""
    python_tool = PythonREPLTool()
    try:
        result = python_tool.invoke(code)
        return f"Execution successful:\n{result}"
    except Exception as e:
        return f"Execution failed:\n{str(e)}"

# Prompts
RESEARCH_PROMPT = """
You are a Code Research Specialist. Analyze the provided Python code and:

1. Check if the code already has documentation (docstrings, comments)
2. Identify all imported libraries and understand their purpose
3. Understand what the code does and what kind of tests would be appropriate
4. Research any unfamiliar libraries using the search tool

Be thorough but concise in your analysis.
"""

DOCUMENT_PROMPT = """
You are a Documentation Generator. Add simple, clear documentation to the code:

1. Add docstrings to functions and classes (keep them concise)
2. Add brief comments for complex logic
3. Maintain original code functionality
4. Use simple, readable formatting

Return ONLY the documented code, no explanations.
"""

ANALYZE_PROMPT = """
You are a Code Analyzer and Tester. Your tasks:

1. Execute the code to test its functionality
2. Try different test scenarios and inputs
3. Identify any issues, errors, or potential problems
4. Document the input/output behavior

Use the code execution tool to run tests and capture results.
"""
# Initialize Model
def create_model():
    """Create the language model"""
    return ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        temperature=0.3,
        google_api_key=os.environ["GOOGLE_API_KEY"]
    )

# Workflow Nodes
def research_node(state: CodeState) -> CodeState:
    """
    Research node: Understand code and check documentation
    Uses agent with search tool for library research
    """
    print("RESEARCH: Analyzing code structure and documentation...")

    model = create_model()
    research_agent = create_react_agent(
        model=model,
        tools=[search_library_info],
        prompt=ChatPromptTemplate.from_messages([
            ("system", RESEARCH_PROMPT),
            ("placeholder", "{messages}")
        ])
    )

    # Analyze the code
    analysis_input = {
        "messages": [HumanMessage(content=f"Analyze this Python code:\n\n{state['original_code']}")]
    }

    result = research_agent.invoke(analysis_input)
    response_text = result["messages"][-1].content

    # Extract libraries using AST
    libraries = []
    try:
        tree = ast.parse(state['original_code'])
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    libraries.append(alias.name)
            elif isinstance(node, ast.ImportFrom):
                module = node.module or ""
                for alias in node.names:
                    libraries.append(f"{module}.{alias.name}")
    except:
        pass

    # Check if code has documentation
    has_docs = ('"""' in state['original_code'] or
                "'''" in state['original_code'] or
                '#' in state['original_code'])

    print(f"  - Libraries found: {libraries}")
    print(f"  - Documentation present: {has_docs}")

    return {
        **state,
        "libraries_used": libraries,
        "has_documentation": has_docs,
        "current_step": "researched"
    }

def document_node(state: CodeState) -> CodeState:
    """
    Document node: Add simple documentation to code
    Uses model with documentation prompt (no tools needed)
    """
    print("DOCUMENT: Adding documentation and comments...")

    model = create_model()

    # Create documentation prompt
    doc_input = {
        "messages": [HumanMessage(content=f"""
        {DOCUMENT_PROMPT}

        Code to document:
        {state['original_code']}

        Libraries used: {', '.join(state['libraries_used'])}

        Please add comprehensive documentation including:
        - Detailed docstrings for all functions and classes
        - Inline comments explaining complex logic
        - Comments for important variables and calculations
        - Warning comments for potential issues
        """)]
    }

    result = model.invoke(doc_input["messages"])
    documented_code = result.content

    # Clean up the response to extract just the code
    if "```python" in documented_code:
        documented_code = documented_code.split("```python")[1].split("```")[0].strip()
    elif "```" in documented_code:
        documented_code = documented_code.split("```")[1].split("```")[0].strip()

    print("  - Documentation completed")

    return {
        **state,
        "documented_code": documented_code,
        "current_step": "documented"
    }

def analyze_node(state: CodeState) -> CodeState:
    """
    Analyze node: Run tests and capture issues/results
    Uses model with code execution tool
    """
    print("ANALYZE: Testing code and identifying issues...")

    model = create_model()

    # Use the code to analyze (documented if available, otherwise original)
    code_to_analyze = state.get('documented_code') or state['original_code']

    # Create analyzer with code execution tool
    analyzer_agent = create_react_agent(
        model=model,
        tools=[execute_code],
        prompt=ChatPromptTemplate.from_messages([
            ("system", ANALYZE_PROMPT),
            ("placeholder", "{messages}")
        ])
    )

    # Analyze and test the code
    analysis_input = {
        "messages": [HumanMessage(content=f"""
        Analyze and test this Python code:

        {code_to_analyze}

        Execute the code and try different test scenarios. Document any issues and the input/output behavior.
        """)]
    }

    result = analyzer_agent.invoke(analysis_input)
    response_text = result["messages"][-1].content

    # Extract test results and issues
    test_results = []
    issues = []

    # Better parsing of the response
    if isinstance(response_text, str):
        # Use the full response as a single test result for better readability
        test_results.append(response_text)

        # Extract specific issues from the response
        lines = response_text.split('\n')
        for line in lines:
            line = line.strip()
            if any(keyword in line.lower() for keyword in ['error', 'issue', 'problem', 'fail', 'exception', 'warning']):
                if line and len(line) > 10:  # Avoid very short lines
                    issues.append(line)
    else:
        test_results.append(str(response_text))

    # Fallback if no results captured
    if not test_results:
        test_results.append("Analysis completed but no detailed results captured")

    if not issues:
        issues.append("No critical issues identified during analysis")

    print(f"  - Issues found: {len(issues)}")
    print(f"  - Test results captured: {len(test_results)}")

    return {
        **state,
        "test_results": test_results,
        "issues_found": issues,
        "current_step": "analyzed"
    }

# Conditional edge function
def should_skip_documentation(state: CodeState) -> str:
    """Decide whether to skip documentation based on existing docs"""
    if state["has_documentation"]:
        print("  - Code already documented, proceeding to analysis")
        # Set documented_code to original_code since we're skipping documentation
        state["documented_code"] = state["original_code"]
        return "analyze"
    else:
        print("  - Code requires documentation")
        return "document"

# File saving functions
def save_documented_code(documented_code: str):
    """Save documented code to code.py"""
    try:
        with open("code.py", "w", encoding="utf-8") as f:
            f.write(documented_code)
        print("  - Documented code saved to code.py")
    except Exception as e:
        print(f"  - Error saving code.py: {e}")

def save_analysis_results(state: CodeState):
    """Save analysis results to analysis.txt"""
    try:
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        with open("analysis.txt", "w", encoding="utf-8") as f:
            f.write(f"# Code Analysis Results\n")
            f.write(f"Generated on: {timestamp}\n\n")

            f.write("## Libraries Used\n")
            if state['libraries_used']:
                for lib in state['libraries_used']:
                    f.write(f"- {lib}\n")
            else:
                f.write("- No libraries identified\n")
            f.write("\n")

            f.write("## Issues and Recommendations\n")
            if state['issues_found']:
                for i, issue in enumerate(state['issues_found'], 1):
                    f.write(f"{i}. {issue}\n")
            else:
                f.write("- No critical issues identified\n")
            f.write("\n")

            f.write("## Test Results and I/O Behavior\n")
            if state['test_results']:
                for i, result in enumerate(state['test_results'], 1):
                    f.write(f"### Test {i}\n{result}\n\n")
            else:
                f.write("- No test results captured\n")
            f.write("\n")

            f.write("## Usage Guidelines\n")
            f.write("1. Review the documented code in code.py\n")
            f.write("2. Address any issues or recommendations listed above\n")
            f.write("3. Test the code with various input scenarios\n")
            f.write("4. Validate functionality before production use\n")

        print("  - Analysis results saved to analysis.txt")
    except Exception as e:
        print(f"  - Error saving analysis.txt: {e}")

def final_node(state: CodeState) -> CodeState:
    """Final node: Save results to files"""
    print("FINALIZE: Saving results to files...")

    # Use documented code if available, otherwise original code
    code_to_save = state.get('documented_code') or state['original_code']

    # Save documented code
    save_documented_code(code_to_save)

    # Save analysis results
    save_analysis_results(state)

    print("Workflow completed successfully")

    return {
        **state,
        "current_step": "completed"
    }

# Workflow Creation
def create_workflow():
    """Create and configure the simplified workflow"""
    workflow = StateGraph(CodeState)

    # Add nodes
    workflow.add_node("research", research_node)
    workflow.add_node("document", document_node)
    workflow.add_node("analyze", analyze_node)
    workflow.add_node("final", final_node)

    # Set entry point
    workflow.set_entry_point("research")

    # Add conditional edge from research
    workflow.add_conditional_edges(
        "research",
        should_skip_documentation,
        {
            "document": "document",
            "analyze": "analyze"
        }
    )

    # Add regular edges
    workflow.add_edge("document", "analyze")
    workflow.add_edge("analyze", "final")
    workflow.add_edge("final", END)

    # Compile workflow
    compiled_workflow = workflow.compile()

    # Generate workflow diagram
    try:
        graph_png = compiled_workflow.get_graph().draw_mermaid_png()
        with open("workflow_diagram.png", "wb") as f:
            f.write(graph_png)
        print("Workflow diagram saved as workflow_diagram.png")
    except Exception as e:
        print(f"Could not save workflow diagram: {e}")
        try:
            mermaid_text = compiled_workflow.get_graph().draw_mermaid()
            with open("workflow_diagram.mmd", "w") as f:
                f.write(mermaid_text)
            print("Workflow diagram saved as workflow_diagram.mmd")
        except Exception as e2:
            print(f"Workflow visualization failed: {e2}")

    return compiled_workflow

def run_documentation_workflow(code_input: str) -> Dict:
    """
    Run the simplified documentation workflow

    Args:
        code_input: Python code to analyze and document

    Returns:
        Dictionary containing all results from the workflow
    """
    # Set up environment
    setup_environment()

    # Create and run workflow
    app = create_workflow()

    # Initialize state
    initial_state = {
        "original_code": code_input,
        "documented_code": "",
        "has_documentation": False,
        "libraries_used": [],
        "test_results": [],
        "issues_found": [],
        "current_step": "start"
    }

    print("Starting Documentation Workflow")
    print("=" * 50)

    # Stream the workflow execution
    final_result = None
    for step in app.stream(initial_state):
        step_name = list(step.keys())[0]
        step_data = step[step_name]

        print(f"\nStep: {step_name.upper()}")
        print("-" * 30)

        final_result = step_data

    # Display final results
    print("\n" + "=" * 50)
    print("WORKFLOW SUMMARY")
    print("=" * 50)
    print(f"Status: {final_result['current_step']}")
    print(f"Libraries: {len(final_result['libraries_used'])}")
    print(f"Issues: {len(final_result['issues_found'])}")
    print(f"Tests: {len(final_result['test_results'])}")

    return final_result

# Example Usage
if __name__ == "__main__":
    # Sample code to test the workflow (with potential issues)
    sample_code = """
import math
import random

def calculate_area(shape, **kwargs):
    if shape == "circle":
        return math.pi * kwargs["radius"] ** 2
    elif shape == "rectangle":
        return kwargs["width"] * kwargs["height"]
    else:
        return 0

def divide_numbers(a, b):
    return a / b

def process_list(items):
    total = 0
    for i in range(len(items)):
        total += items[i] * 2
    return total

class Calculator:
    def __init__(self):
        self.history = []

    def add(self, a, b):
        result = a + b
        self.history.append(f"{a} + {b} = {result}")
        return result

    def divide(self, a, b):
        return divide_numbers(a, b)

calc = Calculator()
result = calc.add(5, 3)
area = calculate_area("circle", radius=5)
division = calc.divide(10, 2)
items = [1, 2, 3, 4]
processed = process_list(items)
print(f"Results: {result}, {area:.2f}, {division}, {processed}")
"""

    print("Running Simplified Documentation Workflow")
    print("=" * 50)

    # Run the workflow
    result = run_documentation_workflow(sample_code)

    print("\nWorkflow completed successfully!")
    print("Output files:")
    print("  - code.py: Documented code")
    print("  - analysis.txt: Analysis results")

