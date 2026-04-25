import streamlit as st
import pickle
import pandas as pd

st.title("Customer Retention Engine")

# -------------------------
# LOAD MODEL
# -------------------------
with open('model/final_model.pkl', 'rb') as f:
    model = pickle.load(f)

# -------------------------
# LOGIC FUNCTIONS
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

    if row['monetary'] > 500 and row['total_orders'] > 3:
        value = 'High'
    elif row['monetary'] > 200:
        value = 'Medium'
    else:
        value = 'Low'

    if proba >= 0.5:
        risk = 'High Risk'
    elif proba >= 0.3:
        risk = 'Medium Risk'
    else:
        risk = 'Low Risk'

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

total_orders = st.number_input("Total Orders (count)", min_value=1, step=1)

data = {"total_orders": int(total_orders)}

# -------------------------
# 1-ORDER
# -------------------------
if total_orders == 1:

    st.subheader("1-Order Customer Inputs")

    data.update({
        "amount": st.number_input("Order Amount (₹)", min_value=0.0),
        "review_score": st.slider("Review Score (1–5)", 1, 5),
        "is_late": st.selectbox("Was Delivery Late? (0=No, 1=Yes)", [0,1]),
        "is_boleto": st.selectbox("Payment via Boleto? (0=No, 1=Yes)", [0,1]),
        "days_since_order": st.number_input("Days Since Order (days)", min_value=0)
    })

# -------------------------
# MULTI-ORDER
# -------------------------
else:

    st.subheader("Multi-Order Customer Inputs")

    data.update({
        "monetary": st.number_input("Total Spend (₹)", min_value=0.0),
        "avg_order_value": st.number_input("Average Order Value (₹)", min_value=0.0),
        "late_ratio": st.number_input("Late Delivery Ratio (0–1)", min_value=0.0, max_value=1.0),
        "cancel_count": st.number_input("Total Cancellations (count)", min_value=0),
        "late_count": st.number_input("Total Late Deliveries (count)", min_value=0),
        "avg_time_between_orders": st.number_input("Avg Time Between Orders (days)", min_value=0.0),
        "avg_review_score": st.number_input("Avg Review Score (1–5)", min_value=0.0, max_value=5.0),
        "order_value_std": st.number_input("Order Value Std Dev (₹)", min_value=0.0)
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

        # -------------------------
        # FEATURE ENGINEERING
        # -------------------------

        df['recency_ratio'] = 1 / (df['avg_time_between_orders'] + 1)
        df['order_consistency'] = 1 / (df['order_value_std'] + 1)

        df['experience_score'] = (
            df['avg_review_score'] -
            (df['late_ratio'] * 2) -
            (df['cancel_count'] * 0.5)
        )

        df['bad_experience'] = df['late_count'] + df['cancel_count']

        df['value_density'] = df['monetary'] / (df['total_orders'] + 1)

        df['engagement_score'] = df['total_orders'] / (df['avg_time_between_orders'] + 1)

        df['risk_score'] = df['late_ratio'] * df['cancel_count']

        df['review_std_proxy'] = abs(df['avg_review_score'] - 3)

        df['gap_trend'] = 0  # cannot compute from single input

        # -------------------------
        # FINAL FEATURE ORDER
        # -------------------------
        features = [
            'total_orders',
            'monetary',
            'avg_order_value',
            'late_ratio',
            'cancel_count',
            'late_count',
            'avg_time_between_orders',
            'avg_review_score',
            'order_value_std',
            'recency_ratio',
            'order_consistency',
            'experience_score',
            'bad_experience',
            'value_density',
            'engagement_score',
            'risk_score',
            'review_std_proxy',
            'gap_trend'
        ]

        df = df[features]

        # -------------------------
        # MODEL PREDICTION
        # -------------------------
        proba = model.predict_proba(df)[0][1]

        value, risk, action = multi_order_logic(data, proba)

        st.success("Multi-Order Strategy")

        st.write(f"Churn Probability: {proba:.4f}")
        st.write("Customer Value Segment:", value)
        st.write("Risk Level:", risk)
        st.write("Recommended Action:", action)