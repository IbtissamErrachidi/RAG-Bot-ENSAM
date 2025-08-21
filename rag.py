from cleaning import clean_text_keep_lines_and_paragraphs
from chunking import chunk_text
from vectorisation import embed
import google.generativeai as genai
import os
from dotenv import load_dotenv
from langchain.memory import ConversationBufferMemory

load_dotenv()


api_key = os.getenv("GEMINI_API_KEY")

genai.configure(api_key=api_key)



memory = ConversationBufferMemory(
    memory_key="chat_history",
    return_messages=True
)




def rag_answer(query, retriever_func, index, indexed_chunks):

    context = retriever_func(query, index, indexed_chunks)
    print("Context:", context)

    past_messages = memory.load_memory_variables({}).get("chat_history", [])

    history_text = ""
    for msg in past_messages:
        role = "Utilisateur" if msg.type == "human" else "Assistant"
        history_text += f"{role}: {msg.content}\n"


    prompt = f"""
Vous êtes un assistant spécialisé dans l'ENSAM Casablanca.
Répondez uniquement avec les informations présentes dans le contexte ci-dessous.
Ne complétez jamais avec des informations inventées.
Si l’information n’est pas dans le contexte, répondez "Je ne sais pas".

Historique de conversation :
{history_text}

Contexte :
{context}

Question :
{query}

Réponse :
"""

    model = genai.GenerativeModel("models/gemini-2.5-pro")
    response = model.generate_content(prompt)


    memory.save_context({"input": query}, {"output": response.text})

    return response.text

