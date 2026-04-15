import pandas as pd

def detect_anomalies(df):
    df['z_score'] = (df['claim_amount'] - df['claim_amount'].mean()) / df['claim_amount'].std()
    df['anomaly'] = df['z_score'].apply(lambda x: 1 if abs(x) > 3 else 0)
    return df