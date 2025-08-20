from cleaning import clean_text_keep_lines_and_paragraphs
from chunking import chunk_text
from vectorisation import embed
import google.generativeai as genai


api_key = userdata.get('GEMINI_API_KEY')
genai.configure(api_key=api_key)

def rag_answer(query, retriever_func, index, indexed_chunks):
    context = retriever_func(query, index, indexed_chunks)
    print(context)

    prompt = f"""
Vous êtes un assistant spécialisé dans l'ENSAM Casablanca.
Répondez uniquement avec les informations présentes dans le contexte ci-dessous.
Ne complétez jamais avec des informations inventées.
Si l’information n’est pas dans le contexte, répondez "Je ne sais pas".

Contexte :
{context}

Question :
{query}

Réponse :
"""

    model = genai.GenerativeModel("models/gemini-2.5-pro")
    response = model.generate_content(prompt)


    return response.text
