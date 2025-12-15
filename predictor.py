# predictor.py
import pandas as pd
import numpy as np
import joblib
import json
from tensorflow.keras.models import load_model

# -------------------------------
# Load saved artifacts
# -------------------------------
model = load_model("models/cnn_cicids_model.h5")
scaler = joblib.load("models/scaler.pkl")
feature_cols = json.load(open("models/feature_columns.json"))
label_encoder = joblib.load("models/label_encoder.pkl")

# -------------------------------
# Preprocess CSV for prediction
# -------------------------------
def preprocess(csv_file):
    """
    Reads a CICFlowMeter CSV, selects numeric features,
    aligns with training feature columns, scales, and reshapes for CNN.
    """
    df = pd.read_csv(csv_file, low_memory=False)
    df.columns = df.columns.str.strip()

    # Keep only numeric columns
    df_numeric = df.select_dtypes(include=[np.number])

    # Align with training features
    df_aligned = df_numeric.reindex(columns=feature_cols, fill_value=0)

    # Scale features
    X_scaled = scaler.transform(df_aligned)

    # Reshape for CNN: (samples, features, 1)
    X_cnn = X_scaled.reshape(X_scaled.shape[0], X_scaled.shape[1], 1)

    return X_cnn, df

# -------------------------------
# Make predictions
# -------------------------------
def predict(csv_file):
    """
    Takes a CSV file path, returns:
    - numeric predictions (0/1)
    - probability scores
    - original dataframe with human-readable Prediction column
    """
    X, raw_df = preprocess(csv_file)

    # Predict probabilities
    probs = model.predict(X, verbose=0)

    # Convert probabilities to 0/1
    preds = (probs > 0.5).astype(int)

    # Map numeric predictions to human-readable labels
    labels = label_encoder.inverse_transform(preds.flatten())

    # Add predictions to dataframe
    raw_df['Prediction'] = labels

    return preds, probs, raw_df

# -------------------------------
# Example usage
# -------------------------------
if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: python3 predictor.py <path_to_csv>")
        sys.exit(1)

    csv_file = sys.argv[1]
    preds, probs, df_pred = predict(csv_file)

    print(f"\n✅ Predictions for {csv_file}:")
    print(df_pred[['Prediction']].head(10))  # show first 10 predictions

