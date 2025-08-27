import os
import shutil
from crawler import run_crawler
from chunks import load_and_chunk_texts
from vector import build_vectordb

def update_corpus1():
    tmp_dir = "infos_txt_new"
    prod_dir = "infos_txt"

    # Clean temp folder
    if os.path.exists(tmp_dir):
        shutil.rmtree(tmp_dir)
    os.makedirs(tmp_dir, exist_ok=True)

    run_crawler(output_dir=tmp_dir)

    chunks = load_and_chunk_texts(tmp_dir)
    if not chunks:
        print("⚠️ Aucun chunk généré, le corpus n’a pas été mis à jour.")
        return
    vectordb = build_vectordb(chunks, model_name="sentence-transformers/all-MiniLM-L6-v2")
    vectordb.save_local("vectordb_local_new")

    # Swap directories atomically
    if os.path.exists(prod_dir):
        shutil.rmtree(prod_dir)
    os.rename(tmp_dir, prod_dir)

    if os.path.exists("vectordb_local"):
        shutil.rmtree("vectordb_local")
    os.rename("vectordb_local_new", "vectordb_local")
