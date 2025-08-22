from retriever import get_retriever
from rag import build_gemini_conversational_chain
from vector import build_vectordb
import streamlit as st
from langchain.schema import Document
from langchain.vectorstores import FAISS
from langchain.embeddings import HuggingFaceEmbeddings
from chunks import load_and_chunk_texts
import os


st.set_page_config(page_title="💬 Chat ENSAM", page_icon="🎓", layout="wide")
st.title("💬 Chat ENSAM Casablanca")


folder_path = "infos_txt"
vectordb_path = "vectordb_local"
embedding_model_name = "sentence-transformers/all-MiniLM-L6-v2"


if "vectordb_ready" not in st.session_state:
    st.session_state.vectordb_ready = False
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "user_input" not in st.session_state:
    st.session_state.user_input = ""


if not st.session_state.vectordb_ready:
    with st.spinner("🔄 Préparation du chat, veuillez patienter..."):
        if os.path.exists(vectordb_path):
            st.session_state.vectordb = FAISS.load_local(
                vectordb_path,
                HuggingFaceEmbeddings(model_name=embedding_model_name),
                allow_dangerous_deserialization=True
            )
        else:
            chunks = load_and_chunk_texts(folder_path)
            docs = [Document(page_content=chunk.page_content, metadata=chunk.metadata) for chunk in chunks]
            st.session_state.vectordb = build_vectordb(docs, model_name=embedding_model_name)

        st.session_state.retriever = get_retriever(st.session_state.vectordb)
        st.session_state.chain = build_gemini_conversational_chain(st.session_state.retriever)
        st.session_state.vectordb_ready = True


def send_message():
    query = st.session_state.user_input
    if query:
        with st.spinner("💬 Chat en cours..."):
            response = st.session_state.chain.run(query)
           
            st.session_state.chat_history.append((query, response))
        st.session_state.user_input = ""  

if st.session_state.vectordb_ready:
    st.success("✅ Chat prêt ! Vous pouvez poser votre question ci-dessous.")

    


    for q, a in st.session_state.chat_history:
        st.markdown(f"**Vous :** {q}")
        st.markdown(f"**Réponse :** {a}")
        st.markdown("---")

    st.text_input(
        label="",  
        placeholder="Posez votre question ici :",  
        key="user_input",
        on_change=send_message
    )



    if st.button("Envoyer"):
        send_message()
