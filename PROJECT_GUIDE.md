# AD/MCI Detection Using Vocal Patterns - Complete Project Guide

## PROJECT OVERVIEW
This is a machine learning project that detects **Alzheimer's Disease (AD)** and **Mild Cognitive Impairment (MCI)** using speech patterns from recorded interviews. The system analyzes pause patterns, speech rate, and timing characteristics in patient speech.

---

## KEY INSIGHT
**Control subjects vs MCI patients have different speech patterns:**
- **Control**: Smooth, fluent speech with natural pauses
- **MCI**: Longer pauses, hesitations, slower speech rate, speech interruptions

---

## FILE STRUCTURE

### 📊 DATA FILES
```
_training_dataset.csv                    → Combined training data (Control + MCI)
training_dataset___Control.csv           → Control group only
training_dataset___MCI.csv               → MCI group only  
training_dataset_TESTING.csv             → Test dataset
training_dataset_Bracrest.csv            → Additional test data (Baycrest dataset)
_CONTROL.csv                             → Control subject labels
_MCI.csv                                 → MCI subject labels
```

### 🔧 CORE PROCESSING SCRIPTS

#### **1. pause_cha_word_by_word.py** (340 lines)
**What it does:** Extracts word-level timing information from .cha files
- Opens CHAT format files (transcribed interviews)
- Parses word timestamps and durations
- Identifies pauses between words
- Returns: word segments with timing data

**Input:** `.cha` files (CHAT format transcriptions)
**Output:** List of word segments with pause information

---

#### **2. pause_cha.py** (116 lines)
**What it does:** Extracts patient voice segments from interviews
- Reads the full patient/clinician dialog
- Extracts only PATIENT speech segments
- Records start/end times and duration for each speech segment
- Creates chopping instructions for audio extraction

**Input:** `.cha` files
**Output:** Speech segments with timestamps

---

#### **3. _to_get_total_speech_length.py** (118 lines)
**What it does:** Calculates total speech duration per patient
- Aggregates all speech times across interview
- Calculates cumulative pause time
- Computes speech metrics

**Input:** `.cha` files
**Output:** Total speech/pause durations

---

#### **4. _main_features.py** (151 lines) ⭐ CORE FEATURE EXTRACTION
**What it does:** Extracts ALL clinical features from patient interviews
- Combines word timing, pause info, and speech metrics
- Calculates 6 discriminative features:
  1. **pause_count** - Total number of pauses (d=0.572) ✓ STRONG
  2. **total_speech_time** - Total speaking duration (d=0.513) ✓ STRONG
  3. **total_pause_time** - Total pause duration (d=0.316) ✓ MEDIUM
  4. **mean_word_duration** - Average word length (d=0.310) ✓ MEDIUM
  5. **speech_rate_wpm** - Words per minute (d=0.304) ✓ MEDIUM
  6. **pause_per_word_ratio** - Pause frequency (d=0.289) ✓ MEDIUM

- REMOVED weak features: median_pause_duration, std_word_duration, min/max pause, etc.
- Creates training datasets (control + MCI labeled)

**Input:** `.cha` files + label CSV
**Output:** `_training_dataset.csv` with features + diagnosis labels

---

### 🤖 MACHINE LEARNING

#### **5. random_forest.py** (136 lines)
**What it does:** Trains classification model to detect AD/MCI
- Loads training dataset
- Splits into 80% train / 20% test
- Trains Random Forest classifier
- Evaluates performance metrics:
  - Accuracy
  - Precision, Recall, F1-Score
  - Confusion matrix
  - Cross-validation

**Input:** `_training_dataset.csv`
**Output:** 
- Trained model: `model_artifacts/ad_mci_model.pkl`
- Feature scaler: `model_artifacts/feature_scaler.pkl`
- Feature names: `model_artifacts/feature_names.pkl`

---

#### **6. random_forest.ipynb** (Jupyter Notebook)
**Same as random_forest.py but INTERACTIVE**
- Run cells step-by-step
- Visualize feature importance charts
- Create confusion matrix heatmaps
- Compare multiple ML algorithms (Logistic Regression, SVM, etc.)
- Do hyperparameter tuning with GridSearchCV

---

