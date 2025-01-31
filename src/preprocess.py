import pandas as pd
from sklearn.preprocessing import StandardScaler

def load_data(file_path):
    """Load the log data from a CSV file."""
    data = pd.read_csv(file_path)
    data['timestamp'] = pd.to_datetime(data['Timestamp'])  # Convert timestamps
    return data

def preprocess_data(data):
    """Preprocess the log data and return features for modeling."""
    # Feature extraction
    # data['is_admin'] = data['is_admin'].astype(int)  # Convert boolean to int

    # Select relevant features
    features = data[['session_duration', 'ip_address', 'status' 'failed_logins', 'resource_access_count', 'is_admin']]

    # Standardize features
    scaler = StandardScaler()
    scaled_features = scaler.fit_transform(features)

    return scaled_features, data

if __name__ == "__main__":
    logs = load_data("../data/user_session_logs.csv")
    features, logs_with_features = preprocess_data(logs)
    print(logs_with_features.head())
