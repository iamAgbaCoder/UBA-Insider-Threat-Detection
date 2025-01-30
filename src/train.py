from sklearn.ensemble import IsolationForest
from preprocess import load_data, preprocess_data
import pickle  # To save the trained model

def train_model(features):
    """Train the Isolation Forest model."""
    model = IsolationForest(contamination=0.1, random_state=42)
    model.fit(features)
    return model

if __name__ == "__main__":
    # Load and preprocess data
    logs = load_data("../data/user_logs.csv")
    features, logs_with_features = preprocess_data(logs)

    # Train the model
    model = train_model(features)

    # Save the model
    with open("../models/anomaly_detection_model.pkl", "wb") as f:
        pickle.dump(model, f)

    print("Model trained and saved successfully!")


# import pandas as pd
# import matplotlib.pyplot as plt
# from sklearn.ensemble import IsolationForest
# from preprocess import load_data, preprocess_data
# import pickle  # For saving the trained model
#
# def train_model(features):
#     """Train the Isolation Forest model."""
#     model = IsolationForest(contamination=0.1, random_state=42)
#     model.fit(features)
#     return model
#
# def plot_anomalies(logs_with_features, anomaly_scores):
#     """Plot the session anomalies with Matplotlib."""
#     logs_with_features['anomaly_score'] = anomaly_scores
#     logs_with_features['anomaly'] = [1 if score == -1 else 0 for score in anomaly_scores]
#
#     # Filter out anomalies
#     anomalies = logs_with_features[logs_with_features['anomaly'] == 1]
#
#     # Plot the anomalies
#     plt.figure(figsize=(10, 6))
#     plt.scatter(logs_with_features['timestamp'], logs_with_features['session_duration'], label='Normal Sessions', color='blue')
#     plt.scatter(anomalies['timestamp'], anomalies['session_duration'], label='Anomalous Sessions', color='red', marker='x')
#
#     plt.title('Session Duration Anomalies')
#     plt.xlabel('Timestamp')
#     plt.ylabel('Session Duration (minutes)')
#     plt.legend()
#     plt.xticks(rotation=45)
#     plt.tight_layout()
#     plt.show()
#
# if __name__ == "__main__":
#     # Load and preprocess data
#     logs = load_data("../data/user_logs.csv")
#     features, logs_with_features = preprocess_data(logs)
#
#     # Train the model
#     model = train_model(features)
#
#     # Predict anomaly scores
#     anomaly_scores = model.predict(features)
#
#     # Plot anomalies
#     plot_anomalies(logs_with_features, anomaly_scores)
#
#     # Save the model
#     with open("../models/anomaly_detection_model.pkl", "wb") as f:
#         pickle.dump(model, f)
#
#     print("Model trained, anomalies plotted, and saved successfully!")
