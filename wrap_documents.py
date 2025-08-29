from langchain.schema import Document

def clean(documents):
    cleaned_docs = [
        Document(page_content=doc.page_content, metadata=doc.metadata)
        for doc in documents
    ]
    return cleaned_docs



