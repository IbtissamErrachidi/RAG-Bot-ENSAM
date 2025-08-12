from faiss import create_faiss_index
from answer import search_and_display,generate_answer
from indexing import prepare_indexed_chunks
from cleaning import clean_text_keep_lines_and_paragraphs
from chunking import chunk_text
from vectorisation import embed


def rag_chatbot(folder_path, query):
    indexed_chunks = prepare_indexed_chunks(
        folder_path,
        clean_text_keep_lines_and_paragraphs,
        chunk_text,
        embed
    )
    index = create_faiss_index(indexed_chunks) 
    context_chunks = search_and_display(query, index, indexed_chunks, k=5)
    return generate_answer(context_chunks, query)



if __name__ == "__main__":
    question = "Quand aura lieu le prochain séminaire scientifique à l’ENSAM Casablanca ?"
    response = rag_chatbot(folder_path, question)
    print("Réponse générée :\n", response)