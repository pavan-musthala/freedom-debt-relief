import streamlit as st

def show_overview():
    st.title("Campaign Analysis Dashboard Overview")
    
    # Campaign Overview
    st.header("📊 Campaign Overview")
    st.markdown("""
    This dashboard provides comprehensive analysis of our $5 million marketing campaign performance,
    helping optimize strategy and ROI through data-driven insights.
    
    ### 🎯 Key Objectives
    1. **Performance Analysis**: Track and measure campaign effectiveness
    2. **ROI Optimization**: Identify highest-performing segments
    3. **Strategic Planning**: Generate actionable insights for future campaigns
    """)
    
    # Dashboard Features
    st.header("🛠️ Dashboard Features")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        #### Campaign Performance
        - Monthly deposit trends
        - Client acquisition metrics
        - ROI analysis
        - Segment performance
        
        #### Strategic Insights
        - Best performing deposit types
        - Optimal deposit cadence
        - Client behavior patterns
        """)
        
    with col2:
        st.markdown("""
        #### What-If Analysis
        - Future projections
        - Scenario modeling
        - Timing optimization
        
        #### Data Filtering
        - Time period selection
        - Deposit type filtering
        - Custom metric views
        """)
    
    # Business Value
    st.header("💡 Business Value")
    st.markdown("""
    ### Key Benefits
    1. **Data-Driven Decisions**: Make informed campaign strategy decisions based on actual performance data
    2. **Resource Optimization**: Identify and focus on highest-performing segments and strategies
    3. **ROI Maximization**: Optimize future campaigns based on historical performance insights
    4. **Risk Mitigation**: Better understand client behavior and campaign timing impacts
    """)
    
    # Usage Instructions
    st.header("📝 Usage Instructions")
    st.markdown("""
    ### Navigation Guide
    1. Use the sidebar filters to select specific time periods or deposit types
    2. Navigate through different analysis tabs:
       - Campaign Performance: View core metrics and trends
       - Strategic Insights: Explore segment performance and recommendations
       - What-If Analysis: Model different scenarios
    3. Hover over charts for detailed information
    4. Click legends to toggle data series
    """)
    
    # Data Sources
    st.header("📚 Data Sources")
    st.markdown("""
    ### Analysis based on:
    - Client demographic data
    - Deposit transaction records
    - Campaign timeline data
    
    *Data is updated daily to ensure current insights*
    """)
    
    # Add a divider before the main analysis
    st.markdown("---")
