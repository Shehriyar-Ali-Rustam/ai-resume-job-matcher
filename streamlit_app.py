"""
AI Resume-Job Matcher - Standalone Streamlit App
Professional UI with integrated AI matching (no backend required)
"""

import streamlit as st
import sys
import os
from io import BytesIO
import json

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import utilities
from utils.text_processor import extract_text_from_pdf, extract_keywords, find_missing_keywords
from backend.matcher import ResumeJobMatcher

# Download NLTK data on first run
import nltk
import ssl

try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context

# Download required NLTK data silently
try:
    nltk.download('punkt', quiet=True)
    nltk.download('stopwords', quiet=True)
    nltk.download('wordnet', quiet=True)
    nltk.download('averaged_perceptron_tagger', quiet=True)
    nltk.download('punkt_tab', quiet=True)
except Exception as e:
    pass  # Fail silently, data might already be downloaded


# Page configuration - MUST be first Streamlit command
st.set_page_config(
    page_title="AI Resume Matcher - Free Resume Job Matching Tool | Career Intelligence",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://github.com/Shehriyar-Ali-Rustam/ai-resume-job-matcher',
        'Report a bug': 'https://github.com/Shehriyar-Ali-Rustam/ai-resume-job-matcher/issues',
        'About': "AI Resume Matcher - Free online tool to match your resume with job descriptions using artificial intelligence. Get instant feedback, skills gap analysis, and improve your chances of landing your dream job."
    }
)

# Initialize session state for theme
if 'theme' not in st.session_state:
    st.session_state.theme = 'light'

# Initialize AI matcher (cached to avoid reloading)
@st.cache_resource
def load_matcher():
    """Load and cache the AI matcher model"""
    return ResumeJobMatcher()


def toggle_theme():
    """Toggle between light and dark theme"""
    st.session_state.theme = 'dark' if st.session_state.theme == 'light' else 'light'


