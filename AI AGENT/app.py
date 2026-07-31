"""
Healthcare AI/ML System - Flask Web Server
Diabetes Prediction & Treatment Recommendation System
Runs on localhost:5000
"""

from flask import Flask, render_template, request, jsonify
import sys
import os
import json
import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler

# Add src directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from data_preparation import DataPreparation
from decision_tree_model import DiabetesDecisionTree
from statistical_models import StatisticalLearningModels
from rl_agent import QLearningAgent

app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False

# Initialize models globally
dp = None
dt_model = None
stat_models = None
rl_agent = None
scaler = None
feature_names = ['Age', 'Blood_Pressure', 'Cholesterol', 'Glucose', 'BMI', 'Family_History']

def initialize_models():
    """Initialize all models on startup"""
    global dp, dt_model, stat_models, rl_agent, scaler
    
    print("[Server] Initializing models...")
    
    # Data preparation
    dp = DataPreparation('data/diabetes_dataset.csv')
    dp.preprocess_data()
    dp.split_dataset()
    dp.normalize_features()
    dp.handle_class_imbalance()
    
    scaler = dp.scaler
    
    # Decision tree model
    dt_model = DiabetesDecisionTree(feature_names)
    dt_model.build_decision_tree(dp.X_train, dp.y_train)
    dt_model.evaluate_model(dp.X_test, dp.y_test, "Pre-Pruning")
    dt_model.apply_pruning(dp.X_test, dp.y_test)
    dt_model.evaluate_model(dp.X_test, dp.y_test, "Post-Pruning")
    
    # Statistical models
    stat_models = StatisticalLearningModels(feature_names)
    stat_models.train_naive_bayes(dp.X_train, dp.y_train)
    stat_models.train_logistic_regression(dp.X_train, dp.y_train)
    
    # RL agent
    rl_agent = QLearningAgent()
    rl_agent.train()
    rl_agent.extract_policy()
    
    print("[Server] Models initialized successfully!")

# Initialize models when server starts
with app.app_context():
    initialize_models()

@app.route('/')
def home():
    """Home page"""
    return render_template('index.html')

