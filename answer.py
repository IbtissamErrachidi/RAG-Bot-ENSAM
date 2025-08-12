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

# --- Modèle génératif (ex: T5) ---
gen_tokenizer = AutoTokenizer.from_pretrained("google/flan-t5-base")
gen_model = AutoModelForSeq2SeqLM.from_pretrained("google/flan-t5-base")

    def generate_answer(context_chunks, question):

    # Construire un prompt avec les chunks récupérés
    context_text = "\n---\n".join([chunk['content'] for chunk in context_chunks])
    prompt = f"Informations :\n{context_text}\n\nQuestion : {question}\nRéponse :"
    
    inputs = gen_tokenizer(prompt, return_tensors="pt", truncation=True, max_length=512)
    outputs = gen_model.generate(**inputs, max_length=256, num_beams=5, no_repeat_ngram_size=2, early_stopping=True)
    answer = gen_tokenizer.decode(outputs[0], skip_special_tokens=True)
    
    return answer
