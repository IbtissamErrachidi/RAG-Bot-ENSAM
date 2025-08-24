# Chat ENSAM Casablanca

An intelligent chatbot for answering questions about **ENSAM Casablanca**, based on a **RAG (Retrieval-Augmented Generation)** system using **Google Gemini-2.5**.


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
- Answers strictly based on the provided knowledge base.
- Simple and interactive Streamlit interface.



## Installation

1. **Clone the repository:**
```bash
git clone https://github.com/IbtissamErrachidi/RAG-Bot-ENSAM.git
cd RAG-Bot-ENSAM
