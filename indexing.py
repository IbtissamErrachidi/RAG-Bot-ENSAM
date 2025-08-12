import os
import numpy as np

def prepare_indexed_chunks(folder_path, clean_func, chunk_func, embed_func):
    indexed_chunks = []
    

    for filename in os.listdir(folder_path):
        if filename.endswith(".txt"):
            full_path = os.path.join(folder_path, filename)
            with open(full_path, encoding="utf-8") as f:
                raw_text = f.read()

            # 1. Nettoyer le texte
            clean_text = clean_func(raw_text)

            # 2. Découper en chunks
            chunks = chunk_func(clean_text)

            # 3. Embedding + conversion directe en numpy float32
            embeddings = embed_func(chunks).detach().cpu().numpy().astype(np.float32)

            # 4. Normalisation
            norms = np.linalg.norm(embeddings, axis=1, keepdims=True)
            embeddings = embeddings / norms


            # 5. Stockage
            for i, (chunk, emb) in enumerate(zip(chunks, embeddings)):
                indexed_chunks.append({
                    "embedding": emb,  
                    "content": chunk,
                    "source": filename,
                    "chunk_index": i
                })

    print(f"Total chunks vectorisés : {len(indexed_chunks)}")
    return indexed_chunks
