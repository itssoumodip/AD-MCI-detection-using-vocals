import pandas as pd
import numpy as np
import joblib
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix, classification_report
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier

import matplotlib.pyplot as plt
import seaborn as sns
import os

# Set root directory relative to this script
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# The dataset is in the parent directory
TRAINING_CSV = os.path.join(BASE_DIR, '..', '_training_dataset.csv')
MODEL_DIR = os.path.join(BASE_DIR, 'model_artifacts')

def train_model(training_csv=TRAINING_CSV, output_dir=MODEL_DIR):
    """
    Train a Random Forest classifier for AD/MCI detection
    
    Args:
        training_csv: Path to training dataset CSV
        output_dir: Directory to save trained model artifacts
    """
    
    print("="*80)
    print("TRAINING AD/MCI DETECTION MODEL")
    print("="*80)
    
    # Load training data
    if not os.path.exists(training_csv):
        print(f"Error: Training CSV not found at {training_csv}")
        return

    print(f"\nLoading training data from: {training_csv}")
    try:
        df = pd.read_csv(training_csv)
    except Exception as e:
        print(f"Error reading CSV: {e}")
        return
    
    print(f"Total patients: {len(df)}")
    if 'diagnosis_name' in df.columns:
        print(f"\nDiagnosis distribution:")
        print(df['diagnosis_name'].value_counts())
    
    # Separate features and labels
    # Verify required columns exist
    if 'diagnosis' not in df.columns:
        print("Error: 'diagnosis' column missing from dataset")
        return

    feature_cols = [col for col in df.columns if col not in ['patient_id', 'diagnosis', 'diagnosis_name', 'filename']]
    X = df[feature_cols].astype(float)
    y = df['diagnosis'].astype(int)
    
    print(f"\nFeatures used ({len(feature_cols)}):")
    # for i, col in enumerate(feature_cols, 1):
    #     print(f"  {i}. {col}")
    
    # Split data: 80% train, 20% test
    # Stratify is important for imbalanced datasets
    try:
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42, stratify=y
        )
    except ValueError as e:
        print(f"Warning: Stratified split failed (possibly too few samples per class). Using random split. Error: {e}")
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )
    
    print(f"\nData split:")
    print(f"  Training set: {len(X_train)} patients")
    print(f"  Test set: {len(X_test)} patients")
    
    # Scale features
    print("\nScaling features...")
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    # Train Random Forest model
    print("\nTraining Random Forest classifier...")
    model = RandomForestClassifier(
        n_estimators=100,
        max_depth=10,
        random_state=42,
        n_jobs=-1,
        class_weight='balanced'
    )
    model.fit(X_train_scaled, y_train)
    
    # Predictions
    y_test_pred = model.predict(X_test_scaled)
    
    # Evaluation metrics
    print("\n" + "="*80)
    print("MODEL PERFORMANCE")
    print("="*80)
    
    test_acc = accuracy_score(y_test, y_test_pred)
    print(f"Test Accuracy:     {test_acc:.4f}")
    
    # Save model and scaler
    os.makedirs(output_dir, exist_ok=True)
    
    model_path = os.path.join(output_dir, 'ad_mci_model.pkl')
    scaler_path = os.path.join(output_dir, 'feature_scaler.pkl')
    features_path = os.path.join(output_dir, 'feature_names.pkl')
    
    joblib.dump(model, model_path)
    joblib.dump(scaler, scaler_path)
    joblib.dump(feature_cols, features_path)
    
    print(f"\n{'='*80}")
    print("MODEL SAVED")
    print(f"{'='*80}")
    print(f"Model:        {model_path}")
    print(f"Scaler:       {scaler_path}")
    print(f"Features:     {features_path}")

if __name__ == '__main__':
    train_model()
