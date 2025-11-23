import streamlit as st
import pandas as pd # FIX: Added missing import
import plotly.express as px
from utils.visualizations import plot_heatmap

def show():
    st.header("Factor Analysis 📊")
    
    if 'data' not in st.session_state or st.session_state['data'].empty:
        st.error("Data not initialized.")
        return

    df = st.session_state['data']
    
    # Seasonality
    st.subheader("Seasonality Analysis")
    
    # Resample to Monthly Average (FIX: 'ME' instead of 'M')
    if 'Date' in df.columns:
        monthly = df.set_index('Date').resample('ME')['Sales'].mean().reset_index()
        monthly['Month'] = monthly['Date'].dt.month_name()
        
        # Sort order
        order = ['January', 'February', 'March', 'April', 'May', 'June', 
                 'July', 'August', 'September', 'October', 'November', 'December']
        
        fig_season = px.bar(monthly, x='Month', y='Sales', title="Avg Sales by Month")
        fig_season.update_xaxes(categoryorder='array', categoryarray=order)
        st.plotly_chart(fig_season, use_container_width=True)

    # Heatmap
    st.subheader("Weekly Traffic Heatmap")
    st.plotly_chart(plot_heatmap(df), use_container_width=True)