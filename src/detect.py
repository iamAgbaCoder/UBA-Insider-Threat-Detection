import pickle
from preprocess import load_data, preprocess_data

def detect_anomalies(features, model):
    """Use the trained model to detect anomalies."""
    predictions = model.predict(features)  # -1 = anomaly, 1 = normal
    return predictions

if __name__ == "__main__":
    # Load the model
    with open("../models/anomaly_detection_model.pkl", "rb") as f:
        model = pickle.load(f)

    # Load and preprocess data
    logs = load_data("../data/user_logs.csv")
    features, logs_with_features = preprocess_data(logs)

    # Detect anomalies
    logs_with_features['anomaly'] = detect_anomalies(features, model)

    # Print anomalies
    anomalies = logs_with_features[logs_with_features['anomaly'] == -1]
    print("Anomalies detected:")
    print(anomalies)
