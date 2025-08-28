from retriever import get_retriever
from rag import build_gemini_conversational_chain
from vector import build_vectordb
import streamlit as st
from langchain.schema import Document
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from chunks import load_and_chunk_texts
import os
import threading
import time
import schedule
from update_corpus import update_corpus1
import threading

vectordb_lock = threading.Lock()


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
            with vectordb_lock:
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
    label="Question :", 
    placeholder="Posez votre question ici :",  
    key="user_input",
    on_change=send_message,
    label_visibility="hidden" 
)




    if st.button("Envoyer"):
        send_message()



def load_vectordb_to_session_thread():
    print("🔄 Préparation du chat en arrière-plan...")
    

    new_vectordb = FAISS.load_local(
        vectordb_path,
        HuggingFaceEmbeddings(model_name=embedding_model_name),
        allow_dangerous_deserialization=True
    )
    new_retriever = get_retriever(new_vectordb)
    new_chain = build_gemini_conversational_chain(new_retriever)
    

    with vectordb_lock:
        st.session_state.vectordb = new_vectordb
        st.session_state.retriever = new_retriever
        st.session_state.chain = new_chain
        st.session_state.vectordb_ready = True

    print("✅ Chat prêt avec la nouvelle version du vectordb !")

# -------------------- Background update --------------------
def scheduled_update():
    st.session_state.vectordb_ready = False
    
    update_corpus1()  
    load_vectordb_to_session_thread()  
    


def run_schedule():
    schedule.every(45).minutes.do(scheduled_update)
    while True:
        try:
            schedule.run_pending()
        except Exception as e:
            print(f"Erreur dans schedule : {e}")
        time.sleep(30)


threading.Thread(target=run_schedule, daemon=True).start()

