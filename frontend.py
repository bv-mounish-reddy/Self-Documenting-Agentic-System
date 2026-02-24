"""
Streamlit frontend for the Self-Documentation Agent System.
Provides an interactive UI for code analysis and documentation.
"""

import streamlit as st
import requests
import json
from datetime import datetime

# Page configuration
st.set_page_config(
    page_title="Code Documentation Agent",
    page_icon="📚",
    layout="wide"
)

# Styling
st.markdown("""
    <style>
    .stCodeBlock { background-color: #f0f0f0; }
    .success-box { background-color: #d4edda; padding: 1rem; border-radius: 0.5rem; }
    .error-box { background-color: #f8d7da; padding: 1rem; border-radius: 0.5rem; }
    </style>
    """, unsafe_allow_html=True)

# Header
st.title("📚 Code Documentation Agent")
st.markdown("Analyze and document Python code with AI-powered analysis")

# Configuration
API_BASE_URL = "http://localhost:8000"

# Sidebar
with st.sidebar:
    st.header("Configuration")
    api_url = st.text_input("API Base URL", value=API_BASE_URL)
    st.markdown("---")
    st.markdown("### How to use:")
    st.markdown("""
    1. Paste your Python code in the editor
    2. Click "Analyze Code" button
    3. View documented code and analysis results
    4. Download results if needed
    """)

# Main content
col1, col2 = st.columns(2)

with col1:
    st.subheader("Input Code")
    code_input = st.text_area(
        "Enter your Python code here:",
        height=400,
        placeholder="# Paste your Python code here...\ndef hello():\n    pass"
    )

with col2:
    st.subheader("Results")
    result_placeholder = st.empty()

# Analysis button
if st.button("Analyze Code", key="analyze_btn", type="primary"):
    if not code_input.strip():
        st.error("Please enter some code to analyze.")
    else:
        # Show loading state
        with st.spinner("Analyzing code..."):
            try:
                # Call FastAPI backend
                response = requests.post(
                    f"{api_url}/analyze",
                    json={"code": code_input},
                    timeout=60
                )
                
                if response.status_code == 200:
                    result = response.json()
                    
                    with result_placeholder.container():
                        st.markdown("### Analysis Complete ✓")
                        
                        # Display results in tabs
                        tab1, tab2, tab3, tab4 = st.tabs([
                            "Documented Code",
                            "Analysis",
                            "Libraries",
                            "Issues"
                        ])
                        
                        with tab1:
                            st.code(result.get("documented_code", "No code generated"), language="python")
                        
                        with tab2:
                            st.markdown(result.get("analysis", "No analysis available"))
                        
                        with tab3:
                            libraries = result.get("libraries", [])
                            if libraries:
                                st.write("**Detected Libraries:**")
                                for lib in libraries:
                                    st.markdown(f"- `{lib}`")
                            else:
                                st.info("No external libraries detected.")
                        
                        with tab4:
                            issues = result.get("issues", [])
                            if issues:
                                st.write("**Issues Found:**")
                                for issue in issues:
                                    st.warning(issue)
                            else:
                                st.success("No issues detected.")
                        
                        # Download options
                        st.markdown("---")
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            st.download_button(
                                label="Download Documented Code",
                                data=result.get("documented_code", ""),
                                file_name=f"documented_code_{datetime.now().strftime('%Y%m%d_%H%M%S')}.py",
                                mime="text/plain"
                            )
                        
                        with col2:
                            analysis_text = f"Analysis Results\n{result.get('analysis', '')}"
                            st.download_button(
                                label="Download Analysis",
                                data=analysis_text,
                                file_name=f"analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                                mime="text/plain"
                            )
                else:
                    st.error(f"API Error: {response.status_code}")
                    st.error(response.json())
            
            except requests.exceptions.ConnectionError:
                st.error(f"Cannot connect to API at {api_url}")
                st.info("Make sure the FastAPI backend is running: `python backend.py`")
            except Exception as e:
                st.error(f"Error: {str(e)}")

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; padding: 2rem;'>
    <p>Self-Documentation Agent System | Built with FastAPI & Streamlit</p>
</div>
""", unsafe_allow_html=True)
