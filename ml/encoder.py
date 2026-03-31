from sentence_transformers import SentenceTransformer
import torch
import gc

# Model variable ko initially None rakhein
model = None

def load_bert():
    global model
    if model is None:
        print("Loading MiniLM model... (Memory Optimized Mode)")
        
        device = "cpu"
        
        model = SentenceTransformer('all-MiniLM-L6-v2', device=device)
        
        torch.set_num_threads(1)
        
        model.eval()
        print("Model Loaded Successfully!")

def encode_symptoms(text):
    global model
    load_bert()
    
    if not text:
        text = "normal"


    with torch.no_grad():
        
        embedding = model.encode(text, convert_to_numpy=True)

    return embedding