from langchain.schema import Document
import re

def cleaning(text):
    text = re.sub(r'<[^>]+>', '', text)
    text = re.sub(r'\S+@\S+\.\S+', '', text)
    text = re.sub(r'(\+?\d{1,3}[-.\s]?)?(\(?\d{2,4}\)?[-.\s]?)?[\d\s\-]{5,}', '', text)
    text = text.replace('\n\n', '<<PARA>>')
    text = text.replace('\n', '<<LINE>>')
    text = re.sub(r'\s+', ' ', text)
    text = text.replace('<<LINE>>', '\n')
    text = text.replace('<<PARA>>', '\n\n')
    text = text.strip()

    return text



# def clean_documents(documents):
#     cleaned_docs = [
#         Document(page_content=cleaning(doc.page_content), metadata=doc.metadata)
#         for doc in documents
#     ]
#     return cleaned_docs

def clean_documents(documents):
    cleaned_docs = [
        Document(page_content=doc.page_content, metadata=doc.metadata)
        for doc in documents
    ]
    return cleaned_docs



