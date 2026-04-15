import streamlit as st
import pandas as pd
from anomaly_detection import detect_anomalies

st.title("🏥 Healthcare Anomaly Detection System")

# ---------------- FILE UPLOAD ----------------
uploaded_file = st.file_uploader("Upload CSV", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)

    # 🔥 Limit data for speed
    df = df.head(500)

    # Fix column name
    if 'charges' in df.columns:
        df.rename(columns={'charges': 'claim_amount'}, inplace=True)

    # 🔥 Add extreme values (ensure anomalies)
    extra = pd.DataFrame({
        'claim_amount': [100000, 200000, 500000, 1000000]
    })
    df = pd.concat([df, extra], ignore_index=True)

    # Run anomaly detection
    result = detect_anomalies(df)

    # ---------------- DISPLAY DATA ----------------
    st.subheader("📊 Processed Data (Top 5)")
    st.write(result.head())

    # ---------------- ANOMALIES ----------------
    st.subheader("🚨 Anomalies with Full Details")
    anomalies = result[result['anomaly'] == 1]
    st.write(anomalies.head())

# ---------------- MANUAL INPUT ----------------
st.subheader("✍️ Manual Input")

claim_amount = st.number_input("Enter Claim Amount", min_value=0.0)

if st.button("Check Anomaly"):
    if uploaded_file is not None:

        # 🔍 Search matching records
        matched = df[df['claim_amount'] == claim_amount]

        if not matched.empty:
            st.subheader("📌 Matching Record(s)")
            st.write(matched)
        else:
            st.warning("No exact match found in dataset")

        # 🚨 Anomaly detection
        df_manual = df.copy()
        new_row = pd.DataFrame({'claim_amount': [claim_amount]})
        df_manual = pd.concat([df_manual, new_row], ignore_index=True)

        result_manual = detect_anomalies(df_manual)
        last = result_manual.tail(1)

        st.subheader("📊 Anomaly Result")
        st.write(last)

        if last['anomaly'].values[0] == 1:
            st.error("🚨 Anomaly Detected!")
        else:
            st.success("✅ Normal Transaction")

    else:
        st.warning("⚠️ Please upload dataset first")
