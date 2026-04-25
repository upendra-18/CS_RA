import streamlit as st
import pickle
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(page_title="Retention Engine", layout="wide")

# -------------------------
# LOAD MODEL
# -------------------------
with open('model/final_model.pkl', 'rb') as f:
    model = pickle.load(f)

# -------------------------
# SESSION HISTORY
# -------------------------
if "history" not in st.session_state:
    st.session_state.history = []

# -------------------------
# STYLING
# -------------------------
st.markdown("""
<style>
.card {
    padding: 20px;
    border-radius: 12px;
    background-color: #1e1e1e;
    margin-bottom: 15px;
}
.metric {
    font-size: 22px;
    font-weight: bold;
}
.green {color: #00c853;}
.orange {color: #ff9100;}
.red {color: #ff1744;}
</style>
""", unsafe_allow_html=True)

st.title("📊 Customer Retention Engine")

# -------------------------
# SEGMENTED CONTROL
# -------------------------
customer_type = st.segmented_control(
    "Customer Type",
    ["One Order", "Multiple Orders"]
)

# -------------------------
# LOGIC FUNCTIONS
# -------------------------
def one_order_logic(row):

    score = 0
    if row['amount'] > 200: score += 2
    if row['review_score'] >= 4: score += 2
    if row['is_late'] == 0: score += 1
    if row['is_boleto'] == 0: score += 1

    bucket = 'Potential' if score >= 3 else 'Low Intent'
    days = row['days_since_order']

    if bucket == 'Potential':
        if days <= 3:
            return "No Action", "Wait"
        elif days <= 7:
            return "Recommendation", "Show similar products"
        elif days <= 14:
            return "Discount", "Offer 10% coupon"
        else:
            return "Urgency", "Last chance offer"
    else:
        if days <= 10:
            return "Reminder", "Soft engagement"
        else:
            return "Drop", "No action"

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
        action = 'Strong Retention (Voucher)'
    elif risk == 'Medium Risk':
        action = 'Engagement Email'
    else:
        action = 'No Action'

    return value, risk, action

# -------------------------
# INPUT UI
# -------------------------
data = {}

col1, col2 = st.columns(2)

# ---------- 1 ORDER ----------
if customer_type == "One Order":

    with col1:
        data['amount'] = st.number_input("Order Amount (₹)", 0.0)
        data['review_score'] = st.slider("Review Score (1–5)", 1, 5)
        data['days_since_order'] = st.number_input("Days Since Order (days)", 0)

    with col2:
        data['is_late'] = st.selectbox("Late Delivery (0/1)", [0,1])
        data['is_boleto'] = st.selectbox("Boleto Payment (0/1)", [0,1])

    data['total_orders'] = 1

# ---------- MULTI ORDER ----------
else:

    with col1:
        data['total_orders'] = st.number_input("Total Orders", 2)
        data['monetary'] = st.number_input("Total Spend (₹)", 0.0)
        data['avg_order_value'] = st.number_input("Avg Order Value (₹)", 0.0)
        data['avg_time_between_orders'] = st.number_input("Avg Gap (days)", 0.0)

    with col2:
        data['late_ratio'] = st.number_input("Late Ratio (0–1)", 0.0, 1.0)
        data['cancel_count'] = st.number_input("Cancel Count", 0)
        data['late_count'] = st.number_input("Late Count", 0)
        data['avg_review_score'] = st.number_input("Avg Review (1–5)", 0.0, 5.0)
        data['order_value_std'] = st.number_input("Order Std Dev (₹)", 0.0)

# -------------------------
# PREDICT
# -------------------------
if st.button("🚀 Analyze Customer"):

    # ---------- 1 ORDER ----------
    if customer_type == "One Order":

        action, message = one_order_logic(data)

        st.markdown(f"""
        <div class="card">
            <div class="metric">Action: {action}</div>
            <p>{message}</p>
        </div>
        """, unsafe_allow_html=True)

    # ---------- MULTI ORDER ----------
    else:

        df = pd.DataFrame([data])

        # feature engineering
        df['recency_ratio'] = 1 / (df['avg_time_between_orders'] + 1)
        df['order_consistency'] = 1 / (df['order_value_std'] + 1)
        df['experience_score'] = (
            df['avg_review_score']
            - (df['late_ratio'] * 2)
            - (df['cancel_count'] * 0.5)
        )
        df['bad_experience'] = df['late_count'] + df['cancel_count']
        df['value_density'] = df['monetary'] / (df['total_orders'] + 1)
        df['engagement_score'] = df['total_orders'] / (df['avg_time_between_orders'] + 1)
        df['risk_score'] = df['late_ratio'] * df['cancel_count']
        df['review_std_proxy'] = abs(df['avg_review_score'] - 3)
        df['gap_trend'] = 0

        features = [
            'total_orders','monetary','avg_order_value','late_ratio','cancel_count',
            'late_count','avg_time_between_orders','avg_review_score','order_value_std',
            'recency_ratio','order_consistency','experience_score','bad_experience',
            'value_density','engagement_score','risk_score','review_std_proxy','gap_trend'
        ]

        df = df[features]

        # model
        proba = model.predict_proba(df)[0][1]
        value, risk, action = multi_order_logic(data, proba)

        # store history
        st.session_state.history.append(proba)

        # gauge
        fig = go.Figure(go.Indicator(
            mode="gauge+number",
            value=proba,
            title={'text': "Churn Risk"},
            gauge={
                'axis': {'range': [0, 1]},
                'steps': [
                    {'range': [0, 0.3], 'color': "green"},
                    {'range': [0.3, 0.6], 'color': "orange"},
                    {'range': [0.6, 1], 'color': "red"}
                ]
            }
        ))

        colA, colB = st.columns(2)

        with colA:
            st.plotly_chart(fig, use_container_width=True)

        with colB:
            st.markdown(f"""
            <div class="card">
                <div class="metric">Value: {value}</div>
                <div class="metric">Risk: {risk}</div>
                <div class="metric">Action: {action}</div>
            </div>
            """, unsafe_allow_html=True)

# -------------------------
# HISTORY
# -------------------------
if st.session_state.history:
    st.subheader("📈 Prediction History")
    st.line_chart(st.session_state.history)