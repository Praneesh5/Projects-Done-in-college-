"""
Task 4: Reinforcement Learning for Treatment Recommendation
Q-Learning agent for personalized medical treatment recommendations
"""
import numpy as np
import pandas as pd
from collections import defaultdict
import warnings
warnings.filterwarnings('ignore')

class TreatmentRecommendationMDP:
    """
    Markov Decision Process for medical treatment recommendations
    """
    
    def __init__(self):
        """Initialize the MDP"""
        self.define_mdp()
    
    def define_mdp(self):
        """
        Task 4(a): Define MDP components
        States, Actions, Rewards, and Transition dynamics
        """
        mdp_definition = """
        MDP DEFINITION FOR TREATMENT RECOMMENDATION
        ==========================================
        
        1. STATES (Patient Health Stages):
        ===================================
        State representation: [glucose_level, bmi_status, bp_status]
        
        S0: Low Risk (Healthy)
            • Glucose < 100 mg/dL (fasting)
            • BMI < 25 (normal weight)
            • BP < 120 mmHg
            • Action: Monitor
        
        S1: Prediabetic (Moderate Risk)
            • Glucose 100-125 mg/dL
            • BMI 25-30 (overweight)
            • BP 120-139 mmHg
            • Actions: Diet + Exercise + Monitor
        
        S2: Early Diabetes (High Risk)
            • Glucose 125-200 mg/dL
            • BMI 30-35 (obese)
            • BP 139-160 mmHg
            • Actions: Diet + Exercise + Monitor
        
        S3: Severe Diabetes (Critical)
            • Glucose > 200 mg/dL
            • BMI > 35 (severely obese)
            • BP > 160 mmHg
            • Actions: Medication + Monitor
        
        JUSTIFICATION:
        • Clinically meaningful classification
        • Actionable for physicians
        • Reflects disease progression
        • Based on WHO/ADA guidelines
        
        2. ACTIONS (Treatment Interventions):
        ====================================
        Four discrete actions available:
        
        A0: Monitor Only
            • Cost: Low (routine checkup)
            • Effect: Maintain current state or minor improvement
            • When: Healthy patients, maintenance phase
            • Duration: 3-6 months
        
        A1: Diet Modification
            • Cost: Low (consultation, no drugs)
            • Effect: Modest improvement (5-10% weight loss)
            • Impact: Glucose ↓, BMI ↓, BP ↓
            • When: Prediabetic patients
            • Duration: 2-3 months
        
        A2: Exercise Program
            • Cost: Medium (gym membership, trainer)
            • Effect: Significant improvement (10-15% weight loss)
            • Impact: Glucose ↓↓, BMI ↓↓, BP ↓↓
            • When: Prediabetic, early diabetes
            • Duration: 3-6 months
        
        A3: Medication
            • Cost: High (long-term medication)
            • Effect: Strong improvement (15-30% glucose reduction)
            • Impact: Glucose ↓↓↓, controlled BP
            • When: Severe diabetes, medication-dependent
            • Duration: Ongoing
        
        JUSTIFICATION:
        • Graduated intervention approach
        • Non-pharmacological first
        • Escalates based on patient state
        • Evidence-based clinical practice
        
        3. REWARD FUNCTION (Health Improvement Score):
        =============================================
        
        R(s, a) = Immediate Health Benefit - Treatment Cost
        
        REWARD MATRIX:
        
        From S0 (Healthy):
        • Monitor: +1 (maintain health)
        • Diet: -0.5 (unnecessary intervention)
        • Exercise: -1 (over-treatment)
        • Medication: -3 (harmful, unneeded)
        
        From S1 (Prediabetic):
        • Monitor: -0.5 (allow progression)
        • Diet: +3 (effective intervention)
        • Exercise: +5 (best option)
        • Medication: +1 (premature)
        
        From S2 (Early Diabetes):
        • Monitor: -1 (dangerous)
        • Diet: +2 (modest benefit)
        • Exercise: +4 (good benefit)
        • Medication: +6 (appropriate)
        
        From S3 (Severe Diabetes):
        • Monitor: -3 (life-threatening)
        • Diet: -1 (insufficient)
        • Exercise: +2 (beneficial but limited)
        • Medication: +8 (critical intervention)
        
        JUSTIFICATION OF REWARDS:
        • Higher rewards for clinically appropriate actions
        • Penalties for under/over-treatment
        • Patient safety as primary objective
        • Cost-effectiveness balanced with health
        
        4. TRANSITION DYNAMICS P(s'|s,a):
        ================================
        
        State transitions based on treatment effectiveness:
        
        Deterministic (simplified model):
        • Exercise in S1 → 70% chance S0, 30% chance S1
        • Exercise in S2 → 60% chance S1, 40% chance S2
        • Medication in S2 → 80% chance S1, 20% chance S2
        • Medication in S3 → 75% chance S2, 25% chance S3
        
        Random effects modeled with stochastic transitions
        
        JUSTIFICATION:
        • Variable patient response to treatment
        • Individual differences in compliance
        • External factors (diet, stress)
        • Real-world variability captured
        
        ETHICAL CONSIDERATIONS IN MDP:
        • Rewards favor early intervention
        • No permanent disease states (recovery possible)
        • Cost-benefit aligned with clinical practice
        • Patient autonomy respected (action choice)
        """
        
        print(mdp_definition)
        
        # Store MDP components
        self.states = ['Low Risk', 'Prediabetic', 'Early Diabetes', 'Severe Diabetes']
        self.actions = ['Monitor', 'Diet', 'Exercise', 'Medication']
        self.state_dict = {i: name for i, name in enumerate(self.states)}
        self.action_dict = {i: name for i, name in enumerate(self.actions)}
        
        return self.states, self.actions


