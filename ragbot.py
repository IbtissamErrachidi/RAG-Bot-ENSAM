from indexing import prepare_indexed_chunks
from faiss import create_faiss_index
from answer import search_and_display
import requests

def check_link(url):
    try:
        response = requests.head(url, allow_redirects=True, timeout=5)
        return response.status_code == 200
    except:
        return False

def filter_links(context):
    import re
    links = re.findall(r'https?://\S+', context)
    valid_links = [link for link in links if check_link(link)]
    for link in links:
        if link not in valid_links:
            context = context.replace(link, "[Lien invalide ou obsolète]")
    return context


def retriever_func(query,folder_path, clean_func, chunk_func, embed_func):
  indexed_chunks = prepare_indexed_chunks(folder_path, clean_func, chunk_func, embed_func)
  index = create_faiss_index(indexed_chunks)
  chunks = search_and_display(query, index, indexed_chunks, k=5)
  context = " ".join([c['content'].replace("Voir plus", "").replace("Termes et conditions", "") for c in chunks])
  context = filter_links(context)
  return context