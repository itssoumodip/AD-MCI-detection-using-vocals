from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import shutil
import os
import joblib
import pandas as pd
import numpy as np
try:
    from .features import extract_features_from_patient
except ImportError:
    from features import extract_features_from_patient


app = FastAPI(title="AD/MCI Detection API")

# Configure CORS for Production
origins = [
    "http://localhost:3000",
    "https://neurovoice.vercel.app",  # Example Vercel domain
    "https://*.vercel.app",           # Wildcard for Vercel preview
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # In strict prod, replace with `origins`
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load model artifacts
MODEL_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'model_artifacts')
MODEL_PATH = os.path.join(MODEL_DIR, 'ad_mci_model.pkl')
SCALER_PATH = os.path.join(MODEL_DIR, 'feature_scaler.pkl')
FEATURES_PATH = os.path.join(MODEL_DIR, 'feature_names.pkl')

try:
    print(f"Loading model from {MODEL_PATH}...")
    model = joblib.load(MODEL_PATH)
    scaler = joblib.load(SCALER_PATH)
    feature_cols = joblib.load(FEATURES_PATH)
    print("Model loaded successfully.")
    print(f"Expected features: {feature_cols}")
except Exception as e:
    print(f"Error loading model: {e}")
    model = None
    scaler = None
    feature_cols = []

@app.get("/")
def read_root():
    return {"status": "ok", "message": "AD/MCI Detection API is running"}

@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    if not model:
        raise HTTPException(status_code=500, detail="Model not loaded")
    
    # Save uploaded file temporarily
    temp_dir = "temp_uploads"
    os.makedirs(temp_dir, exist_ok=True)
    temp_file_path = os.path.join(temp_dir, file.filename)
    
    try:
        with open(temp_file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        print(f"Processing file: {temp_file_path}")
        
        # Extract features
        features = extract_features_from_patient(temp_file_path)
        
        if not features:
            raise HTTPException(status_code=400, detail="Could not extract features from the provided file. Ensure it is a valid .cha file with PAR utterances and timing information.")
        
        # Prepare for prediction
        # Ensure features are in the correct order
        feature_values = []
        for col in feature_cols:
            if col in features:
                feature_values.append(features[col])
            else:
                print(f"Warning: Missing feature {col}, using 0")
                feature_values.append(0)
        
        features_array = np.array([feature_values])
        
        # Scale features
        features_scaled = scaler.transform(features_array)
        
        # Predict
        prediction = model.predict(features_scaled)[0]
        probabilities = model.predict_proba(features_scaled)[0]
        
        # Map prediction to label
        # 0: Control, 1: MCI, 2: AD (Assuming mapping from training script)
        # Training script: diagnosis_names = {0: 'Control', 1: 'MCI', 2: 'AD'}
        labels = {0: 'Control', 1: 'MCI', 2: 'AD'}
        predicted_label = labels.get(int(prediction), "Unknown")
        
        confidence = float(max(probabilities))
        
        result = {
            "prediction": predicted_label,
            "confidence": confidence,
            "probabilities": {
                "Control": float(probabilities[0]) if len(probabilities) > 0 else 0,
                "MCI": float(probabilities[1]) if len(probabilities) > 1 else 0,
                "AD": float(probabilities[2]) if len(probabilities) > 2 else 0,
            },
            "features": features
        }
        
        return result

    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        # Clean up temp file
        if os.path.exists(temp_file_path):
            os.remove(temp_file_path)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
