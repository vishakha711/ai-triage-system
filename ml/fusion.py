import numpy as np

def fuse_features(embedding, patient):

    numeric = np.array([
        patient["age"],
        patient["heart_rate"],
        patient["spo2"],
        patient["temperature"],
        patient["waiting_time"],
        patient["emergency_score"]
    ])

    return np.concatenate([embedding,numeric])