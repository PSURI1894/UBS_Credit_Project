import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score, classification_report, confusion_matrix

# ==============================
# 1. Load dataset
# ==============================
df = pd.read_csv("ubs_customers.csv")

# ==============================
# 2. Features & target
# ==============================
features = [
    "credit_score", "debt_to_income", "late_payments_12m",
    "annual_income_inr", "has_loan", "loan_amount_inr",
    "existing_customer_years", "products_owned"
]
X = df[features]
y = df["defaulted"]

# ==============================
# 3. Train / Test Split
# ==============================
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.25, random_state=42, stratify=y
)

# ==============================
# 4. Scale + Logistic Regression
# ==============================
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

clf = LogisticRegression(max_iter=500)
clf.fit(X_train_scaled, y_train)

# ==============================
# 5. Predictions & Probabilities
# ==============================
proba = clf.predict_proba(X_test_scaled)[:,1]

# Metrics
roc_auc = roc_auc_score(y_test, proba)
print(f"ROC-AUC: {roc_auc:.3f}")

# Threshold 0.35 (Medium risk) & 0.50 (High risk)
for t in [0.35, 0.50]:
    preds = (proba >= t).astype(int)
    print(f"\nThreshold {t}")
    print("Confusion Matrix:\n", confusion_matrix(y_test, preds))
    print(classification_report(y_test, preds))

# ==============================
# 6. Save predictions
# ==============================
df.loc[X_test.index, "default_probability"] = proba
df.to_excel("customers_with_risk.xlsx", index=False)
print("File saved: customers_with_risk.xlsx")
