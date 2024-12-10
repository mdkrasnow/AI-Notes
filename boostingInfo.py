boosting_info = {
        "cornell_notes": """
Boosting in data science is an ensemble learning technique that combines multiple weak learners into a strong learner. 
Key concepts from a Cornell notes perspective:
• Sequential Learning: Each model learns from the mistakes of previous models
• Weighted Samples: Misclassified samples get higher weights in subsequent iterations
• Adaptive Learning: The algorithm adapts to difficult patterns over time
• Error Minimization: Focuses on reducing both bias and variance
• Model Combination: Final prediction is a weighted sum of all weak learners
        """,
        
        "background": """
Boosting emerged from the theoretical question: Can weak learners be combined to create a strong learner? 
Historical and Technical Context:
1. Origins in PAC (Probably Approximately Correct) learning theory
2. First practical implementation: AdaBoost (Adaptive Boosting) in 1995
3. Evolution to Gradient Boosting in early 2000s
4. Modern implementations like XGBoost, LightGBM, and CatBoost

Key Components:
• Loss Function: Measures prediction errors
• Weak Learner: Usually decision trees with limited depth
• Additive Model: Sequential addition of weak learners
• Learning Rate: Controls contribution of each weak learner
• Regularization: Prevents overfitting through various techniques
        """,
        
        "conclusion": """
Boosting represents one of the most powerful and widely-used techniques in modern machine learning:

Practical Applications:
1. Ranking algorithms in search engines
2. Computer vision and object detection
3. Natural language processing tasks
4. Financial forecasting and risk assessment
5. Recommendation systems

Key Advantages:
• High prediction accuracy
• Handles different types of predictors
• Built-in feature selection
• Robust to outliers
• Captures complex non-linear patterns

Limitations:
• Computationally intensive
• Risk of overfitting
• Sensitive to noisy data
• Less interpretable than single models
• Requires careful parameter tuning
        """
    }
