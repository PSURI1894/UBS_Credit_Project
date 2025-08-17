import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import roc_curve, auc, confusion_matrix, classification_report

# ==============================
# 1. Load your CSV
# ==============================
df = pd.read_csv("ubs_customers.csv")

# Features and target
features = [
    "annual_income_inr",
    "credit_score",
    "debt_to_income",
    "avg_monthly_spend_inr",
    "late_payments_12m",
    "products_owned"
]

X = df[features]
y = df["defaulted"]

# ==============================
# 2. Train/test split
# ==============================
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.3, random_state=42, stratify=y
)

# Standardize features
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# ==============================
# 3. Logistic Regression
# ==============================
model = LogisticRegression(max_iter=1000, random_state=42)
model.fit(X_train_scaled, y_train)

# Predictions
proba = model.predict_proba(X_test_scaled)[:,1]
y_pred = (proba >= 0.5).astype(int)

# ==============================
# 4. Evaluation
# ==============================
print("Confusion Matrix:\n", confusion_matrix(y_test, y_pred))
print("\nClassification Report:\n", classification_report(y_test, y_pred))

# ROC Curve
fpr, tpr, _ = roc_curve(y_test, proba)
roc_auc = auc(fpr, tpr)

plt.figure(figsize=(6,6))
plt.plot(fpr, tpr, label=f"Logistic Regression (AUC = {roc_auc:.3f})")
plt.plot([0,1], [0,1], linestyle="--", color="grey")
plt.xlabel("False Positive Rate")
plt.ylabel("True Positive Rate")
plt.title("ROC Curve – Default Prediction")
plt.legend(loc="lower right")
plt.tight_layout()
plt.savefig("roc_curve.png")
plt.show()
print("Saved: roc_curve.png")

# Probability Distribution
plt.figure(figsize=(7,5))
plt.hist(proba, bins=40, color="skyblue", edgecolor="black", alpha=0.7)
plt.axvline(x=0.35, color="orange", linestyle="--", label="Threshold 0.35 (Medium Risk)")
plt.axvline(x=0.50, color="red", linestyle="--", label="Threshold 0.50 (High Risk)")
plt.xlabel("Predicted Default Probability")
plt.ylabel("Number of Customers")
plt.title("Distribution of Predicted Default Probabilities")
plt.legend()
plt.tight_layout()
plt.savefig("probability_distribution.png")
plt.show()
print("Saved: probability_distribution.png")