class QLearningAgent:
    """
    Q-Learning Agent for treatment recommendation
    """
    
    def __init__(self, n_states=4, n_actions=4, learning_rate=0.1, discount_factor=0.95, epsilon=0.1):
        """
        Initialize Q-Learning agent
        
        Args:
            n_states: Number of states
            n_actions: Number of actions
            learning_rate: Alpha parameter
            discount_factor: Gamma parameter
            epsilon: Epsilon-greedy parameter
        """
        self.n_states = n_states
        self.n_actions = n_actions
        self.lr = learning_rate  # Alpha
        self.gamma = discount_factor  # Gamma
        self.epsilon = epsilon
        
        # Initialize Q-table
        self.Q = defaultdict(lambda: np.zeros(n_actions))
        
        # MDP
        self.mdp = TreatmentRecommendationMDP()
        
        # Reward matrix
        self.rewards = self._initialize_reward_matrix()
        
        # Transition probabilities
        self.transitions = self._initialize_transitions()
    
    def _initialize_reward_matrix(self):
        """Initialize reward matrix R(s,a)"""
        rewards = {
            0: {'Monitor': 1.0, 'Diet': -0.5, 'Exercise': -1.0, 'Medication': -3.0},
            1: {'Monitor': -0.5, 'Diet': 3.0, 'Exercise': 5.0, 'Medication': 1.0},
            2: {'Monitor': -1.0, 'Diet': 2.0, 'Exercise': 4.0, 'Medication': 6.0},
            3: {'Monitor': -3.0, 'Diet': -1.0, 'Exercise': 2.0, 'Medication': 8.0}
        }
        return rewards
    
    def _initialize_transitions(self):
        """Initialize state transition probabilities"""
        transitions = {
            # State 0 (Healthy) - mostly stay or worsen with bad treatment
            (0, 0): {0: 0.8, 1: 0.2},           # Monitor
            (0, 1): {0: 0.7, 1: 0.3},           # Diet
            (0, 2): {0: 0.85, 1: 0.15},         # Exercise
            (0, 3): {0: 0.6, 1: 0.4},           # Medication (side effects)
            
            # State 1 (Prediabetic)
            (1, 0): {1: 0.5, 2: 0.5},           # Monitor - worsen
            (1, 1): {0: 0.4, 1: 0.5, 2: 0.1},   # Diet
            (1, 2): {0: 0.7, 1: 0.25, 2: 0.05}, # Exercise - best
            (1, 3): {1: 0.6, 2: 0.4},           # Medication
            
            # State 2 (Early Diabetes)
            (2, 0): {2: 0.4, 3: 0.6},           # Monitor - worsen
            (2, 1): {1: 0.3, 2: 0.6, 3: 0.1},   # Diet
            (2, 2): {1: 0.5, 2: 0.4, 3: 0.1},   # Exercise
            (2, 3): {1: 0.4, 2: 0.5, 3: 0.1},   # Medication
            
            # State 3 (Severe Diabetes)
            (3, 0): {3: 0.7, 2: 0.3},           # Monitor
            (3, 1): {3: 0.5, 2: 0.5},           # Diet
            (3, 2): {2: 0.6, 3: 0.4},           # Exercise
            (3, 3): {2: 0.75, 3: 0.25}          # Medication - best
        }
        return transitions
    
    def get_reward(self, state, action):
        """Get reward for state-action pair"""
        action_name = self.mdp.action_dict[action]
        return self.rewards[state].get(action_name, 0)
    
    def get_next_state(self, state, action):
        """Sample next state from transition probabilities"""
        key = (state, action)
        if key in self.transitions:
            next_states = self.transitions[key]
            return np.random.choice(list(next_states.keys()), p=list(next_states.values()))
        return state
    
    def epsilon_greedy_action(self, state):
        """Select action using epsilon-greedy strategy"""
        if np.random.random() < self.epsilon:
            return np.random.randint(self.n_actions)  # Explore
        else:
            return np.argmax(self.Q[state])  # Exploit
    
    def train(self, n_episodes=5, episode_length=10, verbose=True):
        """
        Task 4(b): Train Q-Learning agent
        
        Args:
            n_episodes: Number of episodes (patient trajectories)
            episode_length: Steps per episode
            verbose: Print training progress
        
        Returns:
            Training history
        """
        print(f"\n{'='*70}")
        print("Q-LEARNING TRAINING")
        print(f"{'='*70}")
        print(f"Episodes: {n_episodes}")
        print(f"Max steps per episode: {episode_length}")
        print(f"Learning rate (α): {self.lr}")
        print(f"Discount factor (γ): {self.gamma}")
        print(f"Epsilon (ε): {self.epsilon}")
        
        training_history = []
        
        for episode in range(n_episodes):
            state = np.random.randint(0, self.n_states)  # Start with random patient state
            episode_reward = 0
            
            if verbose:
                print(f"\n{'='*70}")
                print(f"EPISODE {episode + 1}/{n_episodes}")
                print(f"{'='*70}")
                print(f"Initial patient state: {self.mdp.state_dict[state]}")
            
            for step in range(episode_length):
                # Select action
                action = self.epsilon_greedy_action(state)
                
                # Get reward
                reward = self.get_reward(state, action)
                
                # Transition to next state
                next_state = self.get_next_state(state, action)
                
                # Q-Learning update
                old_q = self.Q[state][action]
                next_q_max = np.max(self.Q[next_state])
                
                # Q(s,a) ← Q(s,a) + α[r + γ*max(Q(s',a')) - Q(s,a)]
                self.Q[state][action] = old_q + self.lr * (reward + self.gamma * next_q_max - old_q)
                
                episode_reward += reward
                
                if verbose and step < 3:  # Print first 3 steps
                    print(f"\nStep {step + 1}:")
                    print(f"  Current state: {self.mdp.state_dict[state]}")
                    print(f"  Action: {self.mdp.action_dict[action]}")
                    print(f"  Reward: {reward:.2f}")
                    print(f"  Next state: {self.mdp.state_dict[next_state]}")
                    print(f"  Q-update: {old_q:.4f} → {self.Q[state][action]:.4f}")
                
                state = next_state
            
            training_history.append(episode_reward)
            if verbose:
                print(f"\nEpisode total reward: {episode_reward:.2f}")
        
        return training_history
    
    def extract_policy(self):
        """
        Task 4(c): Extract learned policy
        
        Returns:
            Policy dataframe
        """
        print(f"\n{'='*70}")
        print("LEARNED POLICY EXTRACTION")
        print(f"{'='*70}")
        
        policy_data = []
        
        for state in range(self.n_states):
            q_values = self.Q[state]
            best_action = np.argmax(q_values)
            best_q_value = np.max(q_values)
            
            policy_data.append({
                'State': self.mdp.state_dict[state],
                'Recommended_Action': self.mdp.action_dict[best_action],
                'Q_Value': best_q_value,
                'All_Q_Values': {self.mdp.action_dict[i]: q_values[i] for i in range(self.n_actions)}
            })
        
        policy_df = pd.DataFrame(policy_data)
        
        print("\nFINAL LEARNED POLICY:")
        print(policy_df[['State', 'Recommended_Action', 'Q_Value']].to_string(index=False))
        
        print(f"\n{'='*70}")
        print("DETAILED Q-VALUES FOR EACH STATE:")
        print(f"{'='*70}")
        
        for _, row in policy_df.iterrows():
            print(f"\n{row['State']}:")
            q_vals = row['All_Q_Values']
            for action, q_val in sorted(q_vals.items(), key=lambda x: x[1], reverse=True):
                marker = "→ " if action == row['Recommended_Action'] else "  "
                print(f"  {marker}{action:15s}: {q_val:.4f}")
        
        return policy_df
    
    def ethical_analysis(self):
        """
        Task 4(c): Ethical considerations for deployment
        """
        ethical_discussion = """
        ETHICAL CONSIDERATIONS FOR RL-BASED MEDICAL TREATMENT
        =====================================================
        
        1. PATIENT SAFETY (Primary Concern):
        ==================================
        ✓ Strengths:
          • Q-Learning converges to optimal policy
          • Rewards designed to prevent harmful treatments
          • State space captures critical health stages
        
        ⚠ Risks:
          • Model hasn't seen edge cases
          • May recommend actions outside safe bounds
          • Adverse effects not fully modeled
        
        MITIGATION:
          • Implement hard constraints (action filtering)
          • Require physician override capability
          • Continuous monitoring of recommendations
          • A/B testing before deployment
        
        2. BIAS & FAIRNESS:
        ================
        ⚠ Potential Issues:
          • Training data bias (specific patient demographics)
          • Model may learn demographic discrimination
          • Reward function reflects designer bias
        
        ✓ Safeguards:
          • Regular bias auditing
          • Fairness constraints in rewards
          • Diverse patient representation in evaluation
          • Documentation of model assumptions
        
        3. EXPLAINABILITY & TRANSPARENCY:
        ===============================
        ✓ Advantages:
          • Q-Learning provides action rationales
          • Policy is human-interpretable
          • State space clinically meaningful
        
        ⚠ Challenges:
          • "Black box" nature of learned values
          • Difficult to explain WHY action best
          • No natural language explanations
        
        IMPROVEMENT:
          • Visualize Q-value heatmaps
          • Provide confidence scores
          • Show alternative action rankings
          • Explain state assessment reasoning
        
        4. ACCOUNTABILITY & LIABILITY:
        ============================
        LEGAL FRAMEWORK:
          • Clear liability assignment
          • Physician retains responsibility
          • Model as decision support, not replacement
          • Audit trail for all recommendations
        
        REGULATORY:
          • FDA approval required (Class II-III device)
          • Validation against clinical standards
          • Post-market surveillance
          • Performance monitoring
        
        5. PATIENT AUTONOMY:
        ==================
        REQUIREMENTS:
          • Patients informed of AI involvement
          • Option to decline recommendations
          • Physician consultation mandatory
          • Alternative treatments presented
        
        IMPLEMENTATION:
          • Clear consent forms
          • Transparent UI/UX
          • Easy access to physician override
          • Patient education materials
        
        6. CONTINUOUS IMPROVEMENT:
        ==========================
        MONITORING:
          • Track recommendation outcomes
          • Update models quarterly
          • Report on safety metrics
          • Collect physician feedback
        
        RESEARCH:
          • Clinical trials for validation
          • Comparison with standard care
          • Long-term outcome studies
          • Effect on health equity
        
        DEPLOYMENT ROADMAP:
        ═══════════════════
        Phase 1: Pilot Program (6 months)
          • Limited patient cohort
          • Careful monitoring
          • Frequent audits
        
        Phase 2: Extended Trial (1 year)
          • Larger patient group
          • Regional deployment
          • Performance validation
        
        Phase 3: Clinical Deployment
          • Hospital integration
          • Continuous monitoring
          • Regular retraining
          • Ongoing evaluation
        
        CONCLUSION:
        ───────────
        RL agents can improve personalized treatment recommendations when:
        • Deployed as DECISION SUPPORT (not replacement)
        • Subject to physician OVERSIGHT
        • With continuous MONITORING and UPDATING
        • Transparent about LIMITATIONS
        • Designed with PATIENT SAFETY as primary objective
        """
        
        print(ethical_discussion)
        return ethical_discussion


# MAIN EXECUTION FOR TASK 4
if __name__ == "__main__":
    print("\n" + "="*70)
    print("TASK 4: REINFORCEMENT LEARNING FOR TREATMENT RECOMMENDATION")
    print("="*70)
    
    # Task 4(a): Define MDP
    print("\n[TASK 4(a)] MDP DEFINITION")
    print("="*70)
    
    # Initialize agent
    agent = QLearningAgent(n_states=4, n_actions=4, learning_rate=0.1, discount_factor=0.95, epsilon=0.1)
    
    # Task 4(b): Train agent
    print("\n[TASK 4(b)] Q-LEARNING TRAINING")
    training_history = agent.train(n_episodes=5, episode_length=10, verbose=True)
    
    # Task 4(c): Extract policy
    print("\n[TASK 4(c)] LEARNED POLICY")
    policy = agent.extract_policy()
    
    # Task 4(c): Ethical analysis
    print("\n[TASK 4(c)] ETHICAL CONSIDERATIONS")
    ethical = agent.ethical_analysis()
    
    print("\n" + "="*70)
    print("✓ TASK 4 COMPLETED")
    print("="*70)
