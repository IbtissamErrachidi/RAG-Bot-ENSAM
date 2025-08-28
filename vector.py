from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
import os


def build_vectordb(chunks, model_name="all-MiniLM-L6-v2"):
    """
    chunks: liste de Document
    model_name: nom du modèle pour embeddings
    """
    embeddings = HuggingFaceEmbeddings(model_name=model_name)
    vectordb = FAISS.from_documents(chunks, embeddings) 
 
    save_path = "vectordb_local"
    os.makedirs(save_path, exist_ok=True)
    vectordb.save_local(save_path)
    print(f"Vectordb sauvegardé localement dans : {save_path}")

    return vectordb

