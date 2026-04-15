import streamlit as st
import pandas as pd
from anomaly_detection import detect_anomalies

# Title
st.title("Healthcare Anomaly Detection")

# ---------------- FILE UPLOAD ----------------
uploaded_file = st.file_uploader("Upload Healthcare Dataset", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)

    st.subheader("Uploaded Data")
    st.write(df.head())

    result = detect_anomalies(df)

    st.subheader("Processed Data")
    st.write(result)

# ---------------- MANUAL INPUT ----------------
st.subheader("Manual Input for Detection")

claim_amount = st.number_input("Enter Claim Amount", min_value=0.0)

if st.button("Check Anomaly"):
    df_manual = pd.DataFrame({'claim_amount': [claim_amount]})
    result_manual = detect_anomalies(df_manual)

    st.subheader("Result")
    st.write(result_manual)