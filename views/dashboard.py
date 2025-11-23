import streamlit as st
import pandas as pd
import plotly.express as px

def show():
    st.header("Executive Dashboard")
    
    if 'data' not in st.session_state or st.session_state['data'].empty:
        st.warning("No data loaded. Please upload a file in settings.")
        return

    df = st.session_state['data']

    # Quick filters for dashboard only
    stores = ['All'] + list(df['Store'].unique())
    sel_store = st.selectbox("Quick Filter: Store", stores)
    
    if sel_store != 'All':
        df = df[df['Store'] == sel_store]

    # KPIs
    col1, col2, col3, col4 = st.columns(4)
    total_sales = df['Sales'].sum()
    avg_sales = df['Sales'].mean()
    
    col1.metric("Total Revenue", f"${total_sales:,.0f}")
    col2.metric("Avg Transaction", f"${avg_sales:,.2f}")
    col3.metric("Total Records", len(df))
    col4.metric("Unique Products", df['Product'].nunique())

    # Charts
    c1, c2 = st.columns(2)
    with c1:
        st.subheader("Sales Trend")
        # Resample to Monthly (ME) to reduce noise in large datasets
        trend = df.set_index('Date').resample('ME')['Sales'].sum().reset_index()
        fig_trend = px.line(trend, x='Date', y='Sales', markers=True)
        st.plotly_chart(fig_trend, use_container_width=True)
    
    with c2:
        st.subheader("Top Selling Products")
        top_prod = df.groupby('Product')['Sales'].sum().nlargest(10).reset_index()
        fig_bar = px.bar(top_prod, x='Sales', y='Product', orientation='h')
        st.plotly_chart(fig_bar, use_container_width=True)