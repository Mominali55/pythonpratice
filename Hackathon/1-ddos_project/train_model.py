#!/usr/bin/env python3
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report
import joblib
import sys
import os

def train_model():
    input_file = 'data/cicddos2019.csv'
    model_file = 'ddos_model.joblib'
    
    if not os.path.exists(input_file):
        print(f"Error: {input_file} not found.")
        sys.exit(1)

    print(f"Loading data from {input_file}...")
    try:
        # Load data (handling potential large file issues or dtypes if necessary, but standard read_csv for now)
        df = pd.read_csv(input_file)
    except Exception as e:
        print(f"Error reading CSV: {e}")
        sys.exit(1)

    # 2. Clean column names by stripping whitespace
    df.columns = df.columns.str.strip()
    print("Columns cleaned.")

    # 4. Filter the dataset to include 'Benign', 'Syn', and 'UDP' classes
    # Assuming the target column is named 'Label' based on standard CIC-DDoS datasets
    if 'Label' not in df.columns:
        print("Error: 'Label' column not found in dataset.")
        print(f"Available columns: {df.columns.tolist()}")
        sys.exit(1)
        
    target_classes = ['Benign', 'Syn', 'UDP']
    print(f"Filtering for classes: {target_classes}")
    df_filtered = df[df['Label'].isin(target_classes)].copy()
    
    if df_filtered.empty:
        print("Error: No data found for the specified classes.")
        sys.exit(1)

    # 3. Select relevant features
    features = ['Flow Duration', 'Total Fwd Packets', 'Flow IAT Mean', 'Fwd Packet Length Std']
    missing_features = [f for f in features if f not in df_filtered.columns]
    if missing_features:
        print(f"Error: Missing features in dataset: {missing_features}")
        sys.exit(1)
        
    X = df_filtered[features]
    y = df_filtered['Label']
    
    # Handle potential infinity or NaN values
    X = X.replace([np.inf, -np.inf], np.nan)
    X = X.fillna(0)

    # Split data for evaluation (80/20 split)
    print("Splitting data...")
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # 5. Train a RandomForestClassifier
    print("Training RandomForestClassifier...")
    clf = RandomForestClassifier(n_estimators=100, random_state=42, n_jobs=-1)
    clf.fit(X_train, y_train)

    # 6. Save the trained model
    print(f"Saving model to {model_file}...")
    joblib.dump(clf, model_file)

    # 7. Print the classification report
    print("Evaluating model...")
    y_pred = clf.predict(X_test)
    report = classification_report(y_test, y_pred)
    print("\nClassification Report:")
    print(report)

if __name__ == "__main__":
    train_model()
