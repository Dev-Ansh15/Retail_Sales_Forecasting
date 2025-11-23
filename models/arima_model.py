from statsmodels.tsa.arima.model import ARIMA
import pandas as pd

class ARIMAForecaster:
    def __init__(self, order=(5,1,0)):
        self.order = order
        self.model_fit = None
        
    def train(self, df):
        # ARIMA requires a univariate series with datetime index
        ts_data = df.set_index('Date')['Sales']
        self.model = ARIMA(ts_data, order=self.order)
        self.model_fit = self.model.fit()
        
    def predict(self, days):
        forecast_res = self.model_fit.get_forecast(steps=days)
        forecast_df = pd.DataFrame({
            'Date': pd.date_range(start=pd.Timestamp.now().date(), periods=days), # Approximation
            'Prediction': forecast_res.predicted_mean.values,
            'Lower': forecast_res.conf_int().iloc[:, 0].values,
            'Upper': forecast_res.conf_int().iloc[:, 1].values
        })
        return forecast_df