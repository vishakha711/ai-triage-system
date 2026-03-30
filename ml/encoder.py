from transformers import AutoTokenizer, AutoModel
import torch

# Global variables initially empty
tokenizer = None
model = None

# -----------------------------
# Load DistilBERT only once (Lightweight & Fast)
# -----------------------------
def load_bert():
    global tokenizer, model

    if tokenizer is None or model is None:
        # Hackathon Optimization: Using DistilBERT for 60% faster loading
        print("Loading DistilBERT model... (Optimized for Speed)")
        
        model_name = "distilbert-base-uncased"
        
        tokenizer = AutoTokenizer.from_pretrained(model_name)
        model = AutoModel.from_pretrained(model_name)
        
        torch.set_num_threads(4) 
        
        model.eval()
        print("DistilBERT Loaded Successfully!")


# -----------------------------
# Encode symptoms text (Vectorization)
# -----------------------------
def encode_symptoms(text):
    # Ensure model is loaded
    load_bert() 

    # Input cleaning (Essential for good results)
    if not text:
        text = "normal"

    inputs = tokenizer(
        text,
        return_tensors="pt",
        truncation=True,
        padding=True,
        max_length=128 
    )

    with torch.no_grad():
        outputs = model(**inputs)

    embedding = outputs.last_hidden_state.mean(dim=1)

    # Convert to numpy array for the fusion layer
    return embedding.numpy()[0]