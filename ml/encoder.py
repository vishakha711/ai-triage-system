from sentence_transformers import SentenceTransformer
import torch

# Global variables initially empty
model = None

# -----------------------------
# Load MiniLM only once 
# -----------------------------
def load_bert():
    global model

    if model is None:
        print("Loading MiniLM model... (Optimized for Render RAM)")
        
        model_name = "all-MiniLM-L6-v2"
        
        model = SentenceTransformer(model_name)
        
        torch.set_num_threads(1) 
        
        print("MiniLM Loaded Successfully!")


# -----------------------------
# Encode symptoms text (Vectorization)
# -----------------------------
def encode_symptoms(text):
    # Ensure model is loaded
    load_bert() 

    # Input cleaning (Essential for good results)
    if not text:
        text = "normal"

    embedding = model.encode(text)

    return embedding