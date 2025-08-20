import numpy as np
import faiss

def create_faiss_index(indexed_chunks):
    embeddings_np = np.array([c["embedding"] for c in indexed_chunks], dtype="float32")
    dimension = embeddings_np.shape[1]

    index = faiss.IndexFlatL2(dimension)
    index.add(embeddings_np)

    return index

