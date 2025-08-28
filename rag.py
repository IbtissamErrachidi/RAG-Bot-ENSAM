from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory
from langchain.prompts import ChatPromptTemplate
from config import GEMINI_API_KEY
import os





def build_gemini_conversational_chain(retriever, model_name="gemini-2.5-flash"):


    llm = ChatGoogleGenerativeAI(
        model=model_name,
        temperature=0,
        api_key=os.environ.get("GEMINI_API_KEY") 
    )

    memory = ConversationBufferMemory(
        memory_key="chat_history",
        return_messages=True
    )


    custom_prompt = ChatPromptTemplate.from_template("""
    Vous êtes un assistant spécialisé dans l'ENSAM Casablanca.
    Si l'utilisateur envoie une salutation ou un message amical (ex : "hi", "hello", "bonjour", "salut", "hey", "coucou"), répondez par un message d'accueil amical et standard :
    "Bonjour ! Je suis l'assistant de l'ENSAM Casablanca, comment puis-je vous aider ?"
    Répondez uniquement avec les informations présentes dans le contexte ci-dessous.
    Ne complétez jamais avec des informations inventées.
    Informez toujours l'utilisateur lorsque vous n'avez pas trouvé la réponse gentiment - soyez honnête.

    Contexte : {context}
    Historique de la conversation : {chat_history}
    Question : {question}
    Réponse :
    """)

    conv_chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=retriever,
        memory=memory,
        combine_docs_chain_kwargs={"prompt": custom_prompt}
    )

    return conv_chain
