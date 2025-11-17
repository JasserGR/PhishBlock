import streamlit as st
import pandas as pd
from joblib import load
import numpy as np

# --- 1. Configuration and Asset Loading ---
st.set_page_config(page_title="PhishBlock Predictor", layout="wide", page_icon="🎣")

# Load the final, robust model and scaler assets
try:
    model = load('models/phishblock_model_final.joblib')
    scaler = load('models/scaler_final.joblib')
except FileNotFoundError:
    st.error("Model assets not found. Please run 'train_final_model.py' to generate the final model and scaler.")
    st.stop()

# --- 2. Application UI ---
st.title("🎣 PhishBlock: Interactive Phishing Predictor")
st.write("""
This application uses a Random Forest model to predict the likelihood of a website being a phishing site. 
**Adjust the features on the left** to see how characteristics associated with phishing affect the model's real-time prediction.
""")
st.markdown("---")

# --- 3. Sidebar for User Input ---
st.sidebar.header("URL Feature Controls")
st.sidebar.write("Adjust the sliders to simulate different URL characteristics.")

# This dictionary will hold the user's feature selections
user_inputs = {}

# The exact order of features the model was trained on
feature_order = [
    'having_IPhaving_IP_Address', 'URLURL_Length', 'Shortining_Service', 'having_At_Symbol',
    'double_slash_redirecting', 'Prefix_Suffix', 'having_Sub_Domain', 'HTTPS_token',
    'port', 'Submitting_to_email', 'Abnormal_URL'
]

# --- Interactive Widgets ---
user_inputs['having_IPhaving_IP_Address'] = st.sidebar.select_slider(
    'URL Contains IP Address', options=[-1, 1], value=-1,
    help="-1: No, 1: Yes (phishy)")

user_inputs['URLURL_Length'] = st.sidebar.select_slider(
    'URL Length', options=[-1, 0, 1], value=-1,
    help="-1: Short (<54 chars), 0: Medium (54-75), 1: Long (>75, phishy)")

user_inputs['Shortining_Service'] = st.sidebar.select_slider(
    'Uses URL Shortener (e.g., bit.ly)', options=[1, -1], value=1,
    help="1: No, -1: Yes (phishy)")

user_inputs['having_At_Symbol'] = st.sidebar.select_slider(
    'Contains "@" Symbol', options=[-1, 1], value=-1,
    help="-1: No, 1: Yes (phishy)")

user_inputs['double_slash_redirecting'] = st.sidebar.select_slider(
    'Contains "//" Redirect', options=[-1, 1], value=-1,
    help="-1: No, 1: Yes (phishy)")

user_inputs['Prefix_Suffix'] = st.sidebar.select_slider(
    'Domain has "-" Prefix/Suffix', options=[1, -1], value=1,
    help="1: No, -1: Yes (phishy)")

user_inputs['having_Sub_Domain'] = st.sidebar.select_slider(
    'Sub-domain Complexity', options=[-1, 0, 1], value=-1,
    help="-1: Simple, 0: Normal, 1: Complex (phishy)")

user_inputs['HTTPS_token'] = st.sidebar.select_slider(
    '"https" in Domain Name', options=[1, -1], value=1,
    help="1: No, -1: Yes (phishy)")

user_inputs['port'] = st.sidebar.select_slider(
    'Uses Non-standard Port', options=[1, -1], value=1,
    help="1: No, -1: Yes (phishy)")

user_inputs['Submitting_to_email'] = st.sidebar.select_slider(
    'Contains "mailto:"', options=[-1, 1], value=-1,
    help="-1: No, 1: Yes (phishy)")

user_inputs['Abnormal_URL'] = st.sidebar.select_slider(
    'Abnormal URL Structure', options=[1, -1], value=1,
    help="1: No, -1: Yes (phishy)")

# --- 4. Prediction Logic ---
# Convert the dictionary of user inputs into a DataFrame with the correct column order
input_df = pd.DataFrame([user_inputs])
input_df = input_df[feature_order]

# Scale the input features using the loaded scaler
scaled_input = scaler.transform(input_df)

# Make a prediction with the loaded model
prediction = model.predict(scaled_input)
prediction_proba = model.predict_proba(scaled_input)

# --- 5. Display the Results ---
st.subheader("Prediction")

# Use columns for a clean dashboard-style layout
col1, col2 = st.columns(2)

with col1:
    if prediction[0] == 1:
        st.success("✅ **LEGITIMATE**")
        st.write("The model predicts this combination of features corresponds to a legitimate website.")
    else:
        st.error("🚨 **PHISHING**")
        st.write("The model predicts this combination of features corresponds to a phishing website.")

with col2:
    st.metric(
        label="Model Confidence",
        value=f"{np.max(prediction_proba) * 100:.2f}%"
    )

st.markdown("---")
st.write("#### Current Feature Configuration Sent to Model")
st.dataframe(input_df)