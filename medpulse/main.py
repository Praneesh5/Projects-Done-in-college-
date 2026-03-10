# ==========================================
# AI-Based Financial Fraud Detection
# Logistic Regression vs Random Forest vs XGBoost
# ==========================================

import pandas as pd
import numpy as np

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier

from imblearn.over_sampling import SMOTE
from xgboost import XGBClassifier

# ===============================
# 1. Load Dataset
# ===============================

data = pd.read_csv("PS_20174392719_1491204439457_log.csv")

print("Dataset Loaded Successfully")
print("Shape:", data.shape)

# ===============================
# 2. Data Preprocessing
# ===============================

# Drop unnecessary columns
data = data.drop(['nameOrig', 'nameDest'], axis=1)

# Convert categorical column
data = pd.get_dummies(data, columns=['type'], drop_first=True)

# Features & Target
X = data.drop('isFraud', axis=1)
y = data['isFraud']

# ===============================
# 3. Train-Test Split
# ===============================

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

# ===============================
# 4. Handle Imbalance using SMOTE
# ===============================

smote = SMOTE(random_state=42)
X_train_res, y_train_res = smote.fit_resample(X_train, y_train)

print("After SMOTE:", np.bincount(y_train_res))

# ===============================
# 5. Feature Scaling
# ===============================

scaler = StandardScaler()
X_train_res = scaler.fit_transform(X_train_res)
X_test = scaler.transform(X_test)

# ===============================
# Evaluation Function
# ===============================

def evaluate_model(name, y_true, y_pred):
    print("\n", "="*40)
    print(f"{name} Results")
    print("="*40)
    print("Accuracy :", accuracy_score(y_true, y_pred))
    print("Precision:", precision_score(y_true, y_pred))
    print("Recall   :", recall_score(y_true, y_pred))
    print("F1 Score :", f1_score(y_true, y_pred))
    print("ROC-AUC  :", roc_auc_score(y_true, y_pred))


# ===============================
# 6. Logistic Regression
# ===============================

lr = LogisticRegression(max_iter=1000)
lr.fit(X_train_res, y_train_res)
y_pred_lr = lr.predict(X_test)

evaluate_model("Logistic Regression", y_test, y_pred_lr)


# ===============================
# 7. Random Forest
# ===============================

rf = RandomForestClassifier(n_estimators=100, random_state=42)
rf.fit(X_train_res, y_train_res)
y_pred_rf = rf.predict(X_test)

evaluate_model("Random Forest", y_test, y_pred_rf)


# ===============================
# 8. XGBoost (Recommended Best)
# ===============================

xgb = XGBClassifier(
    n_estimators=100,
    learning_rate=0.1,
    max_depth=6,
    use_label_encoder=False,
    eval_metric='logloss',
    random_state=42
)

xgb.fit(X_train_res, y_train_res)
y_pred_xgb = xgb.predict(X_test)

evaluate_model("XGBoost", y_test, y_pred_xgb)


# ===============================
# 9. Final Comparison Table
# ===============================

results = pd.DataFrame({
    "Model": ["Logistic Regression", "Random Forest", "XGBoost"],
    "Accuracy": [
        accuracy_score(y_test, y_pred_lr),
        accuracy_score(y_test, y_pred_rf),
        accuracy_score(y_test, y_pred_xgb)
    ],
    "Precision": [
        precision_score(y_test, y_pred_lr),
        precision_score(y_test, y_pred_rf),
        precision_score(y_test, y_pred_xgb)
    ],
    "Recall": [
        recall_score(y_test, y_pred_lr),
        recall_score(y_test, y_pred_rf),
        recall_score(y_test, y_pred_xgb)
    ],
    "F1 Score": [
        f1_score(y_test, y_pred_lr),
        f1_score(y_test, y_pred_rf),
        f1_score(y_test, y_pred_xgb)
    ]
})

print("\nFinal Comparison Table")
print(results)