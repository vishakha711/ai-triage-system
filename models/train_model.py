import pandas as pd
import pickle
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from sentence_transformers import SentenceTransformer
import torch

# Load Dataset
df = pd.read_csv("data/er_patient_dataset.csv")

# Load MiniLM (same as encoder.py)
print("Loading MiniLM model...")
model_bert = SentenceTransformer('all-MiniLM-L6-v2', device='cpu')
model_bert.eval()

def encode_text(text):
    with torch.no_grad():
        return model_bert.encode(text, convert_to_numpy=True)  # 384 dim

print("Encoding symptoms...")
embeddings = np.vstack(df["symptom_text"].apply(encode_text))

# Numerical Features
num_features = df[[
    "age", "heart_rate", "spo2",
    "temperature", "waiting_time", "emergency_score"
]].values

# Combine → 384 + 6 = 390 features
X = np.hstack([embeddings, num_features])

# Labels
le = LabelEncoder()
y = le.fit_transform(df["priority_label"])

# Train
print("Training model...")
model = RandomForestClassifier(n_estimators=150)
model.fit(X, y)

# Save to models/ folder 
pickle.dump(model, open("models/triage_model.pkl", "wb"))
pickle.dump(le, open("models/label_encoder.pkl", "wb"))

print("Model trained & saved successfully!")