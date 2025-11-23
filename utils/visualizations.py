import plotly.graph_objects as go
import plotly.express as px
import pandas as pd

def plot_forecast(history_df, forecast_df, title="Sales Forecast"):
    fig = go.Figure()
    
    # 1. Historical Data (Last 90 days to keep chart clean)
    # Resample history to match forecast frequency if needed for cleaner lines
    history_subset = history_df.tail(90)
    
    fig.add_trace(go.Scatter(
        x=history_subset['Date'], 
        y=history_subset['Sales'],
        mode='lines+markers', 
        name='Historical Sales',
        line=dict(color='#1f77b4', width=2)
    ))
    
    # 2. Forecast Data
    fig.add_trace(go.Scatter(
        x=forecast_df['Date'], 
        y=forecast_df['Prediction'],
        mode='lines+markers', 
        name='Future Prediction',
        line=dict(color='#ff7f0e', width=2, dash='dash')
    ))
    
    # 3. Confidence Interval
    if 'Lower' in forecast_df.columns:
        fig.add_trace(go.Scatter(
            x=forecast_df['Date'], y=forecast_df['Upper'],
            mode='lines', line=dict(width=0),
            showlegend=False, hoverinfo='skip'
        ))
        fig.add_trace(go.Scatter(
            x=forecast_df['Date'], y=forecast_df['Lower'],
            mode='lines', line=dict(width=0),
            fill='tonexty', fillcolor='rgba(255, 127, 14, 0.2)',
            name='Confidence Interval'
        ))

    fig.update_layout(
        title=title,
        xaxis_title="Date",
        yaxis_title="Sales",
        template="plotly_white",
        hovermode="x unified",
        legend=dict(yanchor="top", y=0.99, xanchor="left", x=0.01)
    )
    return fig

def plot_heatmap(df):
    # Aggregate by Day of Week and Store
    pivot = df.groupby(['Store', 'DayOfWeek'])['Sales'].mean().reset_index()
    
    # Sort days correctly
    days_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    pivot['DayOfWeek'] = pd.Categorical(pivot['DayOfWeek'], categories=days_order, ordered=True)
    pivot = pivot.sort_values('DayOfWeek')
    
    fig = px.density_heatmap(
        pivot, 
        x='DayOfWeek', 
        y='Store', 
        z='Sales', 
        title="Average Sales Heatmap",
        color_continuous_scale='Viridis'
    )
    return fig