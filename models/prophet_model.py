from prophet import Prophet
import pandas as pd

class ProphetForecaster:
    def __init__(self):
        self.model = None
        
    def train(self, df, freq='D'):
        """
        df: DataFrame with 'Date', 'Sales', 'Promo'
        freq: 'D', 'W', 'ME' (Month End)
        """
        # 1. Handle Frequency
        if freq == 'M': freq = 'ME'
            
        # 2. Aggregate Data
        # We use 'sum' for sales (total sold) and 'mean' for promo (avg discount)
        df_agg = df.set_index('Date').resample(freq).agg({
            'Sales': 'sum',
            'Promo': 'mean'
        }).reset_index()
        
        # --- FIX: Fill NaNs created by resampling gaps ---
        # If a week has no data, Sales sum is 0, but Promo mean is NaN.
        df_agg['Sales'] = df_agg['Sales'].fillna(0)
        df_agg['Promo'] = df_agg['Promo'].fillna(0)
        
        # 3. Prepare for Prophet
        train_df = df_agg.rename(columns={'Date': 'ds', 'Sales': 'y'})
        
        # 4. Train
        self.model = Prophet(yearly_seasonality=True, weekly_seasonality=True)
        
        # Only add regressor if there is actual variation (not all 0s)
        if train_df['Promo'].sum() > 0:
            self.model.add_regressor('Promo')
            
        self.model.fit(train_df)
        self.freq = freq
        
    def predict(self, periods):
        # 1. Create Future DataFrame
        future = self.model.make_future_dataframe(periods=periods, freq=self.freq, include_history=False)
        
        # 2. Handle Future Regressors
        # If we used Promo in training, we must provide it for future (set to 0)
        if 'Promo' in self.model.extra_regressors:
            future['Promo'] = 0 
            
        # 3. Predict
        forecast = self.model.predict(future)
        
        result = forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].rename(
            columns={'ds': 'Date', 'yhat': 'Prediction', 'yhat_lower': 'Lower', 'yhat_upper': 'Upper'}
        )
        
        # 4. Clip negatives (Sales can't be negative)
        result['Prediction'] = result['Prediction'].clip(lower=0)
        result['Lower'] = result['Lower'].clip(lower=0)
        
        return result