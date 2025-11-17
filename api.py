from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
from joblib import load
import re
from urllib.parse import urlparse
import tldextract

print("--- Starting PhishBlock API (Final Robust Version) ---")

# Initialize the Flask application
app = Flask(__name__)
# Enable Cross-Origin Resource Sharing to allow the extension to connect
CORS(app)

# --- 1. Load the Final, Trained Model and Scaler ---
try:
    # Load the model and scaler trained only on reliable features
    model = load('models/phishblock_model_final.joblib')
    scaler = load('models/scaler_final.joblib')
    print("Final robust model and scaler loaded successfully.")
except Exception as e:
    print(f"CRITICAL ERROR: Could not load model or scaler. Error: {e}")
    model = None
    scaler = None

# --- 2. Feature Extraction Logic ---
def get_reliable_feature_order():
    """Returns the exact list and order of features the final model was trained on."""
    return [
        'having_IPhaving_IP_Address', 'URLURL_Length', 'Shortining_Service',
        'having_At_Symbol', 'double_slash_redirecting', 'Prefix_Suffix',
        'having_Sub_Domain', 'HTTPS_token', 'port', 'Submitting_to_email',
        'Abnormal_URL'
    ]

def extract_features_from_url(url):
    features = {key: 0 for key in get_reliable_feature_order()}
    if not re.match(r'^(https?|ftp)://', url):
        url = 'http://' + url
    try:
        parsed_url = urlparse(url)
        domain_info = tldextract.extract(url)
        hostname = parsed_url.hostname if parsed_url.hostname else ''

        # --- REVERSE-ENGINEERED LOGIC ---
        # I am trying to match the "secret language" of the dataset
        # where '1' often seems to mean "good" or "absent" and '-1' means "bad" or "present".

        features['having_IPhaving_IP_Address'] = 1 if not re.match(r"^\d{1,3}(\.\d{1,3}){3}$", hostname) else -1
        features['URLURL_Length'] = 0 if 54 <= len(url) <= 75 else (1 if len(url) > 75 else -1) # Match good row
        features['Shortining_Service'] = -1 if any(s in hostname for s in ['bit.ly', 'goo.gl', 't.co']) else 1
        features['having_At_Symbol'] = -1 if '@' in url else 1 # Reverse the logic
        features['double_slash_redirecting'] = -1 if url.rfind('//') > 7 else 1 # Reverse the logic
        features['Prefix_Suffix'] = -1 if '-' in domain_info.domain else 1
        subdomain_parts = domain_info.subdomain.split('.')
        if not domain_info.subdomain: features['having_Sub_Domain'] = -1
        elif len(subdomain_parts) <= 2: features['having_Sub_Domain'] = 0
        else: features['having_Sub_Domain'] = 1 # Keeping this logic, but it might be complex
        features['HTTPS_token'] = -1 if 'https' in hostname else 1 # Reverse the logic
        features['port'] = -1 if parsed_url.port and parsed_url.port not in [80, 443] else 1
        features['Submitting_to_email'] = -1 if 'mailto:' in url else 1 # Reverse the logic
        features['Abnormal_URL'] = -1 if domain_info.domain not in hostname else 1 # Reverse the logic

    except Exception as e:
        print(f"Warning: Could not parse URL '{url}'. Error: {e}")
    return pd.DataFrame([features])[get_reliable_feature_order()]

# --- 3. API Endpoint for Prediction ---
@app.route('/predict', methods=['POST'])
def predict():
    if not model or not scaler:
        return jsonify({'error': 'Model or scaler is not available.'}), 503
    try:
        data = request.get_json()
        if not data or 'url' not in data:
            return jsonify({'error': 'Invalid request. "url" key is required.'}), 400
        url = data['url']
        features_df = extract_features_from_url(url)
        scaled_features = scaler.transform(features_df)
        prediction = model.predict(scaled_features)
        result = 'Phishing' if prediction[0] == -1 else 'Legitimate'
        return jsonify({'url': url, 'prediction': result})
    except Exception as e:
        print(f"An unexpected error occurred during prediction: {e}")
        return jsonify({'error': 'An internal server error occurred.'}), 500

# --- 4. Main entry point to run the Flask application ---
if __name__ == '__main__':
    app.run(debug=True, port=5000)