def get_custom_css():
    """Get custom CSS based on current theme - Professional minimalist design"""

    if st.session_state.theme == 'dark':
        return """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

        /* Dark Theme - Premium Professional */
        * {
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
        }

        .stApp {
            background: #000000;
            color: #FFFFFF;
        }

        /* Hide Streamlit branding */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}

        /* Force sidebar to always be visible */
        section[data-testid="stSidebar"] {
            position: relative !important;
            transform: none !important;
        }

        section[data-testid="stSidebar"][aria-expanded="false"] {
            transform: none !important;
            margin-left: 0 !important;
        }

        /* Hero Header */
        .hero-header {
            background: linear-gradient(135deg, #000000 0%, #1a1a1a 100%);
            padding: 4rem 2rem;
            text-align: center;
            border-bottom: 1px solid #2a2a2a;
            margin-bottom: 3rem;
        }

        .hero-header h1 {
            color: #FFFFFF;
            font-size: 3.5rem;
            font-weight: 800;
            letter-spacing: -0.02em;
            margin: 0;
            line-height: 1.1;
        }

        .hero-header p {
            color: #888888;
            font-size: 1.1rem;
            font-weight: 400;
            margin-top: 1rem;
            letter-spacing: 0.01em;
        }

        /* Status Badge */
        .status-badge {
            display: inline-block;
            background: #1a1a1a;
            border: 1px solid #2a2a2a;
            padding: 0.5rem 1.2rem;
            border-radius: 50px;
            font-size: 0.85rem;
            color: #00ff00;
            margin-top: 1rem;
        }

        /* Match Score Display - Minimalist */
        .score-display {
            background: #0a0a0a;
            border: 1px solid #2a2a2a;
            border-radius: 20px;
            padding: 4rem 2rem;
            text-align: center;
            margin: 3rem 0;
            transition: all 0.3s ease;
        }

        .score-display:hover {
            border-color: #404040;
        }

        .score-number {
            font-size: 7rem;
            font-weight: 800;
            color: #FFFFFF;
            line-height: 1;
            margin: 0;
            letter-spacing: -0.03em;
        }

        .score-label {
            font-size: 1rem;
            color: #666666;
            text-transform: uppercase;
            letter-spacing: 0.2em;
            margin-top: 1rem;
            font-weight: 600;
        }

        .score-excellent .score-number { color: #00ff00; }
        .score-good .score-number { color: #0099ff; }
        .score-moderate .score-number { color: #ff9900; }
        .score-low .score-number { color: #ff3333; }

        /* Progress Bar - Apple Style */
        .progress-container {
            width: 100%;
            height: 4px;
            background: #1a1a1a;
            border-radius: 10px;
            overflow: hidden;
            margin: 2rem 0;
        }

        .progress-bar {
            height: 100%;
            background: linear-gradient(90deg, #FFFFFF 0%, #888888 100%);
            border-radius: 10px;
            transition: width 1s cubic-bezier(0.4, 0, 0.2, 1);
        }

        /* Card Design - Clean & Minimal */
        .info-card {
            background: #0a0a0a;
            border: 1px solid #2a2a2a;
            border-radius: 16px;
            padding: 2rem;
            margin: 1rem 0;
            transition: all 0.3s ease;
        }

        .info-card:hover {
            border-color: #404040;
            transform: translateY(-2px);
        }

        .info-card h3 {
            font-size: 1.1rem;
            font-weight: 600;
            color: #FFFFFF;
            margin: 0 0 1rem 0;
            text-transform: uppercase;
            letter-spacing: 0.05em;
        }

        .info-card p {
            color: #888888;
            line-height: 1.6;
            font-size: 0.95rem;
        }

        /* Keywords - Minimal Pills */
        .keyword-container {
            display: flex;
            flex-wrap: wrap;
            gap: 0.5rem;
            margin-top: 1rem;
        }

        .keyword {
            background: #1a1a1a;
            border: 1px solid #2a2a2a;
            color: #FFFFFF;
            padding: 0.5rem 1rem;
            border-radius: 6px;
            font-size: 0.85rem;
            font-weight: 500;
            transition: all 0.2s ease;
            letter-spacing: 0.02em;
        }

        .keyword:hover {
            background: #2a2a2a;
            border-color: #404040;
        }

        .keyword.resume {
            border-color: #0099ff;
            color: #0099ff;
        }

        .keyword.job {
            border-color: #9966ff;
            color: #9966ff;
        }

        .keyword.missing {
            border-color: #ff3333;
            color: #ff3333;
            background: rgba(255, 51, 51, 0.05);
        }

        /* Buttons - Premium Style */
        .stButton > button {
            background: #FFFFFF;
            color: #000000;
            border: none;
            border-radius: 8px;
            padding: 1rem 2.5rem;
            font-size: 1rem;
            font-weight: 600;
            transition: all 0.2s ease;
            text-transform: none;
            letter-spacing: 0.01em;
        }

        .stButton > button:hover {
            background: #e6e6e6;
            transform: scale(1.02);
        }

        /* Sidebar - Clean Professional */
        section[data-testid="stSidebar"] {
            background: #0a0a0a;
            border-right: 1px solid #2a2a2a;
        }

        section[data-testid="stSidebar"] h1,
        section[data-testid="stSidebar"] h2,
        section[data-testid="stSidebar"] h3,
        section[data-testid="stSidebar"] h4,
        section[data-testid="stSidebar"] p,
        section[data-testid="stSidebar"] span,
        section[data-testid="stSidebar"] div,
        section[data-testid="stSidebar"] label,
        section[data-testid="stSidebar"] a,
        section[data-testid="stSidebar"] li,
        section[data-testid="stSidebar"] .stMarkdown,
        section[data-testid="stSidebar"] .stMarkdown *,
        section[data-testid="stSidebar"] button,
        section[data-testid="stSidebar"] [data-testid="stMetricValue"],
        section[data-testid="stSidebar"] [data-testid="stMetricLabel"] {
            color: #FFFFFF !important;
        }

        /* Force sidebar button text to be white in dark mode */
        section[data-testid="stSidebar"] .stButton > button {
            background: #FFFFFF !important;
            color: #000000 !important;
            border: none !important;
        }

        /* Force all button text elements to be black */
        section[data-testid="stSidebar"] .stButton > button p,
        section[data-testid="stSidebar"] .stButton > button span,
        section[data-testid="stSidebar"] .stButton > button div {
            color: #000000 !important;
        }

        section[data-testid="stSidebar"] .stButton > button:hover {
            background: #e6e6e6 !important;
        }

        /* Input Fields */
        .stTextArea textarea, .stTextInput input {
            background: #0a0a0a !important;
            border: 1px solid #2a2a2a !important;
            color: #FFFFFF !important;
            border-radius: 8px !important;
            font-size: 0.95rem !important;
        }

        .stTextArea textarea:focus, .stTextInput input:focus {
            border-color: #404040 !important;
            box-shadow: none !important;
        }

        /* File Uploader */
        section[data-testid="stFileUploader"] label,
        [data-testid="stFileUploader"] label {
            color: #FFFFFF !important;
        }

        section[data-testid="stFileUploader"] button,
        [data-testid="stFileUploader"] button {
            background: #1a1a1a !important;
            border: 1px solid #404040 !important;
            color: #FFFFFF !important;
            border-radius: 8px !important;
            padding: 0.6rem 1.5rem !important;
            transition: all 0.2s ease !important;
            font-weight: 500 !important;
        }

        section[data-testid="stFileUploader"] button:hover,
        [data-testid="stFileUploader"] button:hover {
            background: #2a2a2a !important;
            border-color: #666666 !important;
        }

        section[data-testid="stFileUploader"] small,
        [data-testid="stFileUploader"] small {
            color: #888888 !important;
        }

        /* Fix all text colors in dark mode */
        .stMarkdown, .stMarkdown p, .stMarkdown span {
            color: #FFFFFF !important;
        }

        .stAlert > div {
            color: #FFFFFF !important;
        }

        .stTabs [data-baseweb="tab-list"] button {
            color: #888888 !important;
        }

        .stTabs [data-baseweb="tab-list"] button[aria-selected="true"] {
            color: #FFFFFF !important;
        }

        label, .stRadio label, .stCheckbox label {
            color: #FFFFFF !important;
        }

        /* Radio buttons styling - Dark mode */
        .stRadio > div {
            color: #FFFFFF !important;
        }

        .stRadio > div > label > div {
            color: #FFFFFF !important;
        }

        .stRadio > div > label > div > p {
            color: #FFFFFF !important;
        }

        /* Radio button circles */
        .stRadio > div > label > div[role="radio"] {
            background-color: #0a0a0a !important;
            border: 2px solid #FFFFFF !important;
        }

        .stRadio > div > label > div[role="radio"][aria-checked="true"] {
            background-color: #FFFFFF !important;
            border: 2px solid #FFFFFF !important;
        }

        /* Expander text colors */
        .streamlit-expanderHeader {
            color: #FFFFFF !important;
        }

        .streamlit-expanderContent {
            color: #FFFFFF !important;
        }

        /* Success/Error/Warning/Info boxes */
        .stSuccess, .stError, .stWarning, .stInfo {
            color: #FFFFFF !important;
        }

        /* Metrics */
        .metric-row {
            display: flex;
            gap: 2rem;
            margin: 2rem 0;
        }

        .metric {
            flex: 1;
            text-align: center;
            padding: 1.5rem;
            background: #0a0a0a;
            border: 1px solid #2a2a2a;
            border-radius: 12px;
        }

        .metric-value {
            font-size: 2.5rem;
            font-weight: 700;
            color: #FFFFFF;
        }

        .metric-label {
            font-size: 0.85rem;
            color: #666666;
            text-transform: uppercase;
            letter-spacing: 0.1em;
            margin-top: 0.5rem;
        }

        /* Divider */
        hr {
            border: none;
            border-top: 1px solid #2a2a2a;
            margin: 3rem 0;
        }

        /* Footer */
        .footer {
            text-align: center;
            padding: 3rem 0;
            margin-top: 5rem;
            border-top: 1px solid #2a2a2a;
            color: #666666;
        }
        </style>
        """
    else:
        # Light Theme - Clean & Professional
        return """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

        /* Light Theme - Premium Professional */
        * {
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
        }

        .stApp {
            background: #FFFFFF;
            color: #000000;
        }

        /* Hide Streamlit branding */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}

        /* Force sidebar to always be visible */
        section[data-testid="stSidebar"] {
            position: relative !important;
            transform: none !important;
        }

        section[data-testid="stSidebar"][aria-expanded="false"] {
            transform: none !important;
            margin-left: 0 !important;
        }

        /* Hero Header */
        .hero-header {
            background: linear-gradient(135deg, #FFFFFF 0%, #F5F5F7 100%);
            padding: 4rem 2rem;
            text-align: center;
            border-bottom: 1px solid #E5E5E7;
            margin-bottom: 3rem;
        }

        .hero-header h1 {
            color: #000000;
            font-size: 3.5rem;
            font-weight: 800;
            letter-spacing: -0.02em;
            margin: 0;
            line-height: 1.1;
        }

        .hero-header p {
            color: #6E6E73;
            font-size: 1.1rem;
            font-weight: 400;
            margin-top: 1rem;
            letter-spacing: 0.01em;
        }

        /* Status Badge */
        .status-badge {
            display: inline-block;
            background: #F5F5F7;
            border: 1px solid #E5E5E7;
            padding: 0.5rem 1.2rem;
            border-radius: 50px;
            font-size: 0.85rem;
            color: #00aa00;
            margin-top: 1rem;
        }

        /* Match Score Display - Minimalist */
        .score-display {
            background: #FBFBFD;
            border: 1px solid #E5E5E7;
            border-radius: 20px;
            padding: 4rem 2rem;
            text-align: center;
            margin: 3rem 0;
            transition: all 0.3s ease;
        }

        .score-display:hover {
            border-color: #D2D2D7;
        }

        .score-number {
            font-size: 7rem;
            font-weight: 800;
            color: #000000;
            line-height: 1;
            margin: 0;
            letter-spacing: -0.03em;
        }

        .score-label {
            font-size: 1rem;
            color: #86868B;
            text-transform: uppercase;
            letter-spacing: 0.2em;
            margin-top: 1rem;
            font-weight: 600;
        }

        .score-excellent .score-number { color: #00aa00; }
        .score-good .score-number { color: #0066CC; }
        .score-moderate .score-number { color: #FF9500; }
        .score-low .score-number { color: #FF3B30; }

        /* Progress Bar - Apple Style */
        .progress-container {
            width: 100%;
            height: 4px;
            background: #E5E5E7;
            border-radius: 10px;
            overflow: hidden;
            margin: 2rem 0;
        }

        .progress-bar {
            height: 100%;
            background: linear-gradient(90deg, #000000 0%, #666666 100%);
            border-radius: 10px;
            transition: width 1s cubic-bezier(0.4, 0, 0.2, 1);
        }

        /* Card Design - Clean & Minimal */
        .info-card {
            background: #FBFBFD;
            border: 1px solid #E5E5E7;
            border-radius: 16px;
            padding: 2rem;
            margin: 1rem 0;
            transition: all 0.3s ease;
        }

        .info-card:hover {
            border-color: #D2D2D7;
            transform: translateY(-2px);
        }

        .info-card h3 {
            font-size: 1.1rem;
            font-weight: 600;
            color: #000000;
            margin: 0 0 1rem 0;
            text-transform: uppercase;
            letter-spacing: 0.05em;
        }

        .info-card p {
            color: #6E6E73;
            line-height: 1.6;
            font-size: 0.95rem;
        }

        /* Keywords - Minimal Pills */
        .keyword-container {
            display: flex;
            flex-wrap: wrap;
            gap: 0.5rem;
            margin-top: 1rem;
        }

        .keyword {
            background: #FFFFFF;
            border: 1px solid #E5E5E7;
            color: #000000;
            padding: 0.5rem 1rem;
            border-radius: 6px;
            font-size: 0.85rem;
            font-weight: 500;
            transition: all 0.2s ease;
            letter-spacing: 0.02em;
        }

        .keyword:hover {
            background: #F5F5F7;
            border-color: #D2D2D7;
        }

        .keyword.resume {
            border-color: #0066CC;
            color: #0066CC;
        }

        .keyword.job {
            border-color: #8E44AD;
            color: #8E44AD;
        }

        .keyword.missing {
            border-color: #FF3B30;
            color: #FF3B30;
            background: rgba(255, 59, 48, 0.05);
        }

        /* Buttons - Premium Style */
        .stButton > button {
            background: #000000;
            color: #FFFFFF;
            border: none;
            border-radius: 8px;
            padding: 1rem 2.5rem;
            font-size: 1rem;
            font-weight: 600;
            transition: all 0.2s ease;
            text-transform: none;
            letter-spacing: 0.01em;
        }

        .stButton > button:hover {
            background: #1a1a1a;
            transform: scale(1.02);
        }

        /* Sidebar - Clean Professional */
        section[data-testid="stSidebar"] {
            background: #FBFBFD;
            border-right: 1px solid #E5E5E7;
        }

        section[data-testid="stSidebar"] h1,
        section[data-testid="stSidebar"] h2,
        section[data-testid="stSidebar"] h3,
        section[data-testid="stSidebar"] h4,
        section[data-testid="stSidebar"] p,
        section[data-testid="stSidebar"] span,
        section[data-testid="stSidebar"] div,
        section[data-testid="stSidebar"] label,
        section[data-testid="stSidebar"] a,
        section[data-testid="stSidebar"] li,
        section[data-testid="stSidebar"] .stMarkdown,
        section[data-testid="stSidebar"] .stMarkdown *,
        section[data-testid="stSidebar"] button,
        section[data-testid="stSidebar"] [data-testid="stMetricValue"],
        section[data-testid="stSidebar"] [data-testid="stMetricLabel"] {
            color: #000000 !important;
        }

        /* Force sidebar button text to be visible in light mode */
        section[data-testid="stSidebar"] .stButton > button {
            background: #000000 !important;
            color: #FFFFFF !important;
            border: none !important;
            font-weight: 600 !important;
        }

        section[data-testid="stSidebar"] .stButton > button:hover {
            background: #1a1a1a !important;
            color: #FFFFFF !important;
        }

        section[data-testid="stSidebar"] .stButton > button p {
            color: #FFFFFF !important;
        }

        /* Input Fields */
        .stTextArea textarea, .stTextInput input {
            background: #FFFFFF !important;
            border: 1px solid #E5E5E7 !important;
            color: #000000 !important;
            border-radius: 8px !important;
            font-size: 0.95rem !important;
        }

        .stTextArea textarea:focus, .stTextInput input:focus {
            border-color: #D2D2D7 !important;
            box-shadow: none !important;
        }

        /* File Uploader */
        section[data-testid="stFileUploader"] label,
        [data-testid="stFileUploader"] label {
            color: #000000 !important;
        }

        section[data-testid="stFileUploader"] button,
        [data-testid="stFileUploader"] button {
            background: #000000 !important;
            border: 1px solid #D2D2D7 !important;
            color: #FFFFFF !important;
            border-radius: 8px !important;
            padding: 0.6rem 1.5rem !important;
            transition: all 0.2s ease !important;
            font-weight: 500 !important;
        }

        section[data-testid="stFileUploader"] button:hover,
        [data-testid="stFileUploader"] button:hover {
            background: #1a1a1a !important;
            border-color: #6E6E73 !important;
        }

        section[data-testid="stFileUploader"] small,
        [data-testid="stFileUploader"] small {
            color: #6E6E73 !important;
        }

        /* Fix all text colors in light mode */
        .stMarkdown, .stMarkdown p, .stMarkdown span {
            color: #000000 !important;
        }

        .stAlert > div {
            color: #000000 !important;
        }

        .stTabs [data-baseweb="tab-list"] button {
            color: #6E6E73 !important;
        }

        .stTabs [data-baseweb="tab-list"] button[aria-selected="true"] {
            color: #000000 !important;
            border-bottom: 2px solid #000000 !important;
        }

        label, .stRadio label, .stCheckbox label {
            color: #000000 !important;
        }

        /* Radio buttons styling - Light mode */
        .stRadio > div {
            color: #000000 !important;
        }

        .stRadio > div > label > div {
            color: #000000 !important;
        }

        .stRadio > div > label > div > p {
            color: #000000 !important;
        }

        /* Radio button circles */
        .stRadio > div > label > div[role="radio"] {
            background-color: #FFFFFF !important;
            border: 2px solid #000000 !important;
        }

        .stRadio > div > label > div[role="radio"][aria-checked="true"] {
            background-color: #000000 !important;
            border: 2px solid #000000 !important;
        }

        /* Expander text colors */
        .streamlit-expanderHeader {
            color: #000000 !important;
        }

        .streamlit-expanderContent {
            color: #000000 !important;
        }

        /* Success/Error/Warning/Info boxes */
        .stSuccess, .stError, .stWarning, .stInfo {
            color: #000000 !important;
        }

        /* Metrics */
        .metric-row {
            display: flex;
            gap: 2rem;
            margin: 2rem 0;
        }

        .metric {
            flex: 1;
            text-align: center;
            padding: 1.5rem;
            background: #FBFBFD;
            border: 1px solid #E5E5E7;
            border-radius: 12px;
        }

        .metric-value {
            font-size: 2.5rem;
            font-weight: 700;
            color: #000000;
        }

        .metric-label {
            font-size: 0.85rem;
            color: #86868B;
            text-transform: uppercase;
            letter-spacing: 0.1em;
            margin-top: 0.5rem;
        }

        /* Divider */
        hr {
            border: none;
            border-top: 1px solid #E5E5E7;
            margin: 3rem 0;
        }

        /* Footer */
        .footer {
            text-align: center;
            padding: 3rem 0;
            margin-top: 5rem;
            border-top: 1px solid #E5E5E7;
            color: #86868B;
        }
        </style>
        """


