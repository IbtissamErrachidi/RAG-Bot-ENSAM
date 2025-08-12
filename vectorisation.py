from transformers import AutoTokenizer, AutoModel
import torch

# 1. Charger le tokenizer et le modèle pré-entraîné E5-large
tokenizer = AutoTokenizer.from_pretrained("intfloat/e5-large")
model = AutoModel.from_pretrained("intfloat/e5-large")

def embed(texts):
    # 2. Tokenizer le texte en entrée, avec padding et truncation, sortie en tenseurs PyTorch
    inputs = tokenizer(texts, padding=True, truncation=True, return_tensors="pt")

    # 3. Passer les tokens dans le modèle (sans calcul du gradient, donc mode évaluation)
    with torch.no_grad():
        # Récupérer la sortie du modèle : vecteurs des tokens
        outputs = model(**inputs, return_dict=True)

        # 4. Extraire l'embedding du token [CLS] (premier token) qui représente la phrase entière
        embeddings = outputs.last_hidden_state[:,0]  # dimension : (batch_size, hidden_size)

    return embeddings

# # Exemple d'utilisation
# texts = ["Bonjour", "Intelligence artificielle"]
# vectors = embed(texts)
# print(vectors.shape)  # Ex: torch.Size([2, 1024]) si hidden_size=1024
