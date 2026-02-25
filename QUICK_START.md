# 🎯 QUICK START GUIDE - AD/MCI Detection Project

## ONE-PAGE OVERVIEW

### What is this project?
A machine learning system that **detects Mild Cognitive Impairment (MCI)** from patient speech patterns.

**Input**: Interview transcript (.cha file)  
**Output**: Diagnosis prediction (Control vs MCI)  
**Accuracy**: 63% (realistic given limited data)

---

## THE SIMPLE EXPLANATION

### Normal Control vs MCI Patient
```
CONTROL PATIENT                    MCI PATIENT
├─ Speaks fluently                 ├─ More hesitations/pauses
├─ Long clear utterances           ├─ Shorter speech segments
├─ Fast speech rate (279 WPM)      ├─ Slower speech (264 WPM)
└─ Few pauses (1082 total)         └─ More pauses (949 total)
```

The model learns this pattern and applies it to new patients.

---

## THE 6 FEATURES (What the model looks at)

```
1. PAUSE COUNT (most important - 23%)
   How many times does the patient pause?
   Control: ~1082 pauses | MCI: ~949 pauses
   
2. TOTAL SPEECH TIME (20.8%)
   How long does the patient talk?
   Control: ~419 seconds | MCI: ~359 seconds

3. PAUSE-PER-WORD RATIO (17.5%)
   How often does the patient hesitate per word?
   Control: 84.7% | MCI: 85.5%

4. TOTAL PAUSE TIME (14.9%)
   Total silence in the interview?
   Control: ~136 sec | MCI: ~125 sec

5. SPEECH RATE (12.7%)
   Words per minute?
   Control: 279 WPM | MCI: 264 WPM

6. WORD DURATION (11.1%)
   Average word length?
   Control: 0.219s | MCI: 0.225s
```

---

## RESULTS

### 📊 Test Set Performance
```
OVERALL ACCURACY: 63.24%

Control Detection  →  71% (29 out of 41 correct)
MCI Detection      →  52% (14 out of 27 correct)

✅ BETTER at identifying normal speech
❌ HARDER at identifying MCI speech
```

### Why 63% and not higher?
```
Reason #1: Limited data (339 patients total)
           Need 600+ for robust model

Reason #2: Classes overlap
           Some MCI speak like Controls
           Some Controls speak like MCI

Reason #3: Text only (no audio)
           Missing: pitch, tone, prosody variations
           These could add 10-15% accuracy

Reason #4: Imbalanced dataset
           60% Control, 40% MCI
           Model biased toward Control
```

---

## FILE STRUCTURE AT A GLANCE

```
e:\Projects\AD-MCI-detection-using-vocals\

📂 Data Files (Input & Output)
   ├── _training_dataset.csv          ← Main dataset (339 patients)
   ├── training_dataset_TESTING.csv   ← Test set
   └── training_dataset_Bracrest.csv  ← Validation data

📂 Python Scripts (The Code)
   ├── pause_cha_word_by_word.py      ← Parse transcripts
   ├── pause_cha.py                   ← Extract voice segments
   ├── _main_features.py              ← Calculate features ⭐
   ├── random_forest.py               ← Train model
   ├── random_forest.ipynb            ← Interactive notebook ⭐
   └── test_on_new.py                 ← Predict new patients

📂 Data Folders
   ├── Delaware/                      (150+ patients)
   │   ├── Control/                   ← Normal subjects
   │   └── MCI/                       ← MCI subjects
   └── Baycrest/                      (11 AD patients)

📚 Documentation (Reading)
   ├── readme.md                      ← Quick start
   ├── PROJECT_GUIDE.md               ← Full guide
   ├── COMPLETE_ANALYSIS.md           ← Deep analysis
   ├── CODE_CHANGES_DETAILED.md       ← Feature history
   └── FEATURE_ANALYSIS_REPORT.md     ← Statistical breakdown
```

---

## HOW TO RUN (3 EASY STEPS)

### STEP 1: Setup (one-time)
```bash
cd "e:\Projects\AD-MCI-detection-using-vocals"
pip install pandas numpy scikit-learn matplotlib seaborn joblib
```

### STEP 2: View Results (FASTEST - Recommended)
```bash
# Open in Jupyter and run cells manually
jupyter notebook random_forest.ipynb

# OR use VS Code built-in notebook viewer
# (Open random_forest.ipynb directly)
```

### STEP 3: Train Model (Command line)
```bash
python random_forest.py
# Creates: model_artifacts/
#   ├── ad_mci_model.pkl
#   ├── feature_scaler.pkl
#   └── feature_names.pkl
```

---

## WHAT EACH SCRIPT DOES (5-SECOND VERSION)

| Script | Input | Output | Purpose |
|--------|-------|--------|---------|
| **pause_cha_word_by_word.py** | .cha files | Word timings | Parse transcripts |
| **_main_features.py** | Word timings + labels | CSV dataset | Extract 6 features |
| **random_forest.py** | CSV dataset | Trained model | Train classifier |
| **random_forest.ipynb** | CSV dataset | Visualizations | Interactive analysis |
| **test_on_new.py** | New .cha file | Prediction | Diagnose new patient |

---

## EXPECTED OUTPUT EXAMPLE

