"""
Task 3: Statistical Learning for Risk Stratification
Naive Bayes and Logistic Regression for diabetes prediction
"""
import numpy as np
import pandas as pd
from sklearn.naive_bayes import GaussianNB
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, roc_auc_score, roc_curve, auc
from sklearn.metrics import precision_score, recall_score, f1_score
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings('ignore')

class StatisticalLearningModels:
    """
    Naive Bayes and Logistic Regression for medical risk stratification
    """
    
    def __init__(self, feature_names):
        """
        Initialize statistical models
        
        Args:
            feature_names: List of feature names
        """
        self.feature_names = feature_names
        self.nb_model = None
        self.lr_model = None
        self.nb_metrics = None
        self.lr_metrics = None
    
    def train_naive_bayes(self, X_train, y_train):
        """
        Task 3(a): Train Naive Bayes classifier
        
        Args:
            X_train: Training features
            y_train: Training labels
        """
        explanation = """
        NAÏVE BAYES FOR DIABETES PREDICTION
        ==================================
        
        ALGORITHM OVERVIEW:
        • Type: Probabilistic classifier
        • Assumption: Feature independence (naive)
        • Distribution: Gaussian (for continuous features)
        
        MATHEMATICAL FOUNDATION:
        Using Bayes' Theorem:
        P(Diabetes|Features) = P(Features|Diabetes) * P(Diabetes) / P(Features)
        
        ADVANTAGES:
        1. Fast training and prediction
        2. Works well with small datasets
        3. Interpretable probability outputs
        4. Handles missing values gracefully
        5. Linear time complexity
        
        DISADVANTAGES:
        1. Assumes feature independence (often violated)
        2. May underestimate probabilities
        3. Sensitive to feature scaling (partially)
        
        SUITABILITY FOR MEDICAL DATA:
        • Medium-sized datasets: ✓ Excellent
        • Interpretability: ✓ Good (probabilistic outputs)
        • Clinical deployment: ✓ Suitable
        • Performance: Moderate (baseline model)
        """
        print(explanation)
        
        self.nb_model = GaussianNB()
        self.nb_model.fit(X_train, y_train)
        
        print("\n✓ Naive Bayes Model Trained")
        print(f"  Classes: {self.nb_model.classes_}")
        print(f"  Class priors: {self.nb_model.class_prior_}")
        
        return self.nb_model
    
    def train_logistic_regression(self, X_train, y_train):
        """
        Task 3(a): Train Logistic Regression classifier
        
        Args:
            X_train: Training features
            y_train: Training labels
        """
        explanation = """
        LOGISTIC REGRESSION FOR DIABETES PREDICTION
        ===========================================
        
        ALGORITHM OVERVIEW:
        • Type: Linear probabilistic classifier
        • Function: Sigmoid (logistic function)
        • Optimization: Maximum likelihood (gradient descent)
        
        MATHEMATICAL FOUNDATION:
        Sigmoid function: P(y=1|x) = 1 / (1 + e^(-βx))
        
        Log-odds (Logit):
        log(p/(1-p)) = β0 + β1*x1 + β2*x2 + ... + βn*xn
        
        ADVANTAGES:
        1. Probabilistic output (confidence scores)
        2. Linear interpretability (feature coefficients)
        3. Fast training
        4. Handles regularization well
        5. Standard clinical deployment
        
        DISADVANTAGES:
        1. Assumes linear relationship
        2. Sensitive to feature scaling
        3. Poor performance with non-linear patterns
        4. Assumes feature independence
        
        SUITABILITY FOR MEDICAL DATA:
        • Interpretability: ✓ Excellent
        • Clinical acceptance: ✓ Very Good (standard in medicine)
        • Performance: ✓ Good with normalized features
        • Deployment: ✓ Ideal (simple, fast, interpretable)
        """
        print(explanation)
        
        self.lr_model = LogisticRegression(
            random_state=42,
            max_iter=1000,
            solver='lbfgs',
            class_weight='balanced'  # Handle imbalance
        )
        self.lr_model.fit(X_train, y_train)
        
        print("\n✓ Logistic Regression Model Trained")
        print(f"  Intercept: {self.lr_model.intercept_[0]:.6f}")
        print(f"  Coefficients shape: {self.lr_model.coef_.shape}")
        
        return self.lr_model
    
    def evaluate_statistical_models(self, X_test, y_test):
        """
        Task 3(a): Evaluate and compare models
        
        Args:
            X_test: Test features
            y_test: Test labels
        
        Returns:
            Comparison dataframe
        """
        # Naive Bayes evaluation
        y_pred_nb = self.nb_model.predict(X_test)
        y_proba_nb = self.nb_model.predict_proba(X_test)[:, 1]
        
        nb_accuracy = accuracy_score(y_test, y_pred_nb)
        nb_auc = roc_auc_score(y_test, y_proba_nb)
        nb_precision = precision_score(y_test, y_pred_nb)
        nb_recall = recall_score(y_test, y_pred_nb)
        nb_f1 = f1_score(y_test, y_pred_nb)
        
        self.nb_metrics = {
            'Model': 'Naive Bayes',
            'Accuracy': nb_accuracy,
            'Precision': nb_precision,
            'Recall': nb_recall,
            'F1-Score': nb_f1,
            'AUC-ROC': nb_auc
        }
        
        # Logistic Regression evaluation
        y_pred_lr = self.lr_model.predict(X_test)
        y_proba_lr = self.lr_model.predict_proba(X_test)[:, 1]
        
        lr_accuracy = accuracy_score(y_test, y_pred_lr)
        lr_auc = roc_auc_score(y_test, y_proba_lr)
        lr_precision = precision_score(y_test, y_pred_lr)
        lr_recall = recall_score(y_test, y_pred_lr)
        lr_f1 = f1_score(y_test, y_pred_lr)
        
        self.lr_metrics = {
            'Model': 'Logistic Regression',
            'Accuracy': lr_accuracy,
            'Precision': lr_precision,
            'Recall': lr_recall,
            'F1-Score': lr_f1,
            'AUC-ROC': lr_auc
        }
        
        # Print comparison
        print(f"\n{'='*70}")
        print("STATISTICAL MODELS COMPARISON")
        print(f"{'='*70}")
        
        comparison_df = pd.DataFrame([self.nb_metrics, self.lr_metrics])
        print(comparison_df.to_string(index=False))
        
        # Analysis
        print(f"\n{'='*70}")
        print("WHEN TO USE EACH MODEL")
        print(f"{'='*70}")
        
        analysis = """
        NAIVE BAYES:
        • Use when: Fast inference needed, small dataset
        • Advantages: Simple, probabilistic, interpretable
        • Clinical scenario: Emergency triage (speed critical)
        
        LOGISTIC REGRESSION:
        • Use when: Feature coefficients important, linear patterns exist
        • Advantages: Highly interpretable, standard in medicine
        • Clinical scenario: Risk scoring, physician explanation needed
        
        GENERAL RECOMMENDATION:
        • For deployment: LOGISTIC REGRESSION
          Reasons:
          1. Better accuracy in most cases
          2. Standard medical interpretation (odds ratio)
          3. Regulatory compliance (explainability)
          4. Easier integration with clinical workflows
        
        • For comparison: NAIVE BAYES useful as baseline
          Reasons:
          1. Simpler model (Occam's razor)
          2. Good performance/complexity ratio
          3. Handles imbalanced data well
        """
        print(analysis)
        
        return comparison_df
    
    def feature_importance_analysis(self):
        """
        Task 3(b): Feature importance from statistical models
        
        Returns:
            Feature importance dataframe
        """
        print(f"\n{'='*70}")
        print("FEATURE IMPORTANCE ANALYSIS")
        print(f"{'='*70}")
        
        # Logistic Regression coefficients (feature importance)
        lr_coef = self.lr_model.coef_[0]
        lr_importance = np.abs(lr_coef)
        
        # Naive Bayes - use learned parameters (theta/var)
        try:
            # Try to get variance from the model
            if hasattr(self.nb_model, 'var_'):
                nb_importance = np.abs(self.nb_model.var_[1] - self.nb_model.var_[0])
            elif hasattr(self.nb_model, 'sigma_'):
                nb_importance = np.abs(self.nb_model.sigma_[1] - self.nb_model.sigma_[0])
            else:
                # Fallback: use theta (mean) difference
                nb_importance = np.abs(self.nb_model.theta_[1] - self.nb_model.theta_[0])
        except:
            # If all else fails, use uniform importance for NB
            nb_importance = np.ones(len(self.feature_names))
        
        # Create importance dataframe
        importance_df = pd.DataFrame({
            'Feature': self.feature_names,
            'LR_Coefficient': lr_coef,
            'LR_Abs_Coef': lr_importance,
            'NB_Variance_Diff': nb_importance
        })
        
        # Rank features
        lr_rank = importance_df[['Feature', 'LR_Abs_Coef']].sort_values('LR_Abs_Coef', ascending=False)
        nb_rank = importance_df[['Feature', 'NB_Variance_Diff']].sort_values('NB_Variance_Diff', ascending=False)
        
        print("\nTOP 3 PREDICTORS - LOGISTIC REGRESSION:")
        print(lr_rank.head(3).to_string(index=False))
        
        print("\nTOP 3 PREDICTORS - NAIVE BAYES:")
        print(nb_rank.head(3).to_string(index=False))
        
        # Agreement analysis
        print(f"\n{'='*70}")
        print("FEATURE IMPORTANCE AGREEMENT ANALYSIS")
        print(f"{'='*70}")
        
        lr_top3 = set(lr_rank.head(3)['Feature'].values)
        nb_top3 = set(nb_rank.head(3)['Feature'].values)
        agreement = lr_top3.intersection(nb_top3)
        
        print(f"\nLogistic Regression Top 3: {lr_top3}")
        print(f"Naive Bayes Top 3: {nb_top3}")
        print(f"Agreement (both models): {agreement}")
        print(f"Agreement rate: {len(agreement)}/3 = {(len(agreement)/3)*100:.1f}%")
        
        if len(agreement) >= 2:
            print("\n✓ Strong agreement between models (good sign)")
            print(f"  Common top predictors: {', '.join(agreement)}")
            
            agreement_text = """
            MEDICAL JUSTIFICATION OF AGREED FEATURES:
            • These features consistently discriminate diabetic patients
            • Robust predictors across different algorithms
            • Should be priority in clinical interventions
            • Most reliable for medical decision support
            """
            print(agreement_text)
        else:
            print("\n⚠ Weak agreement between models")
            print("  Indicates complex feature interactions")
            print("  May require ensemble or non-linear models")
        
        return importance_df


