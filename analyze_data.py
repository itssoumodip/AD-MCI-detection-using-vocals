import pandas as pd
import numpy as np

print("\n" + "="*80)
print("TRAINING DATASET ANALYSIS")
print("="*80)

# Load dataset
df = pd.read_csv('_training_dataset.csv')

print(f"\nTotal Patients: {len(df)}")
print(f"Dataset Shape: {df.shape} (patients × features)")

print(f"\n📊 DIAGNOSIS DISTRIBUTION:")
print(df['diagnosis_name'].value_counts())

print(f"\n📋 COLUMNS IN DATASET ({len(df.columns)}):")
for i, col in enumerate(df.columns, 1):
    print(f"  {i:2d}. {col}")

print(f"\n📈 FEATURE STATISTICS:")
feature_cols = [col for col in df.columns if col not in ['patient_id', 'diagnosis', 'diagnosis_name']]
print(df[feature_cols].describe().round(4))

print(f"\n🎯 DIAGNOSIS BREAKDOWN:")
for diagnosis in sorted(df['diagnosis'].unique()):
    diagnosis_name = df[df['diagnosis'] == diagnosis]['diagnosis_name'].iloc[0]
    count = len(df[df['diagnosis'] == diagnosis])
    percentage = (count / len(df)) * 100
    print(f"  {diagnosis_name:10s} (#{diagnosis}): {count:3d} patients ({percentage:5.1f}%)")

print(f"\n✅ Dataset is ready for model training!")
print("="*80 + "\n")
