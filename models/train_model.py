import pandas as pd
import pickle
import numpy as np

from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder

from transformers import AutoTokenizer, AutoModel
import torch

# -----------------------------
# Load Dataset
# -----------------------------
df = pd.read_csv("data/er_patient_dataset.csv")

# -----------------------------
# Load BERT
# -----------------------------
tokenizer = AutoTokenizer.from_pretrained("bert-base-uncased")
bert = AutoModel.from_pretrained("bert-base-uncased")

def encode_text(text):
    inputs = tokenizer(
        text,
        return_tensors="pt",
        truncation=True,
        padding=True,
        max_length=32
    )

    with torch.no_grad():
        outputs = bert(**inputs)

    embedding = outputs.last_hidden_state.mean(dim=1)
    return embedding.squeeze().numpy()

print("Encoding symptoms using BERT...")

# Convert all symptoms → embeddings
embeddings = np.vstack(df["symptom_text"].apply(encode_text))

# -----------------------------
# Numerical Features
# -----------------------------
num_features = df[
    [
        "age",
        "heart_rate",
        "spo2",
        "temperature",
        "waiting_time",
        "emergency_score",
    ]
].values

# Combine text + numeric
X = np.hstack([embeddings, num_features])

# -----------------------------
# Labels
# -----------------------------
le = LabelEncoder()
y = le.fit_transform(df["priority_label"])

# -----------------------------
# Train Model
# -----------------------------
model = RandomForestClassifier(n_estimators=150)
model.fit(X, y)

# -----------------------------
# Save Model
# -----------------------------
pickle.dump(model, open("triage_model.pkl", "wb"))
pickle.dump(le, open("label_encoder.pkl", "wb"))

print(" Model trained & saved successfully!")