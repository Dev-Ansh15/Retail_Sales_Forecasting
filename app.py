import streamlit as st
import pandas as pd
import os
import warnings

# Suppress warnings to keep UI clean
warnings.filterwarnings('ignore')

# Configure Page
st.set_page_config(page_title="Retail Sales Forecasting", page_icon="📈", layout="wide", initial_sidebar_state="collapsed")

# --- CSS for Top Ribbon Navigation ---
st.markdown("""
    <style>
        /* Hide Sidebar */
        [data-testid="stSidebar"] {display: none;}
        [data-testid="stSidebarCollapsedControl"] {display: none;}
        
        /* Style the Top Ribbon */
        .stRadio > div {
            flex-direction: row;
            background-color: #f0f2f6;
            padding: 10px;
            border-radius: 10px;
            justify-content: center;
        }
        .stRadio div[role='radiogroup'] > label {
            background: white;
            padding: 10px 20px;
            margin: 0 10px;
            border-radius: 5px;
            border: 1px solid #ddd;
        }
        .stRadio div[role='radiogroup'] > label[data-checked='true'] {
            background-color: #ff4b4b;
            color: white;
            border-color: #ff4b4b;
        }
    </style>
""", unsafe_allow_html=True)

# --- Load Data Global ---
from utils.data_loader import load_data

if 'data' not in st.session_state:
    # Default check
    DATA_SOURCE = 'data/retail_sales.csv'
    if os.path.exists("data/uploaded.csv"):
        DATA_SOURCE = "data/uploaded.csv"
    
    try:
        st.session_state['data'] = load_data(DATA_SOURCE)
        st.session_state['data_source_path'] = DATA_SOURCE
    except Exception as e:
        st.session_state['data'] = pd.DataFrame()

# --- Navigation Ribbon ---
st.title("🛒 Retail Intelligence AI")

# Ribbon Menu
menu = ["Dashboard", "Data Explorer", "Forecasting", "Factor Analysis"]
choice = st.radio("Navigate", menu, label_visibility="collapsed")
st.markdown("---")

# --- Routing ---
if choice == "Dashboard":
    from views import dashboard
    dashboard.show()
    
elif choice == "Data Explorer":
    from views import data_explorer
    data_explorer.show()

elif choice == "Forecasting":
    from views import forecasting
    forecasting.show()

elif choice == "Factor Analysis":
    from views import factor_analysis
    factor_analysis.show()

# --- Global File Uploader (Bottom of page for settings) ---
st.markdown("---")
with st.expander("⚙️ Data Settings & Upload"):
    uploaded_file = st.file_uploader("Upload New Dataset (CSV)", type=['csv'])
    if uploaded_file is not None:
        if not os.path.exists('data'):
            os.makedirs('data')
        with open(os.path.join("data", "uploaded.csv"), "wb") as f:
            f.write(uploaded_file.getbuffer())
        st.success("File uploaded! Refreshing...")
        # Reload data
        st.session_state['data'] = load_data("data/uploaded.csv")
        st.rerun()