When you predict on a new patient:

```
Input Patient: John_Doe.cha

EXTRACTED FEATURES:
├─ pause_count:          915
├─ total_speech_time:    385.2 seconds
├─ total_pause_time:     128.5 seconds
├─ mean_word_duration:   0.220 seconds
├─ speech_rate_wpm:      268 words/minute
└─ pause_per_word_ratio: 0.851

MODEL PREDICTION:    MCI (54% confidence)
INTERPRETATION:      Patient shows mild cognitive impairment
ACTION:              Recommend clinical evaluation
```

---

## STATISTICS SUMMARY

### Dataset Composition
```
Total: 339 Patients
├── Control: 206 (60.8%)
└── MCI: 133 (39.2%)

Split: 80% Training (271) + 20% Testing (68)
```

### Model Performance Across Folds
```
Fold 1: 61.8%
Fold 2: 68.5%
Fold 3: 63.0%
Fold 4: 57.4%
Fold 5: 66.7%
─────────────
Average: 63.5% ± 3.9%
```

### Feature Importance
```
📊 Feature Contribution to Decisions:
  pause_count ..................... 23.0% ⭐⭐⭐ Most important!
  total_speech_time ............... 20.8% ⭐⭐⭐
  pause_per_word_ratio ............ 17.5% ⭐⭐
  total_pause_time ................ 14.9% ⭐⭐
  speech_rate_wpm ................. 12.7% ⭐
  mean_word_duration .............. 11.1% ⭐
```

---

## WHAT YOU SHOULD KNOW

### ✅ This model is good for:
- **Screening** patients (preliminary assessment)
- **Research** (studying MCI patterns)
- **Demonstration** of speech analysis concepts

### ❌ This model is NOT good for:
- **Diagnosis** (needs clinical confirmation)
- **Deployment** (needs more validation)
- **Clinical decision** (too many false positives)

### 🚀 To improve accuracy to 75%+:
1. Add audio features (pitch, prosody)
2. Collect more patients (500+)
3. Use deep learning (LSTM)
4. Add demographic factors

---

## COMMON QUESTIONS

**Q: Why only 63% accuracy?**  
A: Classes overlap. Some MCI talk like Controls. Limited dataset.

**Q: Can I test it on new patients?**  
A: Yes! Use test_on_new.py with any patient .cha file.

**Q: Where do I get .cha files?**  
A: From speech/language databases, or transcribe interviews yourself.

**Q: What's a .cha file?**  
A: Standard CHAT format - interview transcript with word timings.

**Q: Is this production-ready?**  
A: No, it's research-grade. Needs more data and validation for clinical use.

**Q: How long to run?**  
A: Training: ~30 seconds. Prediction: <1 second per patient.

---

## RECOMMENDED LEARNING PATH

### 1️⃣ Start Here (5 min)
Read: **readme.md** + **PROJECT_GUIDE.md**

### 2️⃣ See Results (10 min)
Open: **random_forest.ipynb** in Jupyter
Run cells 1-15 step-by-step
See: Feature statistics, confusion matrix

### 3️⃣ Deep Dive (30 min)
Read: **COMPLETE_ANALYSIS.md**
Understand: Statistical foundations, clinical relevance

### 4️⃣ Advanced (60 min)
Read: **CODE_CHANGES_DETAILED.md**
Study: Feature engineering decisions
Modify: Hyperparameters in random_forest.py

### 5️⃣ Experiment (2+ hours)
Run cells 16-22 in notebook
Try: Different models (SVM, Logistic Regression)
Modify: Feature selection, hyperparameters

---

## QUICK REFERENCE

### Keys to Remember
```
🔑 Pause patterns = 40% of the model
🔑 Control speaks MORE than MCI
🔑 63% accuracy is realistic for this data
🔑 Model is better at finding normal speech
🔑 6 features beat 14 weak features
```

### Technical Specs
```
Algorithm: Random Forest (200 trees)
Features: 6 (pause-based metrics)
Patients: 339 (206 Control, 133 MCI)
Test Accuracy: 63.24%
Cross-Val Score: 63.47% ± 3.88%
Framework: scikit-learn, Python 3.9+
```

---

## NEXT STEPS

### 🎯 If you want to understand the code:
1. Open random_forest.ipynb
2. Read PROJECT_GUIDE.md
3. Run cells sequentially

### 🎯 If you want to improve the model:
1. Add more patients to Delaware/
2. Extract audio features from .wav files
3. Try deep learning (LSTM, CNN)
4. Tune hyperparameters

### 🎯 If you want clinical validation:
1. Collect >500 patient dataset
2. Get clinical diagnoses
3. Compare with physician assessment
4. Submit to medical journal

---

## SUPPORT FILES

All `.md` files in the project:
- **readme.md** - Quick start instructions
- **PROJECT_GUIDE.md** - Complete project overview
- **COMPLETE_ANALYSIS.md** - This document + more
- **CODE_CHANGES_DETAILED.md** - Why features were changed
- **FEATURE_ANALYSIS_REPORT.md** - Statistical analysis

All are in: `e:\Projects\AD-MCI-detection-using-vocals`

---

**🎉 You now understand the entire project!**

Questions? Read the .md files or run the Jupyter notebook.
