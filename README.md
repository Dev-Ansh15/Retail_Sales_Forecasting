# 📈 Retail Sales Forecasting Engine

Welcome to the Retail Sales Forecasting System! This is an end-to-end data intelligence application built with Streamlit and Facebook Prophet. It empowers business analysts to upload raw sales data, visualize historical trends, and generate accurate future predictions using advanced time-series modeling.

Stop analyzing the past. Start predicting the future. 🚀

---

## 📂 Project Structure

The project uses a modular architecture, separating the UI views, data processing utilities, and the forecasting engine.

```bash
retail-forecasting/
├── app.py                      # Main Streamlit Application Entry Point
├── requirements.txt            # Project Dependencies
├── data/                       # Data storage
│   ├── retail_sales.csv        # Default generated data
│   └── uploaded.csv            # User uploaded data (if any)
├── models/                     # Forecasting Logic
│   ├── __init__.py
│   └── prophet_model.py        # Facebook Prophet Model Wrapper
├── utils/                      # Helper Scripts
│   ├── __init__.py
│   ├── data_loader.py          # Smart CSV Loader & Column Mapping
│   └── visualizations.py       # Plotly Chart Generation
└── views/                      # UI Page Logic
    ├── __init__.py
    ├── dashboard.py            # Executive Summary View
    ├── data_explorer.py        # Raw Data Inspection
    ├── forecasting.py          # Model Training & Prediction UI
    └── factor_analysis.py      # Seasonality & Heatmap Analytics
```

---

## ⚙️ Setup and Installation

Follow these steps to deploy the application locally on your machine.

### 1. Prerequisites

Ensure you have the following installed:

* **Python 3.8+**
* **PIP** (Python Package Installer)

### 2. Environment Setup

**Clone the repository:**
```bash
git clone https://github.com/Dev-Ansh15/Retail_Sales_Forecasting.git
cd Retail_Sales_Forecasting
```

**Create and Activate Virtual Environment:**
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Mac/Linux
python3 -m venv venv
source venv/bin/activate
```

**Install Dependencies:**
```bash
pip install -r requirements.txt
```

### 3. Launch Application

**Start the Streamlit Server:**
```bash
streamlit run app.py
```

**Access the Dashboard:**
Open your browser and go to `http://localhost:8501`.

---

## 🧩 How It Works (Usage)

This system transforms messy, real-world CSV data into actionable forecasts through a 4-step pipeline.

### 1. Data Ingestion & Smart Cleaning

**Upload:** Use the sidebar to upload your Sales CSV (e.g., Superstore Data).

**Auto-Map:** The system automatically detects schema variations (e.g., mapping Order Date to Date and State to Store).

**Encoding Fix:** Automatically handles utf-8 vs latin1 encoding errors common in Excel exports.

### 2. Executive Dashboard

View high-level KPIs: Total Revenue, Average Transaction Value, and Overall Sales Trends.

Filter data dynamically by Store or Product category.

### 3. AI Forecasting (The Engine)

Navigate to the Forecasting tab.

**Select Frequency:** Choose between Daily, Weekly, or Monthly forecasts.

**Resampling Logic:** The system uses intelligent "Month-End" (ME) resampling and fills NaN gaps (empty weeks) to prevent model crashes.

**Prophet Model:** Trains a custom Facebook Prophet model to predict future sales with confidence intervals.

### 4. Factor Analysis

Visualize Seasonality (which months perform best?).

Analyze Promo Impact (how do discounts correlate with sales spikes?).

View Traffic Heatmaps to identify peak shopping days.

---

## 📊 Data Source Guide

This application is designed to be flexible, but it works best with standard retail datasets.

**Primary Source:** [Superstore Sales Dataset (Kaggle)](https://www.kaggle.com/datasets/rohitsahoo/sales-forecasting)

**Required Columns:** The system expects columns logically similar to Date, Sales, Store, and Product.

**Optional Columns:** Discount or Promo (used for regressor analysis).

> **Note:** If you don't have data, the app will automatically generate a synthetic dataset on the first run so you can explore the features immediately.

---

## 🛠 Technical Stack

* **Frontend:** Streamlit (Python-based UI)
* **Data Manipulation:** Pandas, NumPy
* **Forecasting Engine:** Facebook Prophet
* **Visualization:** Plotly Interactive Charts
* **Data Loader:** Custom Python logic for robust CSV parsing

---

## 🛑 Shutting Down

To stop the application, simply press **Ctrl+C** in the terminal where the Streamlit server is running.
