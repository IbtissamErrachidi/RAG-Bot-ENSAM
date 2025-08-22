def get_retriever(vectordb, k=10):
    """
    vectordb: FAISS object
    k: nombre de chunks similaires à récupérer
    """
    retriever = vectordb.as_retriever(search_type="similarity", search_kwargs={"k": k})
    return retriever
