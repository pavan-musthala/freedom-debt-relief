import streamlit as st
import pandas as pd
import numpy as np
from analysis import campaign_analysis, strategy_recommendations, what_if_analysis, dashboard_overview
import os

# Set page configuration with a wider layout and custom theme
st.set_page_config(
    page_title="Debt Relief Campaign Analysis",
    page_icon="📊",
    layout="wide"
)

# Custom CSS for enhanced UI
st.markdown("""
<style>
    /* Main container styling */
    .main {
        padding: 2rem;
        max-width: 1200px;
        margin: 0 auto;
        background-color: #121212;
        color: #ffffff;
    }
    
    /* Header styling */
    h1 {
        color: #ffffff;
        font-size: 2.5rem;
        font-weight: 600;
        margin-bottom: 1.5rem;
        padding-bottom: 1rem;
        border-bottom: 3px solid #1E88E5;
    }
    
    h2 {
        color: #ffffff;
        font-size: 1.8rem;
        font-weight: 500;
        margin-top: 2rem;
        margin-bottom: 1rem;
    }
    
    h3 {
        color: #ffffff;
        font-size: 1.4rem;
        font-weight: 500;
    }
    
    /* Card styling */
    .objective-card {
        background-color: #1e1e1e;
        padding: 1.5rem;
        border-radius: 0.8rem;
        margin: 1rem 0;
        border: 1px solid #333333;
        box-shadow: 0 2px 4px rgba(0,0,0,0.2);
        transition: transform 0.2s ease, box-shadow 0.2s ease;
        color: #ffffff;
    }
    
    .objective-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0,0,0,0.3);
    }
    
    /* Metric styling */
    .stMetric {
        background: linear-gradient(145deg, #1e1e1e, #2a2a2a);
        padding: 1.5rem;
        border-radius: 1rem;
        border: 1px solid #333333;
        box-shadow: 0 4px 12px rgba(0,0,0,0.3);
        margin: 1rem 0;
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }
    
    .stMetric:hover {
        transform: translateY(-5px);
        box-shadow: 0 6px 16px rgba(0,0,0,0.4);
    }
    
    /* KPI Label styling */
    .stMetric label {
        color: #90CAF9 !important;
        font-size: 1.1rem !important;
        font-weight: 600 !important;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin-bottom: 0.5rem;
    }
    
    /* KPI Value styling */
    .stMetric [data-testid="stMetricValue"] {
        color: #ffffff !important;
        font-size: 2rem !important;
        font-weight: 700 !important;
        text-shadow: 0 2px 4px rgba(0,0,0,0.2);
    }
    
    /* KPI Delta styling */
    .stMetric [data-testid="stMetricDelta"] {
        font-size: 1.1rem !important;
        font-weight: 600 !important;
        padding: 0.2rem 0.5rem;
        border-radius: 0.5rem;
    }
    
    /* Positive Delta */
    .stMetric [data-testid="stMetricDelta"].positive {
        color: #4CAF50 !important;
        background: rgba(76, 175, 80, 0.1);
    }
    
    /* Negative Delta */
    .stMetric [data-testid="stMetricDelta"].negative {
        color: #FF5252 !important;
        background: rgba(255, 82, 82, 0.1);
    }
    
    /* KPI Grid Layout */
    .kpi-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
        gap: 1.5rem;
        padding: 1rem 0;
    }
    
    /* Button styling */
    .stButton>button {
        background-color: #1E88E5;
        color: #ffffff;
        border-radius: 0.5rem;
        padding: 0.5rem 1rem;
        border: none;
        box-shadow: 0 2px 4px rgba(0,0,0,0.2);
        transition: all 0.2s ease;
    }
    
    .stButton>button:hover {
        background-color: #1565C0;
        box-shadow: 0 4px 8px rgba(0,0,0,0.3);
    }
    
    /* Sidebar styling */
    .css-1d391kg {
        padding: 2rem 1rem;
        background-color: #1e1e1e;
        color: #ffffff;
    }
    
    /* Table styling */
    .stDataFrame {
        border: 1px solid #333333;
        border-radius: 0.5rem;
        overflow: hidden;
        color: #ffffff;
        background-color: #1e1e1e;
    }
    
    /* Alert styling */
    .stAlert {
        border-radius: 0.5rem;
        border: none;
        box-shadow: 0 2px 4px rgba(0,0,0,0.2);
        background-color: #1e1e1e;
        color: #ffffff;
    }
    
    /* Custom markdown text */
    .markdown-text-container {
        line-height: 1.6;
        color: #ffffff;
    }
    
    /* Improved link styling */
    a {
        color: #64B5F6;
        text-decoration: none;
        transition: color 0.2s ease;
    }
    
    a:hover {
        color: #90CAF9;
        text-decoration: underline;
    }
    
    /* Radio buttons */
    .stRadio > label {
        color: #ffffff;
    }
    
    /* Selectbox */
    .stSelectbox > label {
        color: #ffffff;
    }
    
    /* Multiselect */
    .stMultiSelect > label {
        color: #ffffff;
    }
    
    /* Dark theme overrides */
    .stApp {
        background-color: #121212;
    }
    
    .st-bk {
        background-color: #1e1e1e;
    }
    
    .st-c0 {
        color: #ffffff;
    }
    
    .st-bq {
        color: #ffffff;
    }
    
    /* Input fields */
    .stTextInput>div>div>input {
        background-color: #1e1e1e;
        color: #ffffff;
        border-color: #333333;
    }
    
    /* Dropdown */
    .stSelectbox>div>div>select {
        background-color: #1e1e1e;
        color: #ffffff;
        border-color: #333333;
    }
</style>
""", unsafe_allow_html=True)

