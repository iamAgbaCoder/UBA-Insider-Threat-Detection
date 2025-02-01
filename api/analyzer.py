import pandas as pd
import joblib
from flask import Blueprint, request, jsonify
from werkzeug.utils import secure_filename
import os

# Load trained anomaly detection model
model_path = "C:\\Users\\Oluwademilade\\Desktop\\dev\\UBA-threat-detection\\models\\anomaly_detection_model.pkl"
model = joblib.load(model_path)

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import IsolationForest

# Define possible column name variations
COLUMN_MAPPING = {
    "timestamp": ["timestamp", "time", "date_time", "activity_timestamp"],
    "session_duration": ["session_duration", "duration", "time_spent"],
    "failed_logins": ["failed_logins", "status", "login_attempts"],
    "resource_access_count": ["resource_access_count", "page_views", "resource_used"],
    "is_admin": ["is_admin", "admin_flag", "role_admin"],
    "ip_address": ["ip_address", "source_ip", "client_ip"],
    "user_id": ["user_id", "id", "gaia_id"],
    "username": ["username", "user_name", "account_name"],
    "email": ["email", "user_email", "contact_email"],
    "device_type": ["device_type", "device", "user_device"],
    "location": ["location", "geo_location", "user_location"],
    "action": ["action", "user_action", "activity_type"],
}


def load_file(file_path):
    """Load the log data from a CSV file."""
    data = pd.read_csv(file_path, dtype=str)  # Load everything as string to prevent parsing errors
    return data

def map_columns(df):
    """Map columns dynamically based on predefined alternatives."""
    mapped_columns = {}
    for key, possible_names in COLUMN_MAPPING.items():
        for name in possible_names:
            if name in df.columns:
                mapped_columns[key] = name
                break  # Stop at the first match
    print(f"Matched columns: {mapped_columns}")
    return mapped_columns

def normalize_column_names(df):
    """Normalize column names to lowercase and replace spaces with underscores."""
    df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")
    return df

def preprocess_data(df):
    """Preprocess the log data and return available features for modeling."""
    mapped_columns = map_columns(df)

    # Convert timestamp to UNIX time if available
    if "timestamp" in mapped_columns and mapped_columns["timestamp"] in df.columns:
        df[mapped_columns["timestamp"]] = pd.to_datetime(df[mapped_columns["timestamp"]], errors='coerce')
        df[mapped_columns["timestamp"]] = df[mapped_columns["timestamp"]].astype(int) // 10**9  # Convert to UNIX time

    # Convert IP addresses to string
    if "ip_address" in mapped_columns and mapped_columns["ip_address"] in df.columns:
        df[mapped_columns["ip_address"]] = df[mapped_columns["ip_address"]].astype(str)

    # Select only valid numerical features
    available_features = [mapped_columns[key] for key in mapped_columns if key != "ip_address"]

    # Convert numerical columns to float, handling errors
    for feature in available_features:
        df[feature] = pd.to_numeric(df[feature], errors='coerce')

    # Handle missing values
    df.fillna(0, inplace=True)

    # Standardize numeric features
    scaler = StandardScaler()
    scaled_features = scaler.fit_transform(df[available_features])

    return scaled_features, df, available_features

def analyze_file(filepath):
    """Processes uploaded logs, applies model, and returns anomaly scores."""
    df = load_file(filepath)
    df = normalize_column_names(df)

    # Preprocess data
    X_scaled, df, available_features = preprocess_data(df)

    # Train Isolation Forest Model
    # model = IsolationForest(contamination=0.05, random_state=42)
    model.fit(X_scaled)

    # Make predictions
    df["anomaly_score"] = model.predict(X_scaled)

    # Extract anomalies
    anomalies = df[df["anomaly_score"] == -1].to_dict(orient="records")
    print("Anomalies detected:", anomalies)

    return anomalies

def plot_anomalies(anomalies):
    """Plots a graph of anomalies detected in user session logs."""
    if not anomalies:
        print("No anomalies detected.")
        return

    df = pd.DataFrame(anomalies)

    # Convert timestamp to datetime for plotting
    if "timestamp" in df.columns:
        df["timestamp"] = pd.to_datetime(df["timestamp"], errors='coerce')

    # Sort for proper visualization
    df = df.sort_values("timestamp")

    # Plot anomalies
    plt.figure(figsize=(12, 6))
    # print(df.index)
    sns.scatterplot(x=df["timestamp"], y=df.index, hue=df["anomaly_score"], palette={-1: "red", 1: "blue"})

    plt.xlabel("Timestamp")
    plt.ylabel("Index")
    plt.title("Anomaly Detection in User Sessions")
    plt.xticks(rotation=45)
    plt.legend(title="Anomaly Score", labels=["Anomaly", "Normal"])
    plt.grid(True)
    plt.show()

# Example usage
# anomalies = analyze_file("C:\\Users\\Oluwademilade\\Desktop\\dev\\UBA-threat-detection\\data\\user_session_logs.csv")
# plot_anomalies(anomalies)
