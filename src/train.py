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