# MAIN EXECUTION FOR TASK 3
if __name__ == "__main__":
    from data_preparation import DataPreparation
    from imblearn.over_sampling import SMOTE
    
    print("\n" + "="*70)
    print("TASK 3: STATISTICAL LEARNING FOR RISK STRATIFICATION")
    print("="*70)
    
    # Prepare data
    dp = DataPreparation('data/diabetes_dataset.csv')
    dp.preprocess_data()
    dp.split_dataset()
    dp.normalize_features()
    
    # Handle imbalance
    smote = SMOTE(random_state=42)
    X_train_balanced, y_train_balanced = smote.fit_resample(dp.X_train, dp.y_train)
    
    # Task 3(a): Train and evaluate models
    print("\n[TASK 3(a)] TRAIN STATISTICAL MODELS")
    sl = StatisticalLearningModels(dp.feature_names)
    sl.train_naive_bayes(X_train_balanced, y_train_balanced)
    sl.train_logistic_regression(X_train_balanced, y_train_balanced)
    
    print("\n[TASK 3(a)] EVALUATE & COMPARE MODELS")
    comparison = sl.evaluate_statistical_models(dp.X_test, dp.y_test)
    
    # Task 3(b): Feature importance analysis
    print("\n[TASK 3(b)] FEATURE IMPORTANCE ANALYSIS")
    importance = sl.feature_importance_analysis()
    
    print("\n" + "="*70)
    print("✓ TASK 3 COMPLETED")
    print("="*70)
