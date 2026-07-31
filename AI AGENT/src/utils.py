"""
Utility functions for the healthcare AI/ML project
"""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import confusion_matrix, roc_curve, auc
import warnings
warnings.filterwarnings('ignore')

def plot_class_distribution(y, title="Class Distribution"):
    """Plot class distribution"""
    plt.figure(figsize=(8, 5))
    unique, counts = np.unique(y, return_counts=True)
    plt.bar(['No Diabetes', 'Diabetes'], counts)
    plt.title(title)
    plt.ylabel('Count')
    plt.savefig(title.replace(' ', '_').lower() + '.png')
    plt.close()
    print(f"✓ {title} plot saved")

def plot_confusion_matrix(y_true, y_pred, model_name="Model"):
    """Plot confusion matrix"""
    cm = confusion_matrix(y_true, y_pred)
    plt.figure(figsize=(8, 6))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues')
    plt.title(f'Confusion Matrix - {model_name}')
    plt.ylabel('True Label')
    plt.xlabel('Predicted Label')
    plt.savefig(f'confusion_matrix_{model_name}.png')
    plt.close()
    print(f"✓ Confusion matrix plot saved for {model_name}")

def plot_roc_curve(y_true, y_proba, model_name="Model"):
    """Plot ROC curve"""
    fpr, tpr, _ = roc_curve(y_true, y_proba)
    roc_auc = auc(fpr, tpr)
    
    plt.figure(figsize=(8, 6))
    plt.plot(fpr, tpr, color='darkorange', lw=2, label=f'ROC curve (AUC = {roc_auc:.3f})')
    plt.plot([0, 1], [0, 1], color='navy', lw=2, linestyle='--', label='Random Classifier')
    plt.xlim([0.0, 1.0])
    plt.ylim([0.0, 1.05])
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')
    plt.title(f'ROC Curve - {model_name}')
    plt.legend(loc="lower right")
    plt.savefig(f'roc_curve_{model_name}.png')
    plt.close()
    print(f"✓ ROC curve plot saved for {model_name}")

def calculate_metrics(y_true, y_pred, y_proba=None):
    """Calculate evaluation metrics"""
    from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
    
    accuracy = accuracy_score(y_true, y_pred)
    precision = precision_score(y_true, y_pred)
    recall = recall_score(y_true, y_pred)
    f1 = f1_score(y_true, y_pred)
    
    metrics = {
        'Accuracy': accuracy,
        'Precision': recall,
        'Recall': recall,
        'F1-Score': f1
    }
    
    if y_proba is not None:
        auc_score = auc(*roc_curve(y_true, y_proba)[:2])
        metrics['AUC-ROC'] = auc_score
    
    return metrics

def analyze_false_negatives(y_true, y_pred, X, feature_names):
    """Analyze false negatives (missed diabetes cases)"""
    false_negatives_idx = np.where((y_true == 1) & (y_pred == 0))[0]
    
    if len(false_negatives_idx) == 0:
        print("✓ No false negatives found!")
        return None
    
    fn_data = X[false_negatives_idx]
    fn_df = pd.DataFrame(fn_data, columns=feature_names)
    
    print(f"\n⚠️  False Negatives (Missed Diabetes Cases): {len(false_negatives_idx)}")
    print("\nStatistics of Missed Cases:")
    print(fn_df.describe())
    
    return false_negatives_idx, fn_df

def print_metrics_report(metrics, model_name="Model"):
    """Print formatted metrics report"""
    print(f"\n{'='*50}")
    print(f"{model_name} - Performance Report")
    print(f"{'='*50}")
    for metric_name, value in metrics.items():
        print(f"{metric_name:15s}: {value:.4f}")
    print(f"{'='*50}\n")

def get_feature_importance_df(feature_names, importances):
    """Create feature importance dataframe"""
    importance_df = pd.DataFrame({
        'Feature': feature_names,
        'Importance': importances
    }).sort_values('Importance', ascending=False)
    
    return importance_df

def plot_feature_importance(feature_names, importances, model_name="Model"):
    """Plot feature importance"""
    importance_df = get_feature_importance_df(feature_names, importances)
    
    plt.figure(figsize=(10, 6))
    plt.barh(importance_df['Feature'], importance_df['Importance'])
    plt.xlabel('Importance')
    plt.title(f'Feature Importance - {model_name}')
    plt.tight_layout()
    plt.savefig(f'feature_importance_{model_name}.png')
    plt.close()
    print(f"✓ Feature importance plot saved for {model_name}")
    
    return importance_df
