import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
from joblib import dump

print("--- Training Final, Robust Model ---")

# --- 1. Define the features we can reliably extract from a URL string ---
RELIABLE_FEATURES = [
    'having_IPhaving_IP_Address', 'URLURL_Length', 'Shortining_Service',
    'having_At_Symbol', 'double_slash_redirecting', 'Prefix_Suffix',
    'having_Sub_Domain', 'HTTPS_token', 'port', 'Submitting_to_email',
    'Abnormal_URL'
]

# --- 2. Load Data and Select Only Reliable Features ---
df = pd.read_csv('data/phishing_urls.csv')
df.columns = df.columns.str.strip()

X = df[RELIABLE_FEATURES] 
y = df['Result']

print(f"Training model with {len(RELIABLE_FEATURES)} reliable features.")

# --- 3. Split and Scale Data ---
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# --- 4. Train the Final Random Forest Model ---
model = RandomForestClassifier(n_estimators=100, random_state=42, n_jobs=-1)
model.fit(X_train_scaled, y_train)

# --- 5. Evaluate the New Model ---
y_pred = model.predict(X_test_scaled)
accuracy = accuracy_score(y_test, y_pred)
report = classification_report(y_test, y_pred)

print(f"\nNew Model Accuracy: {accuracy:.4f}")
print("This accuracy is based only on URL string features, so it may be slightly lower but is more realistic.")
print(report)

# --- 6. Save the Final Assets ---
dump(model, 'models/phishblock_model_final.joblib')
dump(scaler, 'models/scaler_final.joblib')

print("\n✅ Final, robust model and scaler have been saved.")