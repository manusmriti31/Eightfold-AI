"""Custom CSS styles for Streamlit app."""

import streamlit as st


def apply_custom_styles():
    """Apply custom CSS styles to the Streamlit app."""
    st.markdown("""
    <style>
    /* Main container */
    .main {
        padding: 2rem;
    }
    
    /* Headers */
    h1 {
        color: #1f77b4;
        font-weight: 600;
        margin-bottom: 1rem;
    }
    
    h2 {
        color: #2c3e50;
        font-weight: 500;
        margin-top: 2rem;
        margin-bottom: 1rem;
    }
    
    h3 {
        color: #34495e;
        font-weight: 500;
        margin-top: 1.5rem;
        margin-bottom: 0.5rem;
    }
    
    /* Buttons */
    .stButton > button {
        border-radius: 8px;
        font-weight: 500;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
    }
    
    /* Progress bars */
    .stProgress > div > div {
        background-color: #1f77b4;
    }
    
    /* Metrics */
    [data-testid="stMetricValue"] {
        font-size: 2rem;
        font-weight: 600;
    }
    
    /* Info boxes */
    .stAlert {
        border-radius: 8px;
        padding: 1rem;
    }
    
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    
    .stTabs [data-baseweb="tab"] {
        border-radius: 8px 8px 0 0;
        padding: 0.5rem 1rem;
    }
    
    /* Expanders */
    .streamlit-expanderHeader {
        font-weight: 500;
        border-radius: 8px;
    }
    
    /* Forms */
    .stTextInput > div > div > input {
        border-radius: 8px;
    }
    
    .stSelectbox > div > div > select {
        border-radius: 8px;
    }
    
    /* Sidebar */
    [data-testid="stSidebar"] {
        background-color: #1a1a1a;
    }
    
    [data-testid="stSidebar"] .stMarkdown {
        padding: 0.5rem 0;
        color: #e0e0e0;
    }
    
    [data-testid="stSidebar"] h1,
    [data-testid="stSidebar"] h2,
    [data-testid="stSidebar"] h3 {
        color: #ffffff !important;
    }
    
    [data-testid="stSidebar"] .stMarkdown a {
        color: #1f77b4;
    }
    
    /* Download buttons */
    .stDownloadButton > button {
        border-radius: 8px;
        width: 100%;
    }
    
    /* Code blocks */
    .stCodeBlock {
        border-radius: 8px;
    }
    
    /* Containers */
    .element-container {
        margin-bottom: 1rem;
    }
    
    /* Custom spacing */
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }
    </style>
    """, unsafe_allow_html=True)
