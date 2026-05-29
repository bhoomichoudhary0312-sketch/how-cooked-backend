import pandas as pd
import numpy as np
from sklearn.linear_model import LogisticRegression
import pickle

def generate_synthetic_data(n=1000):
    """Generates a synthetic dataset for training."""
    np.random.seed(42)
    
    data = {
        'attendance': np.random.randint(40, 100, n),
        'internal_marks': np.random.randint(5, 30, n),
        'assignments': np.random.randint(20, 100, n),
        'sleep': np.random.randint(3, 10, n),
        'study': np.random.randint(0, 10, n),
        'backlogs': np.random.randint(0, 8, n),
        'difficulty': np.random.randint(1, 4, n)  # 1: Easy, 2: Medium, 3: Hard
    }
    
    df = pd.DataFrame(data)
    
    # Logic to determine if a student is "Cooked" (1) or "Safe" (0)
    # This creates a pattern for the AI to learn
    score = (
        (100 - df['attendance']) * 0.4 +
        (30 - df['internal_marks']) * 1.5 +
        (df['backlogs'] * 15) +
        (8 - df['sleep']) * 5 -
        (df['study'] * 8)
    )
    
    # If the danger score is high, label them as 'Cooked'
    df['is_cooked'] = (score > 60).astype(int)
    return df

# 1. Prepare Data
print("Generating synthetic student data...")
df = generate_synthetic_data()
X = df.drop('is_cooked', axis=1) # Features
y = df['is_cooked']              # Target (0 or 1)

# 2. Train the Model
print("Training Logistic Regression model...")
model = LogisticRegression()
model.fit(X, y)

# 3. Save the Model
with open('model.pkl', 'wb') as f:
    pickle.dump(model, f)

print("Success! 'model.pkl' has been created in the backend folder.")