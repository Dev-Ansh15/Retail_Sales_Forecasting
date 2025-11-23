import xgboost as xgb
import pandas as pd
from sklearn.metrics import mean_squared_error
from utils.feature_engineering import create_time_features, create_lag_features

class XGBoostForecaster:
    def __init__(self):
        self.model = xgb.XGBRegressor(objective='reg:squarederror', n_estimators=1000)
        
    def train(self, df):
        # Prep data
        data = create_time_features(df)
        data = create_lag_features(data)
        
        features = ['DayOfWeek', 'Month', 'Year', 'DayOfYear', 'IsWeekend', 'Holiday', 'Promo', 'Sales_Lag_1', 'Sales_Lag_7']
        X = data[features]
        y = data['Sales']
        
        self.model.fit(X, y)
        self.features = features
        return self.model
        
    def predict(self, days, last_known_data):
        # Recursive forecasting simplified for demo
        future_dates = pd.date_range(start=last_known_data['Date'].max() + pd.Timedelta(days=1), periods=days)
        forecasts = []
        
        # Note: Real recursive forecasting requires updating lags dynamically. 
        # This is a simplified approach using the last known row patterns
        last_row = last_known_data.iloc[-1]
        
        for date in future_dates:
            # Create feature vector (Simplified: Assuming static lags for demo speed)
            feat_vector = pd.DataFrame([{
                'DayOfWeek': date.dayofweek,
                'Month': date.month,
                'Year': date.year,
                'DayOfYear': date.dayofyear,
                'IsWeekend': 1 if date.dayofweek >= 5 else 0,
                'Holiday': 0, # Defaulting future
                'Promo': 0,    # Defaulting future
                'Sales_Lag_1': last_row['Sales'],
                'Sales_Lag_7': last_row['Sales'] # Placeholder
            }])
            
            pred = self.model.predict(feat_vector)[0]
            forecasts.append({'Date': date, 'Prediction': pred})
            
        return pd.DataFrame(forecasts)