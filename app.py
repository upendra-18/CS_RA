from fastapi import FastAPI
import pickle
import pandas as pd
from utils import one_order_logic, multi_order_logic

app = FastAPI()

# load model
with open('model/final_model.pkl', 'rb') as f:
    model = pickle.load(f)

with open('model/feature_names.pkl', 'rb') as f:
    feature_names = pickle.load(f)


@app.post("/predict")
def predict(data: dict):

    df = pd.DataFrame([data])

    # -------------------------
    # 1-ORDER FLOW
    # -------------------------
    if df['total_orders'].iloc[0] == 1:
        result = one_order_logic(df.iloc[0])
        return {
            "type": "1-order",
            "action": result[0],
            "message": result[1]
        }

    # -------------------------
    # MULTI-ORDER FLOW
    # -------------------------
    else:
        X = df[feature_names]
        proba = model.predict_proba(X)[0][1]

        value, risk, action = multi_order_logic(df.iloc[0], proba)

        return {
            "type": "multi-order",
            "value_segment": value,
            "churn_risk": risk,
            "action": action,
            "churn_probability": float(proba)
        }