# UBS Credit Risk & Customer Segmentation

End-to-end mini-project to (1) predict default risk and (2) segment customers for targeted actions.  
Deliverables include a detailed PDF report and a slide-style PDF for quick review.

---

## 🧭 Project Overview

**Business Goal:** Reduce loan default risk while growing profitable customer segments.  
**Tech Goal:** Build a logistic regression default model and K-Means segments; translate insights into actions.

**Key Outcomes**
- Default model AUC ≈ 0.78 (good separation of low/high risk).
- 4 business-friendly segments: Premier, Gold, Silver, High-Risk.
- Actionable playbooks per segment (limit management, cross-sell, nudges, underwriting).

> See `/reports/UBSCreditRisk&CustomerSegmentationReport.pdf` (detailed)  
> and `/reports/UBS_Credit_Risk_Segmentation_Slides.pdf` (7-slide summary).

---

## 📁 Repository Structure

.
├─ data/
│ └─ default of credit card clients.xlsx # source dataset (keep locally / gitignored if large/sensitive)
├─ reports/
│ ├─ UBSCreditRisk&CustomerSegmentationReport.pdf
│ └─ UBS_Credit_Risk_Segmentation_Slides.pdf
├─ src/
│ └─ ubs_segmentation.py # K-Means segmentation pipeline
├─ outputs/ # generated artifacts
│ ├─ customers_with_clusters.xlsx
│ ├─ cluster_profile.xlsx
│ ├─ cluster_counts.xlsx
│ └─ segmentation_income_vs_score.png
├─ .gitignore
└─ README.md


---

## ⚙️ Setup

### 1) Python
```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS/Linux
source .venv/bin/activate

pip install --upgrade pip
pip install -r requirements.txt
```

## requirements.txt
pandas
numpy
scikit-learn
matplotlib
openpyxl

data/ubs_customers.csv


python src/ubs_segmentation.py

What it does

Loads data/default of credit card clients.xlsx using engine="openpyxl".

Standardizes selected features and samples to find best k via silhouette score.

Fits full K-Means, assigns cluster.

Saves:

outputs/customers_with_clusters.xlsx

outputs/cluster_profile.xlsx (means per cluster incl. risk flags if present)

outputs/cluster_counts.xlsx

outputs/segmentation_income_vs_score.png

Default script expects these columns (or mapped equivalents):

annual_income_inr

credit_score

debt_to_income

avg_monthly_spend_inr

late_payments_12m

products_owned

If you’re using the UCI “Default of Credit Card Clients” schema, map columns accordingly inside src/ubs_segmentation.py (e.g., LIMIT_BAL → annual_income_inr, PAY_0 → late_payments_12m, etc.). Print columns to verify:

print(df.columns.tolist())

🧩 Outputs

Cluster counts: how many customers per segment.

Cluster profile: mean values of features (and defaulted / churned if present).

Scatter plot: Income vs Credit Score colored by segment.

Artifacts are saved under /outputs/.

🛠️ Troubleshooting

Error: SyntaxError in xlrd or “engine not found”
Fix: Use openpyxl explicitly and/or install it

df = pd.read_excel("data/default of credit card clients.xlsx", engine="openpyxl")

pip install openpyxl
# optional: remove legacy xlrd if causing issues
pip uninstall xlrd

KeyError for column names
Columns in the Excel don’t match seg_feats. Inspect and add a rename map:

print(df.columns.tolist())
df = df.rename(columns={
    "LIMIT_BAL": "annual_income_inr",
    "PAY_0": "late_payments_12m",
    # add more mappings as needed
})

## 🗺️ Roadmap

Add default model script (src/default_model.py) with ROC chart + calibration.

Auto-generate a segment KPI table (counts, default rate, churn) into

📄 Reports

Detailed report: reports/UBSCreditRisk&CustomerSegmentationReport.pdf
