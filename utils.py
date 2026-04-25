import pandas as pd
from datetime import datetime

def one_order_logic(row):

    # scoring
    score = 0

    if row['amount'] > 200:  # static threshold (since no df)
        score += 2
    if row['review_score'] >= 4:
        score += 2
    if row['is_late'] == 0:
        score += 1
    if row['is_boleto'] == 0:
        score += 1

    bucket = 'Potential' if score >= 3 else 'Low Intent'

    days = row['days_since_order']

    # action engine
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

    # -------- VALUE SEGMENT --------
    if row['monetary'] > 500 and row['total_orders'] > 3:
        value = 'High'
    elif row['monetary'] > 200:
        value = 'Medium'
    else:
        value = 'Low'

    # -------- CHURN RISK --------
    if proba >= 0.5:
        risk = 'High Risk'
    elif proba >= 0.3:
        risk = 'Medium Risk'
    else:
        risk = 'Low Risk'

    # -------- ACTION --------
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