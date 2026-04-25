# 🚀 Customer Retention & Churn Intelligence System

> End-to-end **data → insights → ML → business strategy → product (Streamlit)** pipeline  
> Focus: **Retention-first decision system**, not just churn prediction

---

## 📌 Problem Statement

Most e-commerce businesses optimize for **customer acquisition**, but lose a majority of users after the first purchase.

This project answers:

- Who is likely to churn?
- Why are they churning?
- What action should we take to retain them?

---

## 📊 Dataset

- Source: Brazilian E-commerce (Olist)
- ~100K orders
- ~96K unique customers

---

## 🏗️ Data Pipeline

### 1. Data Engineering

- Merged multiple relational tables (orders, customers, payments, reviews)
- Converted raw logs → **order-level dataset**
- Aggregated → **customer-level dataset**
Raw Tables → Order Level → Customer Level → Model Dataset


---

### 2. Feature Engineering

#### Core Features

- `total_orders`
- `monetary`
- `avg_order_value`
- `late_ratio`
- `cancel_count`
- `avg_time_between_orders`
- `avg_review_score`

#### Advanced Features

- `experience_score = reviews - penalties (late + cancel)`
- `engagement_score = orders / time gap`
- `value_density = spend / frequency`
- `order_consistency = 1 / (std + 1)`
- `risk_score = late_ratio × cancellations`
- `gap_trend = purchase interval trend`

---

## 📈 Key Business Insights

### 🔥 1. Retention is the real problem

- ~80%+ users are **Low Value + Potential**
- Strong acquisition, weak retention

**Action:**  
Shift focus → **Retention over Acquisition**

---

### 🔥 2. One-time users dominate

- Majority of customers make only **1 purchase**

**Action:**  
Separate strategy for **first-time users**

---

### 🔥 3. Critical retention window

- Most churn happens within **0–90 days**

**Action:**  
Trigger retention campaigns early

---

### 🔥 4. Delivery is NOT main driver

- Late delivery is NOT the primary cause of churn

**Action:**  
Focus on **engagement + behavior**

---

### 🔥 5. Value segmentation is critical

- Different customers behave differently

**Action:**  
Use **personalized retention strategies**

---

## 🧠 Customer Segmentation (RFM)

Segments:

- **High Value** → repeat + high spend
- **Loyal** → repeat moderate users
- **Potential** → new but promising
- **At Risk** → inactive repeat users
- **Low Value** → low spend, inactive

---

## 🤖 Churn Prediction Model

### 🎯 Goal

Predict churn **before it happens**

---

### 📌 Labeling Strategy
Churn = recency > 75th percentile


---

### ⚙️ Model

- Algorithm: **XGBoost**
- Optimized for: **PR-AUC**
- Handles imbalance using: `scale_pos_weight`

---

### 📊 Performance

| Metric      | Value |
|------------|------|
| Recall     | 0.81 |
| Precision  | 0.28 |
| ROC-AUC    | 0.71 |
| PR-AUC     | 0.33 |

👉 Focus: **High Recall (capture churners)**

---

## 🎯 Business Strategy Engine (CORE)

---

### 🔹 Multi-Order Customers (>1 orders)

#### Value Segmentation

- High
- Medium
- Low

#### Risk Segmentation

- High Risk
- Medium Risk
- Low Risk

---

### 🔥 Action Matrix

| Value ↓ / Risk → | High Risk                         | Medium Risk              | Low Risk        |
|-----------------|----------------------------------|--------------------------|-----------------|
| High Value      | Voucher + strong retention       | Personalized engagement  | Light touch     |
| Medium Value    | Small discount                   | Reminder                 | Passive         |
| Low Value       | Reminder only                    | Minimal                  | Ignore          |

---

### 🔹 One-Order Customers Strategy

Instead of churn prediction → **predict repeat intent**

---

#### Scoring Logic

- High order value
- Good review
- No late delivery
- No boleto usage

---

#### Buckets

- **Potential**
- **Low Intent**

---

#### Action Plan

**Potential Users**
- Day 0–3 → Wait  
- Day 3–7 → Recommendations  
- Day 7–14 → Discount  
- Day 14+ → Urgency  

**Low Intent Users**
- Early → Soft reminder  
- Late → Drop  

---

## 🖥️ Product (Streamlit App)

Features:

- Segmented UI (1-order vs multi-order)
- Real-time churn prediction
- Automated action recommendation
- Probability gauge visualization
- SaaS-style dashboard

---

## 🧩 System Design

User Input → Feature Engineering → Model → Risk Score
↓
Business Logic Engine
↓
Action Recommendation



---

## 🚀 Key Takeaways

- Churn prediction alone is NOT enough
- Retention strategy is the real value
- First purchase → second purchase is critical
- Personalization > generic campaigns
- ML + business logic > ML alone

---

## 📁 Project Structure
├── data/

├── notebooks/

├── model/

│ ├── final_model.pkl

│ └── feature_names.pkl

├── app/

│ └── streamlit_app.py

├── utils.py

├── requirements.txt


---

## ⚡ Future Improvements

- Time-series churn modeling
- Real-time pipeline
- A/B testing
- CRM integration
- LTV prediction

---

## 💥 Final Statement

> This is not just a churn model.  
> It is a **decision-making system** that connects:
Data → Behavior → Prediction → Business Action
