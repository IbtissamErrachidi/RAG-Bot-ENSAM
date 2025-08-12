import os
from cleaning import clean_text_keep_lines_and_paragraphs
from chunking import chunk_text  # adapte selon où est chunk_text
from vectorisation import embed  # adapte selon où est embed

# dossier contenant les fichiers texte
folder_path = "infos_txt"

indexed_chunks = []

for filename in os.listdir(folder_path):
    if filename.endswith(".txt"):
        full_path = os.path.join(folder_path, filename)
        
        with open(full_path, encoding="utf-8") as f:
            raw_text = f.read()
        
        # 1. Nettoyer le texte
        clean_text = clean_text_keep_lines_and_paragraphs(raw_text)
        
        # 2. Découper en chunks
        chunks = chunk_text(clean_text)
        
        # 3. Embedding de tous les chunks (en batch possible selon ta fonction embed)
        embeddings = embed(chunks)  # embed doit accepter une liste de textes
        
        # 4. Construire indexed_chunks avec contenu, embedding, source, index
        for i, (chunk, emb) in enumerate(zip(chunks, embeddings)):
            indexed_chunks.append({
                "embedding": emb,
                "content": chunk,
                "source": filename,
                "chunk_index": i
            })

# indexed_chunks contient tout le contenu vectorisé avec traçabilité source/index
print(f"Total chunks vectorisés : {len(indexed_chunks)}")