def load_data():
    try:
        # Load client data
        client_data = pd.read_csv('client_data.csv')
        
        # Load deposit data
        deposit_data = pd.read_csv('deposit_data1.csv')
        deposit_data['deposit_date'] = pd.to_datetime(deposit_data['deposit_date'])
        
        # Load calendar data
        calendar_data = pd.read_csv('calendar_data.csv')
        calendar_data['gregorian_date'] = pd.to_datetime(calendar_data['gregorian_date'])
        
        return client_data, deposit_data, calendar_data
    except Exception as e:
        st.error(f"Error loading data: {str(e)}")
        return None, None, None

def main():
    # Load data
    client_data, deposit_data, calendar_data = load_data()
    
    if client_data is None or deposit_data is None or calendar_data is None:
        st.error("⚠️ Failed to load data. Please check the data files and their contents.")
        return
    
    # Sidebar navigation with icons
    st.sidebar.title("📊 Navigation")
    analysis_type = st.sidebar.radio(
        "Choose Analysis Type",
        ["📋 Overview", "📈 Campaign Performance", "🎯 Strategy Recommendations", "🔮 What-If Analysis"]
    )
    
    # Add filters in sidebar
    st.sidebar.title("🔍 Filters")
    
    # Region filter
    if 'client_geographical_region' in client_data.columns:
        selected_regions = st.sidebar.multiselect(
            "Filter by Region",
            options=sorted(client_data['client_geographical_region'].unique()),
            default=sorted(client_data['client_geographical_region'].unique())
        )
    else:
        selected_regions = None
    
    # Residence status filter
    if 'client_residence_status' in client_data.columns:
        selected_status = st.sidebar.multiselect(
            "Filter by Residence Status",
            options=sorted(client_data['client_residence_status'].unique()),
            default=sorted(client_data['client_residence_status'].unique())
        )
    else:
        selected_status = None
    
    # Date range filter
    date_range = st.sidebar.date_input(
        "Select Date Range",
        value=(deposit_data['deposit_date'].min(), deposit_data['deposit_date'].max()),
        min_value=deposit_data['deposit_date'].min(),
        max_value=deposit_data['deposit_date'].max()
    )
    
    # Apply filters
    start_date, end_date = pd.to_datetime(date_range[0]), pd.to_datetime(date_range[1])
    
    filtered_deposit_data = deposit_data[
        (deposit_data['deposit_date'] >= start_date) &
        (deposit_data['deposit_date'] <= end_date)
    ]
    
    if selected_regions is not None and selected_status is not None:
        filtered_client_data = client_data[
            (client_data['client_geographical_region'].isin(selected_regions)) &
            (client_data['client_residence_status'].isin(selected_status))
        ]
    else:
        filtered_client_data = client_data.copy()
    
    filtered_deposit_data = filtered_deposit_data[
        filtered_deposit_data['client_id'].isin(filtered_client_data['client_id'])
    ]
    
    # Display content based on selection
    if "Overview" in analysis_type:
        dashboard_overview.show_overview()
    elif "Campaign Performance" in analysis_type:
        campaign_analysis.show_analysis(filtered_client_data, filtered_deposit_data, calendar_data)
    elif "Strategy Recommendations" in analysis_type:
        strategy_recommendations.show_analysis(filtered_client_data, filtered_deposit_data, calendar_data)
    else:
        what_if_analysis.show_analysis(filtered_client_data, filtered_deposit_data, calendar_data)

if __name__ == "__main__":
    main()
