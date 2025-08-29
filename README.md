# Chat ENSAM Casablanca

An intelligent chatbot powered by **Retrieval-Augmented Generation (RAG)**, designed to answer students’ questions using the official content of **ENSAM Casablanca’s website**.


## Project Description

This project provides an interactive web interface (via **Streamlit**) to ask questions about ENSAM Casablanca.  
The chatbot leverages:

- Local text documents (`*.txt`) as knowledge base.
- **Vector embeddings** for semantic similarity search.
- **Gemini-2.5 LLM** for generating contextual conversational responses.
- **Conversation memory** to maintain context across questions.



## Features

- Automatic loading of text documents from the `infos_txt` folder.
- Cleaning and splitting documents into **chunks** for better retrieval.
- Indexing with **FAISS** for similarity search.
- Contextual conversation with **chat memory**.
- Automatic crawling of ENSAM Casablanca website every 45 minutes.
- Answers strictly based on the provided knowledge base.
- Simple and interactive Streamlit interface.



## Installation

1. **Clone the repository:**
```bash
git clone https://github.com/IbtissamErrachidi/RAG-Bot-ENSAM.git
cd RAG-Bot-ENSAM
``` 

2. **Create a virtual environment and install dependencies:**

```bash
python -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows

pip install -r requirements.txt
``` 


3. **Add your Gemini API key:**

- Create a .env file:
  
GEMINI_API_KEY=your_api_key_here


4. **Prepare your documents:**
   


5. **Run the App:**
   
```bash
streamlit run main.py
``` 
- Open the link displayed in your browser to interact with the chatbot.


## Project Structure

```text
chat-ensam/
│
├─ infos_txt/                  # Text files for the knowledge base
├─ vectordb_local/             # Saved FAISS index
│── infos_txt_new/             # documents retrieved by the crawler
├─ chunks.py                   # Load and split text documents
├─ cleaning.py                 # Document cleaning functions
├─ vector.py                   # Build and save the FAISS vector database
├─ retriever.py                # Retrieve the most relevant chunks
├─ rag.py                      # Gemini-2.5 conversational chain
├─ update_corpus.py            # Automatic crawling and corpus updating
├─ streamlit.py                # Streamlit interface
├─ config.py                   # API key configuration
├─ requirements.txt            # Python dependencies
└─ README.md
``` 




##  Main Modules

- **chunks.py** – loads documents and splits them into chunks.  
- **cleaning.py** – cleans the documents (removing unwanted characters, normalization, etc.).  
- **vector.py** – creates and saves the FAISS vector database from chunks.  
- **retriever.py** – retrieves the top-k most similar chunks for a query.  
- **rag.py** – builds the Gemini-2.5 conversational chain with memory.  
- **streamlit.py** – Streamlit interface for asking questions and displaying chat history.
- **update_corpus.py** – manages crawling, chunking, embedding, and replacing corpus.  



## Usage

1. Type your question in the input field.  
2. The chatbot retrieves relevant documents from the knowledge base.  
3. A contextual answer is generated strictly from the corpus.  
4. The conversation history is displayed below the chat.  


##  Configurable Parameters

- `chunk_size` and `chunk_overlap` in **chunks.py** – control text chunking for vectorization.  
- `embedding_model_name` – HuggingFace model for embeddings (default: `all-MiniLM-L6-v2`).  
- `k` in **retriever.py** – number of similar chunks to retrieve per question.  
- `model_name` in **rag.py** – Gemini model used (`gemini-2.5-flash` by default).  

---

##  Technologies

- **Python 3.10+**  
- **Streamlit** – Web interface  
- **LangChain** – RAG pipeline  
- **FAISS** – Similarity search  
- **HuggingFace Embeddings**  
- **Google Gemini LLM**  
- **python-dotenv** – API key management
- **schedule** – background automatic crawling

---

## ⚠️ Limitations

- The chatbot only answers questions present in the `infos_txt` corpus.  
- If a question has no answer in the corpus, the bot politely informs the user.  
- Requires internet access to query the Gemini LLM.  

