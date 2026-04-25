# 🚀 Customer Retention & Churn Intelligence System

> End-to-end **Data → Insights → ML → Strategy → Product (Streamlit)** pipeline  
> Focus: **Retention-first decision system**, not just churn prediction

---

## 📌 Problem Statement

Most e-commerce platforms struggle not with acquiring users—but **retaining them**.

This project answers:

- Who is likely to churn?
- Why are they churning?
- What action should we take?
- Where should we NOT spend resources?

---

## 📊 Dataset

- Brazilian E-commerce Dataset (Olist)
- ~100K orders
- ~96K customers
- Multi-table relational structure:
  - Orders
  - Customers
  - Payments
  - Reviews

---

## 🏗️ Data Pipeline
Raw Tables → Order-Level Dataset → Customer-Level Dataset → ML Dataset

### Key Steps

- Joined multiple tables (orders, payments, reviews)
- Built **order-level features**
- Aggregated to **customer-level behavior**
- Created **RFM + behavioral + risk features**

---

## 🧠 Feature Engineering

### Core Features

- `total_orders`
- `monetary`
- `avg_order_value`
- `late_ratio`
- `cancel_count`
- `avg_time_between_orders`
- `avg_review_score`

---

### Advanced Behavioral Features

- `experience_score`
- `engagement_score`
- `value_density`
- `order_consistency`
- `risk_score`
- `bad_experience`
- `review_std_proxy`
- `gap_trend`

---

## 📈 Deep Business Insights

---

### 🔥 1. Majority of users are NOT worth heavy retention

- ~80%+ users fall into **Low Value / Potential**

**Meaning:**
- Heavy discounts for all users = wasted money

**Recommendation:**
- Focus only on **high-value + at-risk users**

---

### 🔥 2. One-time buyers dominate the system

- Huge proportion of users make only **1 purchase**

**Meaning:**
- Churn prediction becomes trivial but useless

**Recommendation:**
- Separate pipeline:
  - **Repeat prediction instead of churn prediction**
  - Build early conversion strategy

---

### 🔥 3. First 30–90 days decide retention

- Most churn happens early

**Meaning:**
- Waiting too long = lost user

**Recommendation:**
- Trigger interventions:
  - Day 3 → engagement
  - Day 7 → recommendation
  - Day 14 → discount

---

### 🔥 4. Payment behavior signals intent

- Users using **voucher / boleto combos** show different patterns

**Meaning:**
- Payment behavior reflects engagement and seriousness

**Recommendation:**
- Use payment behavior for segmentation

---

### 🔥 5. Late delivery is NOT the main churn driver

- Weak correlation with churn

**Meaning:**
- Logistics alone won’t fix retention

**Recommendation:**
- Focus on:
  - Engagement
  - Personalization
  - Value perception

---

### 🔥 6. Customer experience matters (but not alone)

- Poor reviews + cancellations → higher churn

**Meaning:**
- Experience contributes but doesn’t fully explain churn

**Recommendation:**
- Combine:
  - Experience + engagement + frequency

---

### 🔥 7. Time-gap behavior is critical

- Large gaps between orders → high churn probability

**Meaning:**
- Time inactivity is strongest churn signal

**Recommendation:**
- Monitor **gap patterns**
- Trigger alerts before threshold

---

### 🔥 8. High spend ≠ loyalty

- Some high spenders still churn

**Meaning:**
- Monetary value alone is misleading

**Recommendation:**
- Combine:
  - Spend + frequency + recency

---

### 🔥 9. Behavioral consistency predicts loyalty

- Stable order values → loyal users

**Meaning:**
- Consistency = trust signal

**Recommendation:**
- Prioritize consistent users for retention campaigns

---

### 🔥 10. Not all churn is worth preventing

- Some users:
  - Low spend
  - Low engagement
  - High inactivity

**Meaning:**
- They will churn regardless

**Recommendation:**
- **Do NOT spend retention budget on them**

---

## 🧠 Customer Segmentation (RFM-Based)

Segments:

- **High Value**
- **Loyal**
- **Potential**
- **At Risk**
- **Low Value**

---

### Key Observation
Low Value + Potential ≈ Majority of users

👉 This drives **cost-optimized strategy**

---

## 🤖 Churn Model

### 🎯 Goal

Predict churn **before it happens**

---

### Labeling Strategy
Churn = recency > 75th percentile

---

### Model

- XGBoost
- Optimized for PR-AUC
- Class imbalance handled

---

### Performance

| Metric     | Value |
|-----------|------|
| Recall    | ~0.81 |
| Precision | ~0.28 |
| ROC-AUC   | ~0.71 |
| PR-AUC    | ~0.33 |

---

### Why High Recall?

- Missing a churned customer = lost revenue
- False positives = acceptable (email cost is low)

---

## 🎯 Strategy Engine (MOST IMPORTANT PART)

---

## 🔹 Multi-Order Customers (>1 orders)

### Step 1: Value Segmentation

- High
- Medium
- Low

---

### Step 2: Risk Segmentation

- High Risk
- Medium Risk
- Low Risk

---

### 🔥 Action Matrix

| Value ↓ / Risk → | High Risk                    | Medium Risk         | Low Risk     |
|-----------------|----------------------------|--------------------|-------------|
| High Value      | Voucher + strong retention | Personalized email | Light touch |
| Medium Value    | Small discount             | Reminder           | Passive     |
| Low Value       | Reminder only              | Minimal            | Ignore      |

---

## 🔹 One-Order Customers Strategy

### Key Shift
Don’t predict churn → Predict repeat intent

---

### Scoring System

- High spend → +2
- Good review → +2
- No delay → +1
- No boleto → +1

---

### Buckets

- **Potential**
- **Low Intent**

---

### Action Engine

#### Potential Users

- Day 0–3 → Wait
- Day 3–7 → Recommendations
- Day 7–14 → Discount
- Day 14+ → Urgency

---

#### Low Intent Users

- Early → Soft reminder
- Later → Drop user

---

## 🖥️ Product (Streamlit App)

Features:

- Segmented UI (1-order vs multi-order)
- Real-time churn prediction
- Action recommendation engine
- Probability gauge visualization
- SaaS-style dashboard
- History tracking

---

## 🧩 System Design
User Input → Feature Engineering → Model → Risk Score
↓
Strategy Engine
↓
Action Recommendation

---

## 🚀 Key Takeaways

- Churn prediction alone is not useful
- Retention strategy is the real value
- First purchase → second purchase is critical
- Not all customers are worth saving
- ML must be combined with business logic

---

## 📁 Project Structure
├── data/ 
├── notebooks/ 
├── model/ 
│ ├── final_model.pkl 
├── app/ 
│ └── streamlit_app.py 
├── utils.py 
├── requirements.txt 

---

## ⚡ Future Improvements

- Real-time event tracking
- Time-series churn modeling
- CRM integration
- A/B testing for strategies
- Customer Lifetime Value (CLV)

---

## 💥 Final Statement

> This is not just a churn model.

It is a **decision-making system** that connects:
Data → Behavior → Prediction → Business Action
