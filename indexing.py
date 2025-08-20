import os
import numpy as np

def prepare_indexed_chunks(folder_path, clean_func, chunk_func, embed_func):
    indexed_chunks = []


    for filename in os.listdir(folder_path):
        if filename.endswith(".txt"):
            full_path = os.path.join(folder_path, filename)
            with open(full_path, encoding="utf-8") as f:
                raw_text = f.read()

            clean_text = clean_func(raw_text)

            chunks = chunk_func(clean_text)
            combined_texts = [f"{filename} {chunk}" for chunk in chunks]
            embeddings = embed_func(combined_texts).detach().cpu().numpy().astype(np.float32)

            norms = np.linalg.norm(embeddings, axis=1, keepdims=True)
            embeddings = embeddings / norms

            for i, (chunk, emb) in enumerate(zip(chunks, embeddings)):
                indexed_chunks.append({
                    "embedding": emb,
                    "content": chunk,
                    "source": filename,
                    "chunk_index": i
                })
    return indexed_chunks

