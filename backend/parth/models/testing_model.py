import numpy as np
import pandas as pd
import joblib

new_entry = {
    "card_no": "9876543210987654",
    "user_location_country": 1,
    "user_location_city": 2,
    "amount": 1000,
    "transaction_hour": 16,
    "transaction_day_of_week": 3,
    "email_domain": 3,
    "avg_transaction_amount": 1.5,
    "city_consistency": 1,
    "country_consistency": 0.9,
    "upi_id": 12345,
    "average_transaction_frequency": 2,
    "transaction_type": 1,
    "transaction_day": 5,
    "transaction_month": 7,
    "transaction_year": 2024
}

new_entry_df = pd.DataFrame([new_entry])
xgb_model = joblib.load('xgb_model.pkl')
scaler = joblib.load('scaler.pkl')

columns = [
    "user_location_country", "user_location_city", "amount",
    "transaction_hour", "transaction_day_of_week", "email_domain",
    "avg_transaction_amount", "city_consistency", "country_consistency",
    "upi_id", "average_transaction_frequency", "transaction_type",
    "transaction_day", "transaction_month", "transaction_year"
]
new_entry_df = new_entry_df[columns]
new_entry_scaled = scaler.transform(new_entry_df)

y_pred_prob = xgb_model.predict_proba(new_entry_scaled)[:, 1]
best_threshold = 0.397  
y_pred = (y_pred_prob > best_threshold).astype(int)

print(f"Predicted probability of fraud: {y_pred_prob[0]}")
print(f"Predicted class: {y_pred[0]}")