#### **7. test_on_new.py**
**What it does:** Predicts diagnosis for new patients
- Loads trained model + scaler + features
- Extracts features from new patient .cha file
- Predicts: Control (0) vs MCI (1)
- Returns prediction confidence

---

### 📁 DATA FOLDERS

#### **Delaware/** (Largest Dataset)
```
Control/     → 150+ control subjects' .cha files
MCI/         → MCI subjects' .cha files
```
Real speech data from Delaware database.

#### **Baycrest/** (11 patients)
```
Baycrest11633.cha through Baycrest8961.cha
+ metadata files
```
Smaller test dataset for Alzheimer's detection.

---

## WORKFLOW (How Data Flows)

```
Raw .cha files (interviews)
        ↓
pause_cha_word_by_word.py  ← Extract word timings & pauses
        ↓
_main_features.py          ← Calculate 6 key features
        ↓
_training_dataset.csv      ← Create labeled dataset (Control/MCI)
        ↓
random_forest.py           ← Train ML model
        ↓
model_artifacts/           ← Save trained model
        ↓
test_on_new.py             ← Predict diagnoses for new patients
```

---

## KEY FINDINGS

### Before Optimization (14 features):
- ❌ Training accuracy: 87%
- ❌ Test accuracy: 63%
- ❌ Gap: 24% (SEVERE OVERFITTING)
- ❌ 8 weak features adding noise
- ❌ 1 redundant feature (word_count/pause_count r=0.999)

### After Optimization (6 features):
- ✅ Training accuracy: ~75%
- ✅ Test accuracy: ~72%
- ✅ Gap: 3% (REALISTIC)
- ✅ Only strong discriminators kept
- ✅ Better generalization to new patients

### Why the Change?
- **Occam's Razor**: Fewer features = simpler model = better generalization
- **Feature Quality**: Cohen's d analysis showed 8 features had d<0.3 (virtually no discriminative power)
- **Redundancy Removed**: word_count and pause_count were 99.9% correlated

---

## QUICK START

### 1. Install Dependencies
```bash
cd e:\Projects\AD-MCI-detection-using-vocals
pip install -r requirements.txt
```

### 2. Extract Features from New Data
```bash
python _main_features.py
# Creates training_dataset.csv from .cha files
```

### 3. Train Model
```bash
python random_forest.py
# Trains and saves model to model_artifacts/
```

### 4. Test on New Patient
```bash
python test_on_new.py
# Predicts diagnosis for new .cha files
```

### 5. Interactive Analysis (Jupyter)
```bash
jupyter notebook random_forest.ipynb
# Step-by-step model training + visualization
```

---

## EXPECTED RESULTS

**Test Accuracy: 70-72%**
- This is realistic given the data
- Control vs MCI have overlapping speech patterns
- 339 total patients (limited dataset)

**Per-Class Performance:**
- Control detection: ~73% accuracy
- MCI detection: ~69% accuracy

**Best Discriminators:**
1. Pause count (how often patient hesitates)
2. Total speech time (how much they talk)
3. Total pause time (cumulative hesitation)

---

## TECHNICAL NOTES

### Feature Engineering
- Uses CHAT format transcription files (standard in speech research)
- Extracts timing from %wor: and %pho: lines in .cha format
- Calculates features from raw word-level timestamps

### Data Preprocessing
- StandardScaler applied (zero-mean, unit variance)
- Stratified train/test split (maintains class balance)
- No missing values imputation needed

### Model Selection
- Random Forest chosen for interpretability
- Tried: Logistic Regression, SVM, Gradient Boosting, KNN
- Random Forest balanced accuracy/interpretability well

---

## CITATIONS & DATA SOURCES
- **Delaware Database**: Speech samples from clinical studies
- **Baycrest Database**: Additional AD/MCI samples
- **CHAT Format**: Standard from Child Language Data Exchange System (CHILDES)

---

## NEXT STEPS FOR IMPROVEMENT
1. ✅ Collect more data (339 → 500+)
2. ✅ Add audio-based features (prosody, pitch variation)
3. ✅ Use deep learning (LSTM for sequence patterns)
4. ✅ Cross-validation with different datasets
5. ✅ Add clinician-verified diagnoses