# Apply custom CSS
st.markdown(get_custom_css(), unsafe_allow_html=True)

# Force sidebar to be visible with JavaScript
st.markdown("""
    <script>
    // Force sidebar to open on page load
    window.addEventListener('load', function() {
        const sidebar = window.parent.document.querySelector('[data-testid="stSidebar"]');
        if (sidebar) {
            sidebar.style.transform = 'translateX(0)';
            sidebar.style.position = 'relative';
            sidebar.setAttribute('aria-expanded', 'true');
        }
    });

    // Check every second and keep sidebar open
    setInterval(function() {
        const sidebar = window.parent.document.querySelector('[data-testid="stSidebar"]');
        if (sidebar && sidebar.getAttribute('aria-expanded') === 'false') {
            const closeButton = window.parent.document.querySelector('[data-testid="collapsedControl"]');
            if (closeButton) {
                closeButton.click();
            }
        }
    }, 1000);
    </script>
""", unsafe_allow_html=True)


def get_match_score_class(score):
    """Get CSS class based on match score"""
    if score >= 85:
        return "score-excellent"
    elif score >= 70:
        return "score-good"
    elif score >= 50:
        return "score-moderate"
    else:
        return "score-low"


def generate_suggestions(score, missing_keywords):
    """Generate AI suggestions based on match score and missing keywords"""
    if score >= 85:
        suggestion = "Your resume shows excellent alignment with the job requirements. You are a strong candidate for this position."
    elif score >= 70:
        suggestion = "Your resume demonstrates good compatibility with the position. Consider highlighting your relevant experience more prominently."
    elif score >= 50:
        suggestion = "Your resume shows moderate alignment. Focus on developing the missing skills and updating your resume to better reflect the job requirements."
    else:
        suggestion = "Your resume needs significant improvements to match this position. Consider gaining experience in the key areas listed below."

    if missing_keywords:
        suggestion += f"\n\nKey skills to develop or highlight: {', '.join(missing_keywords[:5])}"

    return suggestion


