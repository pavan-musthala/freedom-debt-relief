import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
from scipy import stats

def show_analysis(client_data, deposit_data, calendar_data):
    st.header("What-If Analysis")
    
    # Merge data
    deposit_data['deposit_date'] = pd.to_datetime(deposit_data['deposit_date'])
    merged_data = pd.merge_asof(
        deposit_data.sort_values('deposit_date'),
        calendar_data.sort_values('gregorian_date'),
        left_on='deposit_date',
        right_on='gregorian_date',
        direction='nearest'
    )
    
    # Calculate monthly metrics
    monthly_metrics = merged_data.groupby('month_name').agg({
        'deposit_amount': ['sum', 'mean', 'std'],
        'client_id': 'nunique'
    }).round(2)
    monthly_metrics.columns = ['Total Deposits', 'Average Deposit', 'Std Deposit', 'Unique Clients']
    
    # Month 6 Projection
    st.subheader("Month 6 Projection")
    
    # Calculate growth rates
    growth_rates = []
    for i in range(1, 5):
        current = monthly_metrics.iloc[i]['Total Deposits']
        previous = monthly_metrics.iloc[i-1]['Total Deposits']
        growth_rate = (current - previous) / previous
        growth_rates.append(growth_rate)
    
    avg_growth = np.mean(growth_rates)
    std_growth = np.std(growth_rates)
    
    # Project Month 6
    month5_deposits = monthly_metrics.iloc[-1]['Total Deposits']
    projected_month6 = month5_deposits * (1 + avg_growth)
    
    # Calculate confidence interval
    confidence_level = 0.95
    z_score = stats.norm.ppf((1 + confidence_level) / 2)
    margin_error = z_score * (std_growth * month5_deposits)
    
    lower_bound = projected_month6 - margin_error
    upper_bound = projected_month6 + margin_error
    
    # Display projections
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric(
            "Projected Month 6 Deposits",
            f"${projected_month6:,.2f}",
            f"{avg_growth*100:.1f}% growth"
        )
    with col2:
        st.metric("Lower Bound (95% CI)", f"${lower_bound:,.2f}")
    with col3:
        st.metric("Upper Bound (95% CI)", f"${upper_bound:,.2f}")
    
    # Scenario Analysis
    st.subheader("Scenario Analysis")
    
    # Let user select growth scenarios
    col1, col2 = st.columns(2)
    with col1:
        pessimistic_growth = st.slider(
            "Pessimistic Growth Rate",
            min_value=-50,
            max_value=0,
            value=-20,
            step=5,
            help="Percentage growth rate for pessimistic scenario"
        ) / 100
    
    with col2:
        optimistic_growth = st.slider(
            "Optimistic Growth Rate",
            min_value=0,
            max_value=50,
            value=20,
            step=5,
            help="Percentage growth rate for optimistic scenario"
        ) / 100
    
    # Calculate scenarios
    scenarios = {
        'Pessimistic': month5_deposits * (1 + pessimistic_growth),
        'Expected': projected_month6,
        'Optimistic': month5_deposits * (1 + optimistic_growth)
    }
    
    # Create scenario comparison
    scenario_df = pd.DataFrame({
        'Scenario': scenarios.keys(),
        'Projected Deposits': scenarios.values()
    })
    
    fig_scenarios = px.bar(
        scenario_df,
        x='Scenario',
        y='Projected Deposits',
        title='Month 6 Scenario Comparison',
        color='Scenario',
        color_discrete_map={
            'Pessimistic': 'red',
            'Expected': 'yellow',
            'Optimistic': 'green'
        }
    )
    st.plotly_chart(fig_scenarios)
    
    # Impact Analysis
    st.subheader("Campaign Impact Analysis")
    
    # Calculate campaign metrics
    baseline_months = ['Month 1', 'Month 2']
    baseline_deposits = monthly_metrics.loc[baseline_months, 'Total Deposits'].mean()
    
    # Calculate ROI for different scenarios
    campaign_cost = 5000000  # $5M campaign cost
    
    roi_scenarios = {}
    for scenario, month6_value in scenarios.items():
        # Calculate total incremental value
        incremental_value = (
            # Month 3 (campaign month)
            (monthly_metrics.loc['Month 3', 'Total Deposits'] - baseline_deposits) +
            # Months 4-5
            sum(monthly_metrics.loc[['Month 4', 'Month 5'], 'Total Deposits'] - baseline_deposits) +
            # Projected Month 6
            (month6_value - baseline_deposits)
        )
        
        # Calculate ROI
        roi = ((incremental_value - campaign_cost) / campaign_cost) * 100
        roi_scenarios[scenario] = roi
    
    # Display ROI scenarios
    st.write("#### ROI by Scenario")
    roi_df = pd.DataFrame({
        'Scenario': roi_scenarios.keys(),
        'ROI (%)': roi_scenarios.values()
    })
    
    fig_roi = px.bar(
        roi_df,
        x='Scenario',
        y='ROI (%)',
        title='Campaign ROI by Scenario',
        color='Scenario',
        color_discrete_map={
            'Pessimistic': 'red',
            'Expected': 'yellow',
            'Optimistic': 'green'
        }
    )
    st.plotly_chart(fig_roi)
    
    # Key Insights
    st.subheader("Key Insights")
    st.write(f"""
    1. Expected Month 6 Performance:
       - Projected deposits: ${projected_month6:,.2f}
       - 95% Confidence Interval: ${lower_bound:,.2f} to ${upper_bound:,.2f}
       
    2. Scenario Analysis:
       - Pessimistic (${pessimistic_growth*100:.0f}% growth): ${scenarios['Pessimistic']:,.2f}
       - Expected ({avg_growth*100:.1f}% growth): ${scenarios['Expected']:,.2f}
       - Optimistic (${optimistic_growth*100:.0f}% growth): ${scenarios['Optimistic']:,.2f}
       
    3. ROI Implications:
       - Pessimistic ROI: {roi_scenarios['Pessimistic']:.1f}%
       - Expected ROI: {roi_scenarios['Expected']:.1f}%
       - Optimistic ROI: {roi_scenarios['Optimistic']:.1f}%
    """)
