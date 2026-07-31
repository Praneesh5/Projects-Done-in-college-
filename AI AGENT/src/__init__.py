"""
Healthcare AI/ML Project
Diabetes prediction and personalized treatment recommendation using ML and RL
"""

__version__ = "1.0.0"
__author__ = "AI/ML Engineer"
__description__ = "Healthcare AI System for Diabetes Prediction and Treatment Recommendation"

from .data_preparation import DataPreparation
from .decision_tree_model import DiabetesDecisionTree
from .statistical_models import StatisticalLearningModels
from .rl_agent import QLearningAgent, TreatmentRecommendationMDP

__all__ = [
    'DataPreparation',
    'DiabetesDecisionTree',
    'StatisticalLearningModels',
    'QLearningAgent',
    'TreatmentRecommendationMDP'
]