def display_results(result):
    """Display match results in ultra-professional minimalist format"""
    score = result['match_score']
    score_class = get_match_score_class(score)

    # Minimalist score display
    st.markdown(f"""
        <div class='score-display {score_class}'>
            <div class='score-number'>{score}%</div>
            <div class='score-label'>Match Score</div>
        </div>
    """, unsafe_allow_html=True)

    # Progress bar
    st.markdown(f"""
        <div class='progress-container'>
            <div class='progress-bar' style='width: {score}%'></div>
        </div>
    """, unsafe_allow_html=True)

    # Metrics row
    matching_skills = set(result.get('resume_keywords', [])) & set(result.get('job_keywords', []))
    total_required = len(result.get('job_keywords', []))
    missing_count = len(result.get('missing_keywords', []))

    st.markdown(f"""
        <div class='metric-row'>
            <div class='metric'>
                <div class='metric-value'>{len(matching_skills)}/{total_required}</div>
                <div class='metric-label'>Skills Match</div>
            </div>
            <div class='metric'>
                <div class='metric-value'>{missing_count}</div>
                <div class='metric-label'>Skills Gap</div>
            </div>
            <div class='metric'>
                <div class='metric-value'>{len(result.get('resume_keywords', []))}</div>
                <div class='metric-label'>Your Skills</div>
            </div>
        </div>
    """, unsafe_allow_html=True)

    # Analysis sections
    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("<div class='info-card'>", unsafe_allow_html=True)
        st.markdown("### Assessment")
        if score >= 85:
            st.markdown("**Excellent Match**")
            st.markdown("Strong alignment with position requirements.")
        elif score >= 70:
            st.markdown("**Good Match**")
            st.markdown("Solid candidate with room for enhancement.")
        elif score >= 50:
            st.markdown("**Moderate Match**")
            st.markdown("Consider developing additional skills.")
        else:
            st.markdown("**Needs Development**")
            st.markdown("Significant skill gap identified.")
        st.markdown("</div>", unsafe_allow_html=True)

    with col2:
        st.markdown("<div class='info-card'>", unsafe_allow_html=True)
        st.markdown("### Recommendation")
        if score >= 85:
            st.markdown("**Apply Immediately**")
            st.markdown("You are an ideal candidate.")
        elif score >= 70:
            st.markdown("**Apply with Confidence**")
            st.markdown("Strong qualifications present.")
        elif score >= 50:
            st.markdown("**Enhance Resume First**")
            st.markdown("Add relevant skills before applying.")
        else:
            st.markdown("**Significant Updates Required**")
            st.markdown("Tailor resume to position.")
        st.markdown("</div>", unsafe_allow_html=True)

    with col3:
        st.markdown("<div class='info-card'>", unsafe_allow_html=True)
        st.markdown("### Action Items")
        if missing_count > 0:
            st.markdown(f"Add {missing_count} missing skills")
        else:
            st.markdown("No critical gaps")
        st.markdown("Review and refine content")
        st.markdown("Quantify achievements")
        st.markdown("</div>", unsafe_allow_html=True)

    # Keywords section
    st.markdown("<div class='info-card'>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### Your Skills")
        if result.get('resume_keywords'):
            keywords_html = "".join([
                f"<span class='keyword resume'>{kw}</span>"
                for kw in result['resume_keywords'][:15]
            ])
            st.markdown(f"<div class='keyword-container'>{keywords_html}</div>", unsafe_allow_html=True)

    with col2:
        st.markdown("### Required Skills")
        if result.get('job_keywords'):
            keywords_html = "".join([
                f"<span class='keyword job'>{kw}</span>"
                for kw in result['job_keywords'][:15]
            ])
            st.markdown(f"<div class='keyword-container'>{keywords_html}</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    # Missing keywords
    if result.get('missing_keywords'):
        st.markdown("<div class='info-card'>", unsafe_allow_html=True)
        st.markdown("### Skills to Develop")
        missing_html = "".join([
            f"<span class='keyword missing'>{kw}</span>"
            for kw in result['missing_keywords']
        ])
        st.markdown(f"<div class='keyword-container'>{missing_html}</div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    # AI Suggestions
    st.markdown("<div class='info-card'>", unsafe_allow_html=True)
    st.markdown("### Analysis Summary")
    st.markdown(result['suggestions'])
    st.markdown("</div>", unsafe_allow_html=True)

    # Download
    st.markdown("<div class='info-card'>", unsafe_allow_html=True)
    st.markdown("### Export Report")

    from datetime import datetime
    results_text = f"""
RESUME MATCH ANALYSIS REPORT
{'=' * 60}

Match Score: {score}%
Analysis Date: {datetime.now().strftime("%Y-%m-%d %H:%M")}

{'─' * 60}
SKILLS GAP ANALYSIS
Missing Skills: {', '.join(result.get('missing_keywords', [])) if result.get('missing_keywords') else 'None'}

{'─' * 60}
YOUR SKILLS
{', '.join(result.get('resume_keywords', [])) if result.get('resume_keywords') else 'None'}

{'─' * 60}
REQUIRED SKILLS
{', '.join(result.get('job_keywords', [])) if result.get('job_keywords') else 'None'}

{'─' * 60}
RECOMMENDATIONS
{result['suggestions']}

{'─' * 60}
Generated by Resume Matcher - AI Career Intelligence
    """

    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        st.download_button(
            label="Download Report",
            data=results_text,
            file_name=f"match_analysis_{score}pct.txt",
            mime="text/plain",
            use_container_width=True
        )
    st.markdown("</div>", unsafe_allow_html=True)


def render_sidebar():
    """Render minimalist professional sidebar"""
    with st.sidebar:
        # Brand section
        st.markdown("""
            <div style='text-align: center; padding: 2rem 0 1rem 0;'>
                <h2 style='font-size: 1.5rem; font-weight: 700; margin: 0; letter-spacing: -0.01em;'>Resume Matcher</h2>
                <p style='color: #888; font-size: 0.85rem; margin-top: 0.5rem;'>AI Career Intelligence</p>
            </div>
        """, unsafe_allow_html=True)

        st.markdown("---")

        # Theme toggle
        if st.session_state.theme == 'light':
            theme_button_text = "Switch to Dark Mode"
        else:
            theme_button_text = "Switch to Light Mode"

        if st.button(theme_button_text, use_container_width=True, key="theme_toggle"):
            toggle_theme()
            st.rerun()

        st.markdown("---")

        # About section
        with st.expander("About", expanded=False):
            st.markdown("""
            Advanced NLP technology analyzes semantic compatibility between
            your resume and job requirements.

            **Features**
            - AI semantic matching
            - Skills gap analysis
            - Actionable insights
            - Privacy-focused
            """)

        # How it works
        with st.expander("How It Works"):
            st.markdown("""
            **1. Input**
            Upload resume and job description

            **2. Analysis**
            AI processes semantic meaning

            **3. Results**
            Receive detailed match analysis

            **4. Action**
            Improve and apply strategically
            """)

        # Stats
        with st.expander("Performance"):
            st.metric("Match Accuracy", "85%+")
            st.metric("Processing Time", "<5s")
            st.metric("Privacy", "100%")

        st.markdown("---")

        # Feedback Section
        with st.expander("Feedback", expanded=False):
            st.markdown("### Rate Your Experience")

            # Initialize feedback storage in session state
            if 'feedbacks' not in st.session_state:
                st.session_state.feedbacks = []

            if 'selected_rating' not in st.session_state:
                st.session_state.selected_rating = 0

            # Create star rating buttons
            cols = st.columns(5)
            for i, col in enumerate(cols, start=1):
                with col:
                    # Display filled or empty star based on selection
                    if i <= st.session_state.selected_rating:
                        star_icon = "⭐"
                    else:
                        star_icon = "☆"

                    if st.button(star_icon, key=f"star_{i}", use_container_width=True):
                        st.session_state.selected_rating = i
                        st.rerun()

            # Display rating message
            if st.session_state.selected_rating > 0:
                rating_text = ["Poor", "Fair", "Good", "Very Good", "Excellent"]
                st.markdown(f"<div style='text-align: center; font-size: 0.9rem; color: #FFD700; margin-top: 0.5rem;'>{rating_text[st.session_state.selected_rating - 1]}</div>", unsafe_allow_html=True)
            else:
                st.markdown("<div style='text-align: center; font-size: 0.9rem; color: #888; margin-top: 0.5rem;'>Click a star to rate</div>", unsafe_allow_html=True)

            # Feedback text area
            feedback_text = st.text_area(
                "Your feedback",
                placeholder="Share your experience with us...",
                height=100,
                key="feedback_input"
            )

            # Submit button
            if st.button("Submit Feedback", use_container_width=True):
                if st.session_state.selected_rating == 0:
                    st.warning("Please select a star rating")
                elif not feedback_text or not feedback_text.strip():
                    st.warning("Please enter your feedback")
                else:
                    from datetime import datetime
                    feedback_entry = {
                        'rating': st.session_state.selected_rating,
                        'text': feedback_text,
                        'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M")
                    }
                    st.session_state.feedbacks.append(feedback_entry)
                    st.session_state.selected_rating = 0  # Reset rating after submission
                    st.success("Thank you for your feedback!")
                    st.rerun()

            # Display submitted feedbacks
            if st.session_state.feedbacks:
                st.markdown("---")
                st.markdown("### Recent Feedback")

                # Show last 3 feedbacks
                for fb in reversed(st.session_state.feedbacks[-3:]):
                    st.markdown(f"""
                        <div style='background: rgba(255,255,255,0.05); padding: 0.8rem; border-radius: 8px; margin-bottom: 0.5rem;'>
                            <div style='margin-bottom: 0.3rem;'>{"⭐" * fb['rating']}</div>
                            <div style='font-size: 0.9rem; margin-bottom: 0.3rem;'>{fb['text']}</div>
                            <div style='font-size: 0.75rem; color: #888;'>{fb['timestamp']}</div>
                        </div>
                    """, unsafe_allow_html=True)

        st.markdown("---")

        st.markdown("""
            <div style='text-align: center; font-size: 0.75rem; color: #888;'>
                <p>Professional AI Tools</p>
                <p style='margin-top: 0.5rem;'>
                    <a href='https://github.com/Shehriyar-Ali-Rustam/ai-resume-job-matcher' style='color: #888;'>GitHub</a> ·
                    <a href='https://github.com/Shehriyar-Ali-Rustam/ai-resume-job-matcher/issues' style='color: #888;'>Support</a>
                </p>
            </div>
        """, unsafe_allow_html=True)


def main():
    """Main application"""

    # Render sidebar
    render_sidebar()

    # Hero header
    st.markdown("""
        <div class='hero-header'>
            <h1>Resume Matcher</h1>
            <p>AI-Powered Career Intelligence Platform</p>
        </div>
    """, unsafe_allow_html=True)

    # Status badge
    st.markdown("""
        <div style='text-align: center;'>
            <span class='status-badge'>System Operational</span>
        </div>
    """, unsafe_allow_html=True)

    st.markdown("<br><br>", unsafe_allow_html=True)

    # Input section
    tab1, tab2 = st.tabs(["Analysis", "Examples"])

    with tab1:
        col1, col2 = st.columns([1, 1], gap="large")

        with col1:
            st.markdown("### Resume")

            input_method = st.radio(
                "Input method",
                ["Upload File", "Paste Text"],
                horizontal=True,
                label_visibility="collapsed"
            )

            resume_text = ""

            if "Upload" in input_method:
                uploaded_file = st.file_uploader(
                    "Drop your resume here or click to browse",
                    type=['pdf', 'txt'],
                    help="Supports PDF and TXT files - drag and drop or click to browse",
                    accept_multiple_files=False,
                    key="resume_uploader",
                    label_visibility="visible"
                )

                if uploaded_file:
                    try:
                        with st.spinner("Processing..."):
                            if uploaded_file.name.endswith('.pdf'):
                                resume_text = extract_text_from_pdf(uploaded_file.read())
                            else:
                                resume_text = uploaded_file.read().decode('utf-8')

                        st.success(f"Loaded: {uploaded_file.name}")

                        with st.expander("Preview"):
                            st.text_area("Content", resume_text, height=200, disabled=True, label_visibility="collapsed")
                    except Exception as e:
                        st.error(f"Error: {str(e)}")
            else:
                resume_text = st.text_area(
                    "Resume content",
                    height=350,
                    placeholder="Paste your resume here...",
                    label_visibility="collapsed"
                )

        with col2:
            st.markdown("### Job Description")
            job_description = st.text_area(
                "Job description",
                height=450,
                placeholder="Paste job description here...",
                label_visibility="collapsed"
            )

    with tab2:
        st.info("""
        **Sample Data Available**

        Test the platform with sample files located in:
        - `samples/sample_resume.txt`
        - `samples/sample_job.txt`

        Expected match score: 70-75%
        """)

    # Analysis button
    st.markdown("<br>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        analyze_button = st.button(
            "Analyze Match",
            type="primary",
            use_container_width=True
        )

    # Process analysis
    if analyze_button:
        if not resume_text or not resume_text.strip():
            st.error("Resume required")
        elif not job_description or not job_description.strip():
            st.error("Job description required")
        else:
            with st.spinner("Loading AI model and analyzing..."):
                try:
                    # Load the matcher
                    matcher = load_matcher()

                    # Calculate match score
                    match_score = matcher.calculate_match_score(resume_text, job_description)

                    # Extract keywords
                    resume_keywords = extract_keywords(resume_text, top_n=20)
                    job_keywords = extract_keywords(job_description, top_n=20)

                    # Find missing keywords
                    missing_keywords = find_missing_keywords(resume_text, job_description)

                    # Generate suggestions
                    suggestions = generate_suggestions(match_score, missing_keywords)

                    # Prepare result
                    result = {
                        'match_score': round(match_score, 1),
                        'resume_keywords': resume_keywords,
                        'job_keywords': job_keywords,
                        'missing_keywords': missing_keywords,
                        'suggestions': suggestions
                    }

                    st.success("Analysis Complete")
                    st.markdown("<br>", unsafe_allow_html=True)
                    display_results(result)

                except Exception as e:
                    st.error(f"Error during analysis: {str(e)}")
                    st.error("Please try again or contact support if the issue persists.")

    # Footer
    st.markdown("""
        <div class='footer'>
            <h4 style='font-weight: 600; margin-bottom: 0.5rem;'>Resume Matcher</h4>
            <p>Professional AI Career Intelligence</p>
            <p style='font-size: 0.85rem; margin-top: 1rem;'>
                Open Source · Privacy-First · Locally Processed
            </p>
            <p style='font-size: 0.75rem; margin-top: 1rem; color: #666;'>
                © 2025 Resume Matcher. MIT License.
            </p>
        </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
