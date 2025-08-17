# UBS Segmentation Script

import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
import matplotlib.pyplot as plt

# ==============================
# 1. Load dataset
# ==============================
df = pd.read_csv("ubs_customers.csv")

# Features to use for segmentation
seg_feats = [
    "annual_income_inr",
    "credit_score",
    "debt_to_income",
    "avg_monthly_spend_inr",
    "late_payments_12m",
    "products_owned"
]

X = df[seg_feats].copy()

# Standardize features
scaler = StandardScaler()
Xs = scaler.fit_transform(X)

# ==============================
# 2. Find best k (on a sample for speed)
# ==============================
sample = Xs[np.random.choice(len(Xs), size=2000, replace=False)]
best_k, best_score = None, -1
for k in range(3, 7):   # try 3 to 6 clusters
    km = KMeans(n_clusters=k, n_init=10, random_state=42)
    labels = km.fit_predict(sample)
    score = silhouette_score(sample, labels)
    print(f"k={k}, silhouette={score:.3f}")
    if score > best_score:
        best_k, best_score = k, score

print(f"\nBest k chosen = {best_k} (silhouette={best_score:.3f})")

# ==============================
# 3. Run KMeans on full dataset
# ==============================
km = KMeans(n_clusters=best_k, n_init=20, random_state=42)
df["cluster"] = km.fit_predict(Xs)

# ==============================
# 4. Profile clusters
# ==============================
cluster_profile = df.groupby("cluster")[seg_feats + ["defaulted","churned"]].mean()
cluster_counts = df["cluster"].value_counts().sort_index()

print("\nCluster Counts:\n", cluster_counts)
print("\nCluster Profile (means):\n", cluster_profile)

# ==============================
# 5. Save results
# ==============================
df.to_excel("customers_with_clusters.xlsx", index=False)
cluster_profile.to_excel("cluster_profile.xlsx")
cluster_counts.to_excel("cluster_counts.xlsx")

print("\nFiles saved: customers_with_clusters.xlsx, cluster_profile.xlsx, cluster_counts.xlsx")

# ==============================
# 6. Quick visualization
# ==============================
plt.figure(figsize=(7,6))
for c in sorted(df["cluster"].unique()):
    sub = df[df["cluster"]==c]
    plt.scatter(sub["annual_income_inr"], sub["credit_score"], label=f"Cluster {c}", alpha=0.5, s=20)

plt.xlabel("Annual Income (INR)")
plt.ylabel("Credit Score")
plt.title("UBS Segmentation – Income vs Credit Score")
plt.legend()
plt.tight_layout()
plt.savefig("segmentation_income_vs_score.png")
print("Saved segmentation plot: segmentation_income_vs_score.png")
plt.show()
