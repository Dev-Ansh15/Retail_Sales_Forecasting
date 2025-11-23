import streamlit as st
import plotly.express as px

def show():
    st.header("Data Explorer 🔍")
    
    if 'data' not in st.session_state or st.session_state['data'].empty:
        st.error("Data not initialized.")
        return

    df = st.session_state['data']

    # Filters
    col1, col2 = st.columns(2)
    with col1:
        stores = st.multiselect("Filter Stores", df['Store'].unique())
    with col2:
        products = st.multiselect("Filter Products", df['Product'].unique())

    # Apply Filters
    filtered_df = df.copy()
    if stores:
        filtered_df = filtered_df[filtered_df['Store'].isin(stores)]
    if products:
        filtered_df = filtered_df[filtered_df['Product'].isin(products)]

    # Tabs
    tab1, tab2 = st.tabs(["Raw Data", "Visualizations"])

    with tab1:
        # Using width="stretch" per new Streamlit recommendations for full width
        st.dataframe(filtered_df, use_container_width=True)
    
    with tab2:
        st.subheader("Distribution Analysis")
        fig = px.histogram(filtered_df, x="Sales", nbins=50, title="Sales Distribution")
        st.plotly_chart(fig, use_container_width=True)