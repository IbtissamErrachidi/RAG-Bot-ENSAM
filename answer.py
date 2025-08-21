import numpy as np

def search_and_display(query, index, indexed_chunks, k=10, keyword_weight=2.0):
    """
    Recherche les k chunks les plus pertinents en combinant :
    - similarité vectorielle
    - présence de mots-clés issus de la question
    """

    keywords = [word.lower() for word in query.split()]

    query_emb = embed([query]).detach().cpu().numpy().astype('float32')
    query_emb /= np.linalg.norm(query_emb, axis=1, keepdims=True)

    distances, indices = index.search(query_emb, k * 5)  # récupérer plus pour filtrer par mots clés
    candidate_chunks = [indexed_chunks[i] for i in indices[0]]

    scored_chunks = []
    for i, chunk in enumerate(candidate_chunks):
        text_lower = chunk['content'].lower()
        keyword_score = sum(1 for kw in keywords if kw in text_lower)
        combined_score = -distances[0][i] + keyword_weight * keyword_score  # <- utiliser i
        scored_chunks.append((combined_score, chunk))


    scored_chunks.sort(reverse=True, key=lambda x: x[0])

    context_chunks = [chunk for _, chunk in scored_chunks[:k]]

    return context_chunks



