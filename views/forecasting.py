import streamlit as st
import pandas as pd
from models.prophet_model import ProphetForecaster
from utils.visualizations import plot_forecast

def show():
    st.header("Future Sales Prediction 🔮")
    
    if 'data' not in st.session_state or st.session_state['data'].empty:
        st.error("Data not initialized.")
        return

    df = st.session_state['data']

    col1, col2 = st.columns([1, 3])

    with col1:
        st.subheader("Settings")
        # Filters
        store = st.selectbox("Store", ['All'] + list(df['Store'].unique()), key='fc_store')
        product = st.selectbox("Product", ['All'] + list(df['Product'].unique()), key='fc_prod')
        
        # FIX: Updated 'M' to 'ME' for Monthly End frequency to fix FutureWarning
        freq_map = {'Daily': 'D', 'Weekly': 'W', 'Monthly': 'ME'}
        freq_name = st.selectbox("Frequency", list(freq_map.keys()))
        horizon = st.number_input("Horizon (Periods)", 1, 365, 30)
        
        run_btn = st.button("Generate Forecast", type="primary")

    with col2:
        if run_btn:
            # Prep Data
            target_df = df.copy()
            if store != 'All': target_df = target_df[target_df['Store'] == store]
            if product != 'All': target_df = target_df[target_df['Product'] == product]
            
            if len(target_df) < 5:
                st.error("Not enough data to forecast.")
                return

            with st.spinner("Training Prophet model..."):
                try:
                    model = ProphetForecaster()
                    # Pass the pandas frequency code
                    pd_freq = freq_map[freq_name]
                    
                    model.train(target_df, freq=pd_freq)
                    forecast = model.predict(horizon)
                    
                    st.success("Forecast Generated Successfully")
                    
                    # Plot
                    fig = plot_forecast(target_df, forecast)
                    st.plotly_chart(fig, use_container_width=True)
                    
                    # Data Download
                    csv = forecast.to_csv(index=False).encode('utf-8')
                    st.download_button("Download Predictions", csv, "forecast.csv", "text/csv")
                    
                except Exception as e:
                    st.error(f"Forecasting Error: {str(e)}")