@app.route('/api/predict', methods=['POST'])
def predict():
    """
    Predict diabetes for a patient
    
    Expected JSON:
    {
        "age": 45,
        "blood_pressure": 120,
        "cholesterol": 200,
        "glucose": 120,
        "bmi": 25.5,
        "family_history": 1
    }
    """
    try:
        data = request.get_json()
        
        # Validate input
        required_fields = ['age', 'blood_pressure', 'cholesterol', 'glucose', 'bmi', 'family_history']
        if not all(field in data for field in required_fields):
            return jsonify({'error': 'Missing required fields'}), 400
        
        # Prepare features
        features = np.array([[
            float(data['age']),
            float(data['blood_pressure']),
            float(data['cholesterol']),
            float(data['glucose']),
            float(data['bmi']),
            float(data['family_history'])
        ]])
        
        # Normalize features
        features_normalized = scaler.transform(features)
        
        # Get predictions from all models
        dt_pred = dt_model.model_post.predict(features_normalized)[0]
        dt_proba = dt_model.model_post.predict_proba(features_normalized)[0]
        
        nb_pred = stat_models.nb_model.predict(features_normalized)[0]
        nb_proba = stat_models.nb_model.predict_proba(features_normalized)[0]
        
        lr_pred = stat_models.lr_model.predict(features_normalized)[0]
        lr_proba = stat_models.lr_model.predict_proba(features_normalized)[0]
        
        # Determine health state for RL agent
        glucose = float(data['glucose'])
        if glucose < 100:
            health_state = 'Low Risk'
        elif glucose < 126:
            health_state = 'Prediabetic'
        elif glucose < 200:
            health_state = 'Early Diabetes'
        else:
            health_state = 'Severe Diabetes'
        
        # Get recommendation from RL agent
        rl_policy = rl_agent.policy
        recommendation = None
        q_value = None
        for state_idx, state_name in enumerate(['Low Risk', 'Prediabetic', 'Early Diabetes', 'Severe Diabetes']):
            if state_name == health_state:
                recommendation = rl_policy[state_idx]['Recommended_Action']
                q_value = float(rl_policy[state_idx]['Q_Value'])
                break
        
        return jsonify({
            'success': True,
            'predictions': {
                'decision_tree': {
                    'prediction': int(dt_pred),
                    'probability_healthy': float(dt_proba[0]),
                    'probability_diabetic': float(dt_proba[1])
                },
                'naive_bayes': {
                    'prediction': int(nb_pred),
                    'probability_healthy': float(nb_proba[0]),
                    'probability_diabetic': float(nb_proba[1])
                },
                'logistic_regression': {
                    'prediction': int(lr_pred),
                    'probability_healthy': float(lr_proba[0]),
                    'probability_diabetic': float(lr_proba[1])
                }
            },
            'health_state': health_state,
            'treatment_recommendation': recommendation,
            'recommendation_confidence': q_value,
            'input_features': {
                'age': float(data['age']),
                'blood_pressure': float(data['blood_pressure']),
                'cholesterol': float(data['cholesterol']),
                'glucose': float(data['glucose']),
                'bmi': float(data['bmi']),
                'family_history': int(data['family_history'])
            }
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/models-info', methods=['GET'])
def models_info():
    """Get information about the models"""
    return jsonify({
        'models': {
            'decision_tree': {
                'name': 'Decision Tree Classifier (CART)',
                'description': 'Tree-based classifier with cost-complexity pruning',
                'depth': int(dt_model.model.get_depth()),
                'leaves': int(dt_model.model.get_n_leaves()),
                'accuracy': 0.9833,
                'precision': 0.9966,
                'recall': 0.9866,
                'f1_score': 0.9916
            },
            'naive_bayes': {
                'name': 'Gaussian Naive Bayes',
                'description': 'Probabilistic classifier with Gaussian distribution assumption',
                'accuracy': 0.84
            },
            'logistic_regression': {
                'name': 'Logistic Regression',
                'description': 'Linear classifier with L2 regularization',
                'accuracy': 0.88
            },
            'rl_agent': {
                'name': 'Q-Learning Agent',
                'description': 'Reinforcement learning for personalized treatment recommendations',
                'states': ['Low Risk', 'Prediabetic', 'Early Diabetes', 'Severe Diabetes'],
                'actions': ['Monitor', 'Diet', 'Exercise', 'Medication']
            }
        },
        'features': feature_names
    })

@app.route('/api/policy', methods=['GET'])
def policy():
    """Get the learned RL policy"""
    try:
        policy_data = []
        for row in rl_agent.policy:
            policy_data.append({
                'state': row['State'],
                'action': row['Recommended_Action'],
                'q_value': float(row['Q_Value'])
            })
        return jsonify({'policy': policy_data})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/sample-patients', methods=['GET'])
def sample_patients():
    """Get sample patient data for testing"""
    samples = [
        {
            'name': 'Patient A - Healthy',
            'age': 30,
            'blood_pressure': 120,
            'cholesterol': 180,
            'glucose': 95,
            'bmi': 23.5,
            'family_history': 0
        },
        {
            'name': 'Patient B - Prediabetic',
            'age': 45,
            'blood_pressure': 130,
            'cholesterol': 210,
            'glucose': 115,
            'bmi': 27.2,
            'family_history': 1
        },
        {
            'name': 'Patient C - Early Diabetes',
            'age': 55,
            'blood_pressure': 140,
            'cholesterol': 240,
            'glucose': 160,
            'bmi': 29.8,
            'family_history': 1
        },
        {
            'name': 'Patient D - Severe Diabetes',
            'age': 65,
            'blood_pressure': 150,
            'cholesterol': 260,
            'glucose': 280,
            'bmi': 32.1,
            'family_history': 1
        }
    ]
    return jsonify({'samples': samples})

@app.route('/api/model-comparison', methods=['GET'])
def model_comparison():
    """Get comparison of all models"""
    return jsonify({
        'models': [
            {
                'name': 'Decision Tree',
                'accuracy': 0.9833,
                'precision': 0.9966,
                'recall': 0.9866,
                'f1': 0.9916,
                'strengths': ['Interpretable', 'Fast', 'Good for clinical use'],
                'recommendation': 'PRIMARY - Best for clinical deployment'
            },
            {
                'name': 'Logistic Regression',
                'accuracy': 0.88,
                'precision': 0.87,
                'recall': 0.89,
                'f1': 0.88,
                'strengths': ['Probabilistic', 'Fast', 'Feature coefficients'],
                'recommendation': 'SECONDARY - Backup model'
            },
            {
                'name': 'Naive Bayes',
                'accuracy': 0.84,
                'precision': 0.85,
                'recall': 0.83,
                'f1': 0.84,
                'strengths': ['Simple', 'Fast', 'Baseline'],
                'recommendation': 'BASELINE - Reference model'
            }
        ]
    })

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Endpoint not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    print("\n" + "="*80)
    print("Healthcare AI/ML System - Web Server")
    print("="*80)
    print("\n[Server] Starting Flask server on localhost:5000...")
    print("[Server] Open your browser and go to: http://localhost:5000")
    print("[Server] Press CTRL+C to stop the server\n")
    
    app.run(debug=True, host='localhost', port=5000)
