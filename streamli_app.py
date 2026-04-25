import streamlit as st
import pickle
import pandas as pd

st.title("Customer Retention Engine")

# -------------------------
# LOAD MODEL
# -------------------------
with open('model/final_model.pkl', 'rb') as f:
    model = pickle.load(f)

with open('model/feature_names.pkl', 'rb') as f:
    feature_names = pickle.load(f)

# -------------------------
# LOGIC FUNCTIONS (from utils.py)
# -------------------------

def one_order_logic(row):

    score = 0

    if row['amount'] > 200:
        score += 2
    if row['review_score'] >= 4:
        score += 2
    if row['is_late'] == 0:
        score += 1
    if row['is_boleto'] == 0:
        score += 1

    bucket = 'Potential' if score >= 3 else 'Low Intent'
    days = row['days_since_order']

    if bucket == 'Potential':
        if days <= 3:
            return ('No Action', 'Wait')
        elif days <= 7:
            return ('Reminder + Recommendations',
                    'You might like these based on your purchase')
        elif days <= 14:
            return ('5-10% Discount',
                    'Exclusive offer just for you!')
        else:
            return ('Urgency Campaign',
                    'Last chance! Offer expiring soon')
    else:
        if days <= 5:
            return ('No Action', 'Wait')
        elif days <= 10:
            return ('Soft Reminder',
                    'Check out trending products')
        elif days <= 20:
            return ('Generic Nudge',
                    'We miss you!')
        else:
            return ('Drop User',
                    'Stop spending resources')


def multi_order_logic(row, proba):

    # VALUE SEGMENT
    if row['monetary'] > 500 and row['total_orders'] > 3:
        value = 'High'
    elif row['monetary'] > 200:
        value = 'Medium'
    else:
        value = 'Low'

    # RISK
    if proba >= 0.5:
        risk = 'High Risk'
    elif proba >= 0.3:
        risk = 'Medium Risk'
    else:
        risk = 'Low Risk'

    # ACTION
    if risk == 'High Risk':
        if value == 'High':
            action = 'Voucher + Strong Retention'
        elif value == 'Medium':
            action = '5% Discount'
        else:
            action = 'Reminder Only'
    elif risk == 'Medium Risk':
        action = 'Engagement Email'
    else:
        action = 'No Action'

    return value, risk, action

# -------------------------
# INPUT UI
# -------------------------

total_orders = st.number_input("Total Orders", min_value=1, step=1)

data = {"total_orders": int(total_orders)}

# -------------------------
# 1-ORDER UI
# -------------------------
if total_orders == 1:

    st.subheader("1-Order Customer Inputs")

    data.update({
        "amount": st.number_input("Order Amount", min_value=0.0),
        "review_score": st.slider("Review Score", 1, 5),
        "is_late": st.selectbox("Late Delivery", [0, 1]),
        "is_boleto": st.selectbox("Boleto", [0, 1]),
        "days_since_order": st.number_input("Days Since Order", min_value=0)
    })

# -------------------------
# MULTI-ORDER UI
# -------------------------
else:

    st.subheader("Multi-Order Customer Inputs")

    data.update({
        "monetary": st.number_input("Total Spend", min_value=0.0),
        "avg_order_value": st.number_input("Avg Order Value", min_value=0.0),
        "late_ratio": st.number_input("Late Ratio", min_value=0.0, max_value=1.0),
        "cancel_count": st.number_input("Cancel Count", min_value=0),
        "late_count": st.number_input("Late Count", min_value=0),
        "avg_time_between_orders": st.number_input("Avg Time Between Orders", min_value=0.0),
        "avg_review_score": st.number_input("Avg Review Score", min_value=0.0, max_value=5.0),
        "order_value_std": st.number_input("Order Value Std", min_value=0.0)
    })

# -------------------------
# PREDICTION
# -------------------------
if st.button("Predict"):

    if total_orders == 1:

        action, message = one_order_logic(data)

        st.success("1-Order Strategy")
        st.write("Action:", action)
        st.write("Message:", message)

    else:

        df = pd.DataFrame([data])

        # ensure correct feature order
        df = df[feature_names]

        proba = model.predict_proba(df)[0][1]

        value, risk, action = multi_order_logic(data, proba)

        st.success("Multi-Order Strategy")

        st.write(f"Churn Probability: {proba:.4f}")
        st.write("Customer Value:", value)
        st.write("Risk Level:", risk)
        st.write("Recommended Action:", action)