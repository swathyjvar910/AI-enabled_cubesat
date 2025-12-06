# processing.py
import datetime
import pandas as pd
from sklearn.ensemble import IsolationForest
from telemetry import read_all_packets

def packets_to_dataframe(packets):
    """Convert a list of packet tuples to a pandas dataframe"""
    cols = [
        "timestamp",
        "battery_voltage",
        "temperature",
        "cpu_load",
        "gyro_x",
        "gyro_y",
        "gyro_z",
        "mode"
    ]
    df = pd.DataFrame(packets, columns=cols)

    # human readable time string
    df["time_str"] = df["timestamp"].apply(
        lambda t: datetime.datetime.fromtimestamp(t).strftime("%Y-%m-%d %H:%M:%S")
    )
    return df

def run_ai_on_telemetry(df):
    """Run IsolationForest anomaly detection on telemetry.
       Adds an 'anomaly' column: 0 = normal, 1 = anomaly.
       Returns (df, summary_message)."""
    feature_cols = [
        "battery_voltage",
        "temperature",
        "cpu_load",
        "gyro_x",
        "gyro_y",
        "gyro_z"
    ]
    if len(df) < 10:
        df["anomaly"] = 0
        msg = (
            f"AI analysis skipped: only {len(df)} packet(s) available,"
            "need at least 10."
        )
        return df, msg
    X = df[feature_cols].values
    model = IsolationForest(
        contamination = 0.1, # assume 10% anomalies
        random_state=42
    )
    preds = model.fit_predict(X)    # -1 = anomaly, 1 = normal
    df["anomaly"] = (preds == -1).astype(int)

    num_anomalies = int(df["anomaly"].sum())
    total = len(df)
    msg = f"AI analysis completed: {total} packets processed, {num_anomalies} anomalies detected."
    return df, msg

def process_telemetry():
    """High-level processing:
       - Reads all telemetry
       - Converts to dataframe
       - Runs AI
       Returns (summmary_message, df or None)."""
    packets = read_all_packets()
    if not packets:
        return "No telemetry data available.", None
    df = packets_to_dataframe(packets)
    df, msg = run_ai_on_telemetry(df)
    return msg, df
