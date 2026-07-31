"""
Generate synthetic diabetes dataset for medical AI project
"""
import numpy as np
import pandas as pd
from sklearn.datasets import make_classification

# Set random seed for reproducibility
np.random.seed(42)

# Generate synthetic dataset
n_samples = 1000
n_features = 6

# Create imbalanced dataset (realistic for medical data)
X, y = make_classification(
    n_samples=n_samples,
    n_features=n_features,
    n_informative=4,
    n_redundant=1,
    n_clusters_per_class=2,
    weights=[0.75, 0.25],  # 75% non-diabetic, 25% diabetic
    random_state=42
)

# Create feature names
feature_names = ['Age', 'Blood_Pressure', 'Cholesterol', 'Glucose', 'BMI', 'Family_History']

# Scale features to realistic ranges
age_range = (25, 80)
bp_range = (90, 180)
chol_range = (100, 300)
glucose_range = (70, 200)
bmi_range = (18, 45)
family_range = (0, 1)

X_scaled = np.zeros_like(X, dtype=float)
ranges = [age_range, bp_range, chol_range, glucose_range, bmi_range, family_range]

for i, (feature_range) in enumerate(ranges):
    X_scaled[:, i] = np.interp(X[:, i], [X[:, i].min(), X[:, i].max()], feature_range)

# Create DataFrame
df = pd.DataFrame(X_scaled, columns=feature_names)
df['Diabetes'] = y  # 0: No diabetes, 1: Diabetes

# Add some correlation for realism
df.loc[df['Glucose'] > 125, 'Diabetes'] = 1
df.loc[df['BMI'] > 30, 'Diabetes'] = 1
df.loc[df['Blood_Pressure'] > 140, 'Diabetes'] = 1

# Ensure proper class distribution
df['Diabetes'] = df['Diabetes'].astype(int)

# Save dataset
df.to_csv('diabetes_dataset.csv', index=False)
print(f"Dataset created with {len(df)} samples")
print(f"Class distribution:\n{df['Diabetes'].value_counts()}")
print(f"\nDataset statistics:\n{df.describe()}")
print(f"\nDataset saved to diabetes_dataset.csv")
