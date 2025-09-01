from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from retriever import get_retriever
from rag import build_gemini_conversational_chain
from vector import build_vectordb
from chunks import load_and_chunk_texts
from update_corpus import update_corpus1
from langchain.schema import Document
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
import os
import threading
import time
import schedule


app = FastAPI(title="ENSAM Chatbot API")
vectordb_lock = threading.Lock()
vectordb_ready = False
vectordb_path = "vectordb_local"
folder_path = "infos_txt"
embedding_model_name = "sentence-transformers/all-MiniLM-L6-v2"


vectordb = None
retriever = None
chain = None


class QueryRequest(BaseModel):
    question: str

class QueryResponse(BaseModel):
    answer: str


def load_vectordb_background():
    global vectordb, retriever, chain, vectordb_ready
    if os.path.exists(vectordb_path):
        vectordb = FAISS.load_local(
            vectordb_path,
            HuggingFaceEmbeddings(model_name=embedding_model_name),
            allow_dangerous_deserialization=True
        )
    else:
        chunks = load_and_chunk_texts(folder_path)
        docs = [Document(page_content=c.page_content, metadata=c.metadata) for c in chunks]
        vectordb = build_vectordb(docs, model_name=embedding_model_name)
    retriever = get_retriever(vectordb)
    chain = build_gemini_conversational_chain(retriever)
    vectordb_ready = True
    print("✅ Vectordb et chaîne RAG prêts !")

def scheduled_update():
    global vectordb_ready
    vectordb_ready = False
    print("🔄 Mise à jour du corpus...")
    update_corpus1()
    load_vectordb_background()
    print("✅ Vectordb mis à jour !")

def run_schedule():
    schedule.every(45).minutes.do(scheduled_update)
    while True:
        try:
            schedule.run_pending()
        except Exception as e:
            print(f"Erreur dans le scheduler : {e}")
        time.sleep(30)


threading.Thread(target=load_vectordb_background, daemon=True).start()
threading.Thread(target=run_schedule, daemon=True).start()


@app.get("/")
def root():
    return {"message": "✅ ENSAM Chatbot API is running!"}

@app.post("/chat", response_model=QueryResponse)
def chat(request: QueryRequest):
    if not vectordb_ready:
        raise HTTPException(status_code=503, detail="Chatbot is loading, please wait...")
    with vectordb_lock:
        response = chain.invoke(request.question)
    return {"answer": response["answer"]}
