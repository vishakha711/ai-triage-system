import pickle
import numpy as np

model=pickle.load(open("models/triage_model.pkl","rb"))
le=pickle.load(open("models/label_encoder.pkl","rb"))

def predict(features):

    probs=model.predict_proba([features])[0]

    idx=np.argmax(probs)
    confidence=float(probs[idx])

    return le.inverse_transform([idx])[0],confidence