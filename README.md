🚀 Customer Retention & Churn Intelligence System

End-to-end data → insights → ML → business strategy → product (Streamlit) pipeline
Focus: Retention-first decision system, not just churn prediction

📌 Problem Statement

Most e-commerce businesses optimize for customer acquisition, but lose a majority of users after the first purchase.

This project answers:

Who is likely to churn?
Why are they churning?
What action should we take to retain them?
📊 Dataset
Source: Brazilian E-commerce (Olist)
Multi-table relational data:
Orders, Customers, Payments, Reviews
Final dataset:
~100K orders
~96K unique customers
🏗️ Data Pipeline
1. Data Engineering
Merged multiple relational tables into unified dataset
Converted raw logs → order-level dataset
Aggregated into customer-level features
Raw Tables → Order Level → Customer Level → Model Dataset
2. Feature Engineering

Core behavioral signals:

• total_orders
• monetary (total spend)
• avg_order_value
• late_ratio
• cancel_count
• avg_time_between_orders
• avg_review_score

Advanced features (high impact):

• experience_score = reviews - penalties (late + cancel)
• engagement_score = orders / time gap
• value_density = spend / frequency
• order_consistency = inverse std deviation
• risk_score = late_ratio × cancellations
• gap_trend = change in purchase frequency
📈 Key Business Insights
🔥 Insight 1: Retention is the real problem
~80%+ customers are Low Value or Potential users :contentReference[oaicite:1]{index=1}

Meaning:

Strong acquisition
Weak retention

Action:
→ Shift focus from acquisition → retention

🔥 Insight 2: 1-order customers dominate
Majority of users make only ONE purchase :contentReference[oaicite:2]{index=2}

Impact:

Traditional churn modeling becomes less useful

Action:
→ Build separate strategy for first-time users

🔥 Insight 3: Critical retention window
0–90 days after first purchase is crucial :contentReference[oaicite:3]{index=3}

Impact:

Most churn happens early

Action:
→ Trigger campaigns BEFORE 90 days

🔥 Insight 4: Delivery ≠ main churn driver
Late delivery is NOT the main cause of churn :contentReference[oaicite:4]{index=4}

Impact:

Churn is more behavioral than operational

Action:
→ Focus on engagement, not just logistics

🔥 Insight 5: Value segmentation matters
Customers behave very differently across value segments

Impact:

Same retention strategy = wasted money

Action:
→ Personalized retention campaigns

🧠 Customer Segmentation (RFM-based)

Segments:

• High Value → repeat + high spend
• Loyal → repeat moderate users
• Potential → new but promising
• At Risk → inactive repeat users
• Low Value → low spend, inactive

📊 Observation:

Low Value + Potential = ~80%+ of users :contentReference[oaicite:5]{index=5}
🤖 Churn Prediction Model
🎯 Goal

Predict churn before it happens

📌 Labeling Strategy
Churn = recency > 75th percentile

→ Data-driven threshold

⚙️ Model
Algorithm: XGBoost
Optimization: PR-AUC (important for imbalance)
Class balancing: scale_pos_weight
📊 Performance
Recall: 0.81
Precision: 0.28
ROC-AUC: 0.71
PR-AUC: 0.33 :contentReference[oaicite:6]{index=6}

👉 Prioritized recall over precision

Reason:

Missing a churned customer is costly
False positives are acceptable (email campaigns)
🎯 Business Strategy Engine (CORE)
🔹 Multi-Order Customers (>1 orders)
Step 1: Value Segmentation
High | Medium | Low
Step 2: Churn Risk
High Risk | Medium Risk | Low Risk
🔥 Action Matrix
Value ↓ / Risk →	High Risk	Medium Risk	Low Risk
High Value	Voucher + Strong retention	Personalized engagement	Light touch
Medium Value	Small discount	Reminder	Passive
Low Value	Reminder only	Minimal	Ignore
🔹 1-Order Customers (Separate Strategy)

Key idea:

Don’t predict churn → Predict repeat intent
Scoring Logic
+ High order value
+ Good review
+ No late delivery
+ No boleto usage
Buckets
• Potential
• Low Intent
Action Engine
Potential:
  Day 0–3 → Wait
  Day 3–7 → Recommendation
  Day 7–14 → Discount
  Day 14+ → Urgency

Low Intent:
  Early → Soft reminder
  Late → Drop user
🖥️ Product (Streamlit App)

Features:

✔ Segmented UI (1-order vs multi-order)
✔ Real-time churn prediction
✔ Automated action recommendation
✔ Probability gauge visualization
✔ Customer-level decision system
🧩 System Design
User Input → Feature Engineering → Model → Risk Score
            ↓
     Business Rules Engine
            ↓
      Action Recommendation
🚀 Key Takeaways
1. Churn prediction alone is NOT useful
2. Retention strategy is the real value
3. First purchase → second purchase is critical
4. Personalization beats generic campaigns
5. ML + business logic > ML alone
📁 Project Structure
├── data/
├── notebooks/
├── model/
│   ├── final_model.pkl
│   └── feature_names.pkl
├── app/
│   └── streamlit_app.py
├── utils.py
├── requirements.txt
⚡ Future Improvements
• Time-series churn modeling
• Real-time data pipeline
• A/B testing for strategies
• CRM integration
• LTV prediction
💥 Final Statement
This project is not just a churn model.

It is a decision-making system that connects:
Data → Behavior → Prediction → Business Action
