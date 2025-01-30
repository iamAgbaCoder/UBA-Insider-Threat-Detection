from fastapi import FastAPI, UploadFile, File
import pandas as pd
import pickle
from preprocess import preprocess_data

app = FastAPI()

# Load the model
with open("../models/anomaly_detection_model.pkl", "rb") as f:
    model = pickle.load(f)

@app.post("/detect/")
async def detect(file: UploadFile = File(...)):
    """Endpoint to upload logs and detect anomalies."""
    # Read CSV file
    data = pd.read_csv(file.file)
    features, logs_with_features = preprocess_data(data)

    # Predict anomalies
    logs_with_features['anomaly'] = model.predict(features)

    # Return anomalies as JSON
    anomalies = logs_with_features[logs_with_features['anomaly'] == -1]
    return anomalies.to_dict(orient="records")
