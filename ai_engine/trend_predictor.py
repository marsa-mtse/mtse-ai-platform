# ==========================================================
# MTSE Marketing Engine - Trend Predictor
# ==========================================================

import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def predict_future_trends(historical_data_df, value_column="search_volume", periods=30):
    """
    Predict future trend line based on historical data.
    Takes a dataframe with a timestamp/date index or assumes sequential data.
    """
    if historical_data_df is None or len(historical_data_df) < 5:
        return {
            "status": "error",
            "message": "لا توجد بيانات كافية للتنبؤ (تحتاج 5 نقاط على الأقل)."
        }
        
    try:
        from sklearn.linear_model import LinearRegression
        
        y = historical_data_df[value_column].fillna(0).values.reshape(-1, 1)
        X = np.arange(len(y)).reshape(-1, 1)
        
        # Simple Linear Regression (Can be upgraded to ARIMA/Prophet)
        model = LinearRegression()
        model.fit(X, y)
        
        future_X = np.arange(len(y), len(y) + periods).reshape(-1, 1)
        future_y = model.predict(future_X).flatten()
        
        # Determine trend direction (last actual point vs end of prediction)
        current_val = y[-1][0]
        end_val = future_y[-1]
        
        if end_val > current_val * 1.05:
            trend_type = "تصاعدي بقوة 🚀"
        elif end_val > current_val:
            trend_type = "تصاعدي بطيء 📈"
        elif end_val < current_val * 0.95:
            trend_type = "هبوطي 📉"
        else:
            trend_type = "مستقر ➖"
            
        growth_rate = ((end_val - current_val) / max(current_val, 1)) * 100
        
        return {
            "status": "success",
            "trend_type": trend_type,
            "growth_pct": round(growth_rate, 2),
            "predictions": future_y.tolist(),
            "next_30_days_peak": round(max(future_y), 2)
        }
        
    except Exception as e:
        return {
            "status": "error",
            "message": f"خطأ في خوارزمية التنبؤ: {str(e)}"
        }
