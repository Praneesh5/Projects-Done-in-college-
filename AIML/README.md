# Model Interpretability in Clinical Machine Learning

## Using SHAP and LIME to Ensure Explainable AI in Healthcare

A production-quality Windows desktop application for heart disease prediction with full model interpretability using SHAP and LIME.

---

## Features

- **Patient Prediction** — 13-field clinical input form with validation, risk gauge, and recommendations
- **SHAP Analysis** — 5 plot types (Summary, Bar, Waterfall, Force, Dependence) with plain-English explanations
- **LIME Analysis** — Local explanations with feature weight table and contribution chart
- **Model Performance** — Accuracy, Precision, Recall, F1, ROC AUC, Confusion Matrix, ROC Curve
- **PDF Reports** — Professional clinical reports with all predictions and interpretations
- **Export Options** — PDF, PNG images, CSV data export
- **Modern UI** — Microsoft Fluent Design-inspired interface with CustomTkinter

## Tech Stack

| Component | Technology |
|---|---|
| Language | Python 3.12 |
| UI Framework | CustomTkinter + ttkbootstrap |
| ML Model | GradientBoostingClassifier (scikit-learn) |
| Interpretability | SHAP (TreeExplainer) + LIME |
| Visualization | Matplotlib |
| PDF Reports | ReportLab |
| Packaging | PyInstaller |

## Dataset

UCI Heart Disease Dataset (Cleveland) — 302 patients, 13 clinical features, binary classification.

---

## Setup Instructions

### 1. Clone / Download the Project

```bash
cd c:\Users\prane\PycharmProjects\AIML
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Train the Model

Run this **once** to generate model artifacts:

```bash
python train_model.py
```

This creates the following files in `models/`:
- `model.joblib` — Trained GradientBoostingClassifier
- `scaler.joblib` — Fitted StandardScaler
- `X_test.joblib`, `y_test.joblib` — Test data for metrics
- `X_train.joblib` — Training data for SHAP background
- `feature_names.joblib` — Feature column names

### 4. Launch the Application

```bash
python main.py
```

---

## Building an Executable (Windows)

```bash
pyinstaller --onefile --windowed --add-data "models;models" --add-data "heart_cleaned.csv;." --name HealthcareAI main.py
```

The executable will be in `dist/HealthcareAI.exe`.

> **Note:** When using `--onefile`, the `models/` directory and `heart_cleaned.csv` must be bundled using `--add-data`.

---

## Project Structure

```
AIML/
├── main.py                    # Application entry point
├── train_model.py             # One-time model training script
├── heart_cleaned.csv          # Cleaned dataset
├── requirements.txt           # Python dependencies
├── README.md                  # This file
│
├── core/                      # Backend logic
│   ├── __init__.py
│   ├── utils.py               # Logging, validation, feature mappings
│   ├── model_loader.py        # Singleton model loader
│   ├── predict.py             # Prediction engine
│   ├── shap_explainer.py      # SHAP analysis
│   ├── lime_explainer.py      # LIME analysis
│   ├── charts.py              # Matplotlib chart factories
│   └── report_generator.py    # PDF report generation
│
├── gui/                       # User interface
│   ├── __init__.py
│   ├── app.py                 # Main application window
│   ├── theme.py               # Design system (colors, fonts)
│   ├── components.py          # Reusable widgets
│   └── pages/
│       ├── __init__.py
│       ├── dashboard.py       # Dashboard overview
│       ├── prediction.py      # Patient prediction form
│       ├── performance.py     # Model metrics & charts
│       ├── shap_page.py       # SHAP analysis page
│       ├── lime_page.py       # LIME analysis page
│       ├── reports.py         # Report generation
│       ├── about.py           # Project information
│       └── settings.py        # App settings
│
├── assets/                    # Static assets
│   └── icons/
├── models/                    # Trained model artifacts
└── reports/                   # Generated PDF reports
```

---

## Academic Context

This application supports research on **Explainable AI (XAI) in Healthcare**, demonstrating how machine learning predictions can be made transparent and trustworthy for clinical decision-making.

### Key Concepts

- **SHAP** — Based on Shapley values from cooperative game theory. Provides mathematically grounded feature importance.
- **LIME** — Creates local linear surrogate models to explain individual predictions in an interpretable way.
- **Model Interpretability** — Essential for clinical AI where decisions affect patient health and safety.

---

## License

Academic use only. Developed for educational and research purposes.

## Author

Your Name — Your University Name
