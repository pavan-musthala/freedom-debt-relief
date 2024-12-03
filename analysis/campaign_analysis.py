import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

def show_analysis(client_data, deposit_data, calendar_data):
    st.header("📈 Campaign Performance Analysis")
    st.markdown("""
        > Analyzing deposit trends, client engagement, and ROI across the campaign timeline to measure effectiveness
        and identify key success factors.
    """)
    
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
        'deposit_amount': ['sum', 'mean', 'count', 'std'],
        'client_id': ['nunique', 'count']
    }).round(2)
    
    monthly_metrics.columns = [
        'Total Deposits ($)', 'Average Deposit ($)', 
        'Number of Deposits', 'Deposit Std ($)',
        'Unique Clients', 'Total Transactions'
    ]
    
    # High-level KPIs
    st.subheader("🎯 Key Performance Indicators")
    
    # Calculate KPI metrics
    baseline_months = ['Month 1', 'Month 2']
    campaign_month = 'Month 3'
    post_campaign_months = ['Month 4', 'Month 5']
    
    baseline_deposits = monthly_metrics.loc[baseline_months, 'Total Deposits ($)'].mean()
    campaign_deposits = monthly_metrics.loc[campaign_month, 'Total Deposits ($)']
    post_campaign_deposits = monthly_metrics.loc[post_campaign_months, 'Total Deposits ($)'].mean()
    
    # Display KPIs in columns
    st.markdown('<div class="kpi-grid">', unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        growth_vs_baseline = ((campaign_deposits - baseline_deposits) / baseline_deposits) * 100
        st.metric(
            "Campaign Month Growth",
            f"{growth_vs_baseline:,.1f}%",
            delta=f"{growth_vs_baseline:,.1f}%",
            delta_color="normal"
        )
    
    with col2:
        retention = ((post_campaign_deposits - baseline_deposits) / (campaign_deposits - baseline_deposits)) * 100
        st.metric(
            "Effect Retention",
            f"{retention:,.1f}%",
            delta=None
        )
    
    with col3:
        campaign_clients = monthly_metrics.loc[campaign_month, 'Unique Clients']
        baseline_clients = monthly_metrics.loc[baseline_months, 'Unique Clients'].mean()
        client_growth = ((campaign_clients - baseline_clients) / baseline_clients) * 100
        st.metric(
            "Client Growth",
            f"{client_growth:,.1f}%",
            delta=f"{client_growth:,.1f}%",
            delta_color="normal"
        )
    
    with col4:
        campaign_avg = monthly_metrics.loc[campaign_month, 'Average Deposit ($)']
        baseline_avg = monthly_metrics.loc[baseline_months, 'Average Deposit ($)'].mean()
        avg_deposit_growth = ((campaign_avg - baseline_avg) / baseline_avg) * 100
        st.metric(
            "Avg Deposit Growth",
            f"{avg_deposit_growth:,.1f}%",
            delta=f"{avg_deposit_growth:,.1f}%",
            delta_color="normal"
        )
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Deposit Trends Analysis
    st.subheader("💰 Deposit Trends Analysis")
    
    # Create subplot with shared x-axis
    fig = make_subplots(
        rows=2, cols=1,
        shared_xaxes=True,
        vertical_spacing=0.1,
        subplot_titles=("Monthly Deposit Trends", "Client Engagement Metrics")
    )
    
    # Add deposit trends
    fig.add_trace(
        go.Scatter(
            x=monthly_metrics.index,
            y=monthly_metrics['Total Deposits ($)'],
            name="Total Deposits",
            line=dict(color='#1f77b4', width=3),
            mode='lines+markers'
        ),
        row=1, col=1
    )
    
    # Add client engagement metrics
    fig.add_trace(
        go.Scatter(
            x=monthly_metrics.index,
            y=monthly_metrics['Unique Clients'],
            name="Unique Clients",
            line=dict(color='#2ca02c', width=2),
            mode='lines+markers'
        ),
        row=2, col=1
    )
    
    fig.add_trace(
        go.Scatter(
            x=monthly_metrics.index,
            y=monthly_metrics['Total Transactions'],
            name="Total Transactions",
            line=dict(color='#ff7f0e', width=2, dash='dot'),
            mode='lines+markers'
        ),
        row=2, col=1
    )
    
    # Update layout
    fig.update_layout(
        height=700,
        showlegend=True,
        title_text="Campaign Impact on Deposits and Client Engagement"
    )
    
    # Add campaign month annotation separately
    fig.add_annotation(
        x='Month 3',
        y=monthly_metrics.loc['Month 3', 'Total Deposits ($)'],
        text="Campaign Month",
        showarrow=True,
        arrowhead=1,
        yref='y1'
    )
    
    # Add phase backgrounds
    phases = [
        dict(type="rect", x0="Month 1", x1="Month 2", y0=0, y1=1, 
             fillcolor="lightblue", opacity=0.2, layer="below", yref="paper", name="Pre-Campaign"),
        dict(type="rect", x0="Month 3", x1="Month 3", y0=0, y1=1, 
             fillcolor="orange", opacity=0.2, layer="below", yref="paper", name="Campaign"),
        dict(type="rect", x0="Month 4", x1="Month 5", y0=0, y1=1, 
             fillcolor="lightgreen", opacity=0.2, layer="below", yref="paper", name="Post-Campaign")
    ]
    
    for phase in phases:
        fig.add_shape(phase, row=1, col=1)
        fig.add_shape(phase, row=2, col=1)
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Deposit Pattern Analysis
    st.subheader("📊 Deposit Pattern Analysis")
    col1, col2 = st.columns(2)
    
    with col1:
        # Deposits by type
        deposit_type_metrics = merged_data.groupby(['month_name', 'deposit_type']).agg({
            'deposit_amount': 'sum',
            'client_id': 'nunique'
        }).round(2)
        
        fig_types = px.bar(
            deposit_type_metrics.reset_index(),
            x='month_name',
            y='deposit_amount',
            color='deposit_type',
            title='Deposit Types Over Time',
            labels={'deposit_amount': 'Total Deposits ($)', 'month_name': 'Month'},
            barmode='group'
        )
        st.plotly_chart(fig_types)
    
    with col2:
        # Deposit cadence analysis
        cadence_metrics = merged_data.groupby(['month_name', 'deposit_cadence']).agg({
            'deposit_amount': 'sum',
            'client_id': 'nunique'
        }).round(2)
        
        fig_cadence = px.bar(
            cadence_metrics.reset_index(),
            x='month_name',
            y='client_id',
            color='deposit_cadence',
            title='Deposit Cadence Distribution',
            labels={'client_id': 'Number of Clients', 'month_name': 'Month'},
            barmode='stack'
        )
        st.plotly_chart(fig_cadence)
    
    # ROI Analysis
    st.subheader("💹 Campaign ROI Analysis")
    
    campaign_cost = 5000000  # $5M campaign cost
    
    # Calculate incremental revenue
    incremental_campaign = campaign_deposits - baseline_deposits
    incremental_post = sum(monthly_metrics.loc[post_campaign_months, 'Total Deposits ($)'] - baseline_deposits)
    total_incremental = incremental_campaign + incremental_post
    
    roi = ((total_incremental - campaign_cost) / campaign_cost) * 100
    
    # Display ROI metrics
    st.markdown('<div class="kpi-grid">', unsafe_allow_html=True)
    
    roi_col1, roi_col2, roi_col3, roi_col4 = st.columns(4)
    
    with roi_col1:
        st.metric(
            "Campaign Month Lift",
            f"${incremental_campaign:,.2f}",
            delta=None
        )
    
    with roi_col2:
        st.metric(
            "Post-Campaign Lift",
            f"${incremental_post:,.2f}",
            delta=None
        )
    
    with roi_col3:
        st.metric(
            "Total Incremental Value",
            f"${total_incremental:,.2f}",
            delta=None
        )
    
    with roi_col4:
        st.metric(
            "Campaign ROI",
            f"{roi:.1f}%",
            delta=f"{roi:.1f}%",
            delta_color="normal"
        )
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Campaign Success Assessment
    st.subheader("📊 Campaign Success Assessment")
    
    # Calculate success metrics
    avg_baseline_clients = monthly_metrics.loc[baseline_months, 'Unique Clients'].mean()
    campaign_clients = monthly_metrics.loc[campaign_month, 'Unique Clients']
    post_campaign_clients = monthly_metrics.loc[post_campaign_months, 'Unique Clients'].mean()
    
    # Calculate incremental clients
    incremental_clients = campaign_clients - avg_baseline_clients
    
    # Calculate client acquisition cost (protect against division by zero)
    acquisition_cost = campaign_cost / incremental_clients if incremental_clients > 0 else float('inf')
    
    # Calculate lifetime value (using post-campaign average deposits)
    avg_post_campaign_deposit = monthly_metrics.loc[post_campaign_months, 'Average Deposit ($)'].mean()
    estimated_lifetime_value = avg_post_campaign_deposit * 12  # Annualized value
    
    # Calculate ROI multiple
    roi_multiple = estimated_lifetime_value / acquisition_cost if acquisition_cost > 0 else 0
    
    # Display metrics
    st.markdown('<div class="kpi-grid">', unsafe_allow_html=True)
    
    success_col1, success_col2, success_col3 = st.columns(3)
    
    with success_col1:
        st.metric(
            "Client Acquisition Cost",
            f"${acquisition_cost:,.2f}" if acquisition_cost != float('inf') else "N/A",
            delta=None
        )
    
    with success_col2:
        st.metric(
            "Estimated Client LTV",
            f"${estimated_lifetime_value:,.2f}",
            delta=None
        )
    
    with success_col3:
        st.metric(
            "ROI Multiple",
            f"{roi_multiple:.1f}x" if roi_multiple > 0 else "N/A",
            delta=None
        )
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Format metrics text with proper error handling
    metrics_text = f"""
    #### Campaign Success Metrics & Rationale
    
    1. **Primary Success Metrics**:
       - ROI: {roi:.1f}% (Measures direct financial impact)
       - Client Acquisition Cost: {f"${acquisition_cost:,.2f}" if acquisition_cost != float('inf') else "N/A"} (Efficiency of client acquisition)
       - LTV/CAC Ratio: {f"{roi_multiple:.1f}x" if roi_multiple > 0 else "N/A"} (Long-term value creation)
    
    2. **Why These Metrics**:
       - ROI captures immediate financial return
       - CAC measures acquisition efficiency
       - LTV/CAC indicates long-term sustainability
       - Combined metrics provide holistic view of campaign success
    
    3. **Success Threshold Analysis**:
       - Industry benchmark for LTV/CAC is 3x
       - Our campaign achieved {f"{roi_multiple:.1f}x" if roi_multiple > 0 else "N/A"}
       - ROI of {roi:.1f}% {"exceeds" if roi > 15 else "meets" if roi > 0 else "falls below"} typical marketing campaign returns
    """
    
    st.markdown(metrics_text)
    
    # Strategic Recommendations
    st.subheader("🎯 Future Campaign Strategy Recommendations")
    
    # Analyze by deposit type
    deposit_type_performance = merged_data[merged_data['month_name'] == 'Month 3'].groupby(
        'deposit_type'
    ).agg({
        'deposit_amount': ['mean', 'sum', 'count'],
        'client_id': 'nunique'
    }).round(2)
    
    # Analyze by deposit cadence
    cadence_performance = merged_data[merged_data['month_name'] == 'Month 3'].groupby(
        'deposit_cadence'
    ).agg({
        'deposit_amount': ['mean', 'sum', 'count'],
        'client_id': 'nunique'
    }).round(2)
    
    # Find best performing segments
    deposit_type_sums = deposit_type_performance[('deposit_amount', 'sum')]
    best_deposit_type = deposit_type_sums.idxmax()
    best_deposit_type_amount = deposit_type_sums.max()
    
    cadence_sums = cadence_performance[('deposit_amount', 'sum')]
    best_cadence = cadence_sums.idxmax()
    best_cadence_amount = cadence_sums.max()
    
    # Display performance metrics
    st.markdown('<div class="kpi-grid">', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.metric(
            "Best Performing Deposit Type",
            best_deposit_type,
            delta=f"${best_deposit_type_amount:,.2f} total deposits"
        )
    
    with col2:
        st.metric(
            "Best Performing Cadence",
            best_cadence,
            delta=f"${best_cadence_amount:,.2f} total deposits"
        )
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown(f"""
    #### Recommended Strategy Adjustments
    
    1. **Deposit Type Optimization**:
       - Focus on promoting {best_deposit_type} deposits
       - Highest total deposit volume during campaign
       - Consider incentives for this deposit type
    
    2. **Deposit Cadence Strategy**:
       - Optimize for {best_cadence} deposit schedule
       - Showed strongest performance
       - Align messaging with preferred cadence
    
    3. **Campaign Timing**:
       - Maintain Month 3 timing for future campaigns
       - Aligns with observed deposit patterns
       - Capitalizes on established momentum
    """)
    
    # Show detailed performance tables
    st.subheader("Detailed Performance Analysis")
    
    # Format column names for better display
    deposit_type_performance.columns = [f"{col[0]} {col[1]}".title() for col in deposit_type_performance.columns]
    cadence_performance.columns = [f"{col[0]} {col[1]}".title() for col in cadence_performance.columns]
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("Deposit Type Performance")
        st.dataframe(deposit_type_performance.style.format({
            'Deposit_amount Sum': '${:,.2f}',
            'Deposit_amount Mean': '${:,.2f}'
        }))
    
    with col2:
        st.write("Deposit Cadence Performance")
        st.dataframe(cadence_performance.style.format({
            'Deposit_amount Sum': '${:,.2f}',
            'Deposit_amount Mean': '${:,.2f}'
        }))
    
    # Month 6 Projection Analysis
    st.subheader("🔮 Alternative Timing Analysis")
    
    # Calculate trend-based projection for Month 6
    monthly_growth = (monthly_metrics['Total Deposits ($)'].pct_change().mean())
    projected_baseline = baseline_deposits * (1 + monthly_growth) ** 5  # Project to Month 6
    
    # Calculate campaign impact if moved to Month 6
    campaign_lift_percentage = (campaign_deposits - baseline_deposits) / baseline_deposits
    projected_month6_with_campaign = projected_baseline * (1 + campaign_lift_percentage)
    
    # Calculate incremental difference
    current_total_impact = incremental_campaign + incremental_post
    projected_impact = projected_month6_with_campaign - projected_baseline
    
    st.markdown(f"""
    #### Month 6 Campaign Scenario Analysis
    
    1. **Current Campaign Impact (Month 3)**:
       - Total Incremental Value: ${current_total_impact:,.2f}
       - ROI: {roi:.1f}%
    
    2. **Projected Month 6 Impact**:
       - Projected Incremental Value: ${projected_impact:,.2f}
       - Projected ROI: {((projected_impact - campaign_cost) / campaign_cost * 100):.1f}%
    
    3. **Incremental Difference**:
       - Value Difference: ${(projected_impact - current_total_impact):,.2f}
       - Recommendation: {'Postpone to Month 6' if projected_impact > current_total_impact else 'Keep Month 3 timing'}
    """)
    
    # Key Insights
    st.subheader("💡 Key Insights")
    
    # Calculate insights
    best_deposit_type = deposit_type_metrics.xs('Month 3', level='month_name').nlargest(1, 'deposit_amount')
    best_cadence = cadence_metrics.xs('Month 3', level='month_name').nlargest(1, 'client_id')
    
    st.markdown(f"""
    #### Campaign Impact
    - The campaign drove a **{growth_vs_baseline:,.1f}%** increase in total deposits during Month 3
    - Client base expanded by **{client_growth:,.1f}%** during the campaign
    - Average deposit value grew by **{avg_deposit_growth:,.1f}%**
    - Post-campaign retention rate of **{retention:,.1f}%** indicates sustainable impact
    
    #### Deposit Patterns
    - Most successful deposit type: **{best_deposit_type.index[0]}**
    - Preferred deposit cadence: **{best_cadence.index[0]}**
    - Client transaction frequency increased by **{((monthly_metrics.loc['Month 3', 'Total Transactions'] / monthly_metrics.loc['Month 3', 'Unique Clients']) / (monthly_metrics.loc['Month 1', 'Total Transactions'] / monthly_metrics.loc['Month 1', 'Unique Clients']) - 1) * 100:.1f}%**
    
    #### Financial Impact
    - Total incremental value: **${total_incremental:,.2f}**
    - Campaign ROI: **{roi:.1f}%**
    - Average monthly lift: **${(incremental_campaign + incremental_post) / 3:,.2f}**
    """)
