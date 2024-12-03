import streamlit as st
import pandas as pd
import plotly.express as px

def show_analysis(client_data, deposit_data, calendar_data):
    st.header("Strategy Recommendations")
    
    # Merge data
    deposit_data['deposit_date'] = pd.to_datetime(deposit_data['deposit_date'])
    merged_data = pd.merge_asof(
        deposit_data.sort_values('deposit_date'),
        calendar_data.sort_values('gregorian_date'),
        left_on='deposit_date',
        right_on='gregorian_date',
        direction='nearest'
    )
    
    merged_data = pd.merge(
        merged_data,
        client_data,
        on='client_id',
        how='left'
    )
    
    # Regional Analysis
    st.subheader("Regional Performance")
    region_metrics = merged_data.groupby(['month_name', 'client_geographical_region']).agg({
        'deposit_amount': ['sum', 'mean'],
        'client_id': 'nunique'
    }).round(2)
    region_metrics.columns = ['Total Deposits', 'Average Deposit', 'Unique Clients']
    region_metrics = region_metrics.reset_index()
    
    fig_region = px.bar(
        region_metrics,
        x='month_name',
        y='Total Deposits',
        color='client_geographical_region',
        title='Regional Deposit Performance',
        barmode='group'
    )
    st.plotly_chart(fig_region)
    
    # Residence Status Analysis
    st.subheader("Residence Status Analysis")
    residence_metrics = merged_data.groupby(['month_name', 'client_residence_status']).agg({
        'deposit_amount': ['sum', 'mean'],
        'client_id': 'nunique'
    }).round(2)
    residence_metrics.columns = ['Total Deposits', 'Average Deposit', 'Unique Clients']
    residence_metrics = residence_metrics.reset_index()
    
    fig_residence = px.bar(
        residence_metrics,
        x='month_name',
        y='Total Deposits',
        color='client_residence_status',
        title='Deposit Performance by Residence Status',
        barmode='group'
    )
    st.plotly_chart(fig_residence)
    
    # Age Group Analysis
    st.subheader("Age Group Analysis")
    merged_data['age_group'] = pd.cut(
        merged_data['client_age'],
        bins=[0, 25, 35, 45, 55, 100],
        labels=['18-25', '26-35', '36-45', '46-55', '55+']
    )
    
    age_metrics = merged_data.groupby(['month_name', 'age_group']).agg({
        'deposit_amount': ['sum', 'mean'],
        'client_id': 'nunique'
    }).round(2)
    age_metrics.columns = ['Total Deposits', 'Average Deposit', 'Unique Clients']
    age_metrics = age_metrics.reset_index()
    
    fig_age = px.bar(
        age_metrics,
        x='month_name',
        y='Total Deposits',
        color='age_group',
        title='Deposit Performance by Age Group',
        barmode='group'
    )
    st.plotly_chart(fig_age)
    
    # Key Findings
    st.subheader("Key Findings & Recommendations")
    
    # Region Analysis
    best_region = region_metrics[region_metrics['month_name'] == 'Month 3'].nlargest(1, 'Total Deposits')
    worst_region = region_metrics[region_metrics['month_name'] == 'Month 3'].nsmallest(1, 'Total Deposits')
    
    st.write("#### Regional Insights")
    st.write(f"- Best performing region: {best_region.iloc[0]['client_geographical_region']} (${best_region.iloc[0]['Total Deposits']:,.2f})")
    st.write(f"- Region needing attention: {worst_region.iloc[0]['client_geographical_region']} (${worst_region.iloc[0]['Total Deposits']:,.2f})")
    
    # Residence Status
    best_residence = residence_metrics[residence_metrics['month_name'] == 'Month 3'].nlargest(1, 'Average Deposit')
    st.write("#### Residence Status Insights")
    st.write(f"- Highest average deposits from: {best_residence.iloc[0]['client_residence_status']} (${best_residence.iloc[0]['Average Deposit']:,.2f})")
    
    # Age Groups
    best_age = age_metrics[age_metrics['month_name'] == 'Month 3'].nlargest(1, 'Total Deposits')
    st.write("#### Age Group Insights")
    st.write(f"- Most responsive age group: {best_age.iloc[0]['age_group']} (${best_age.iloc[0]['Total Deposits']:,.2f})")
    
    # Strategic Recommendations
    st.write("#### Strategic Recommendations")
    st.write("1. Geographic Focus:")
    st.write(f"   - Increase marketing efforts in {worst_region.iloc[0]['client_geographical_region']}")
    st.write(f"   - Replicate successful strategies from {best_region.iloc[0]['client_geographical_region']}")
    
    st.write("2. Demographic Targeting:")
    st.write(f"   - Primary focus on {best_age.iloc[0]['age_group']} age group")
    st.write(f"   - Tailor messaging for {best_residence.iloc[0]['client_residence_status']} status clients")
    
    st.write("3. Campaign Optimization:")
    st.write("   - Analyze successful regions for best practices")
    st.write("   - Develop region-specific marketing strategies")
    st.write("   - Consider demographic-specific messaging")
