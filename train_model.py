import pandas as pd
import numpy as np
import os
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier # <-- ADD THIS IMPORT
from sklearn.metrics import accuracy_score, classification_report
from joblib import dump

print("--- Training and Comparing Models ---")

# --- 1. Configuration & Data Loading ---
DATA_PATH = 'data/phishing_urls.csv'
REPORT_PATH = 'reports/model_comparison_report.txt' 
SCALER_PATH = 'models/scaler.joblib'
MODEL_PATH = 'models/phishblock_model.joblib' 

df = pd.read_csv(DATA_PATH)
df.columns = df.columns.str.strip()

print(f"Loaded data with shape: {df.shape}")


# --- 2. Separate Features and Target ---
X = df.drop(columns=['Result', 'index'])
y = df['Result']


# --- 3. Splitting Data ---
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)
print(f"Data split: Training {X_train.shape}, Testing {X_test.shape}")


# --- 4. Scaling Numerical Features ---
scaler = StandardScaler()
scaler.fit(X_train)
X_train_scaled = scaler.transform(X_train)
X_test_scaled = scaler.transform(X_test)
dump(scaler, SCALER_PATH)
print(f"Fitted Scaler saved to {SCALER_PATH}")


# --- 5. Train & Evaluate Logistic Regression ---
print("\n--- Training Logistic Regression Baseline ---")
lr_model = LogisticRegression(solver='liblinear', random_state=42)
lr_model.fit(X_train_scaled, y_train)
y_pred_lr = lr_model.predict(X_test_scaled)
accuracy_lr = accuracy_score(y_test, y_pred_lr)
report_lr = classification_report(y_test, y_pred_lr, target_names=['Phishing (-1)', 'Legitimate (1)'])

print(f"Accuracy: {accuracy_lr:.4f}")


# --- 6. Train & Evaluate Random Forest ---
print("\n--- Training Random Forest Model ---")
rf_model = RandomForestClassifier(n_estimators=100, random_state=42, n_jobs=-1)
rf_model.fit(X_train_scaled, y_train)
y_pred_rf = rf_model.predict(X_test_scaled)
accuracy_rf = accuracy_score(y_test, y_pred_rf)
report_rf = classification_report(y_test, y_pred_rf, target_names=['Phishing (-1)', 'Legitimate (1)'])

print(f"Accuracy: {accuracy_rf:.4f}")


# --- 7. Compare Models and Save the Best One ---
print("\n--- Model Comparison ---")

# Save a combined report for documentation
with open(REPORT_PATH, 'w') as f:
    f.write("--- Logistic Regression Baseline Results ---\n")
    f.write(f"Accuracy: {accuracy_lr:.4f}\n")
    f.write(report_lr)
    f.write("\n\n--- Random Forest Results ---\n")
    f.write(f"Accuracy: {accuracy_rf:.4f}\n")
    f.write(report_rf)
print(f"Comparison report saved to {REPORT_PATH}")

# Deciding which model is better and saving it
if accuracy_rf > accuracy_lr:
    print("\nRandom Forest is the winner. Saving Random Forest model...")
    dump(rf_model, MODEL_PATH)
else:
    print("\nLogistic Regression is sufficient. Saving Logistic Regression model...")
    dump(lr_model, MODEL_PATH)

print(f"Final model saved to {MODEL_PATH}")
print("\nStronger model trained and best model saved.")