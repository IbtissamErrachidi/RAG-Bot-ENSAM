import numpy as np

def search_and_display(query, index, indexed_chunks, k=5):
    # 1. Embedding
    query_emb = embed([query]).detach().cpu().numpy().astype('float32')
    
    # 2. Normalisation pour cosine similarity (optionnel mais recommandé)
    norms = np.linalg.norm(query_emb, axis=1, keepdims=True)
    query_emb = query_emb / norms
    
    # 3. Recherche dans FAISS
    distances, indices = index.search(query_emb, k)

    #4. Récupérer les chunks correspondants
    context_chunks = [indexed_chunks[i] for i in indices[0]]
    
    # 5. Affichage des résultats
    for rank, idx in enumerate(indices[0]):
        chunk = indexed_chunks[idx]
        print(f"{rank+1}. (distance={distances[0][rank]:.4f})")
        print(f"Source : {chunk['source']}")
        print(f"Texte  : {chunk['content'][:200]}...\n")

    return context_chunks

