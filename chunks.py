from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from wrap_documents import clean


def load_and_chunk_texts(folder_path, chunk_size=800, chunk_overlap=100, separators=None):

    loader = DirectoryLoader(
        folder_path,
        glob="*.txt",
        loader_cls=lambda path: TextLoader(path, encoding="utf-8")  # <- encodage fixé
    )
    documents = loader.load()

    if separators is None:
        separators = ["\n\n","\n", "- ", "> ", ".", "!", "?", " ", ""]

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        separators=separators
    )

    documents = clean(documents)

    chunks = text_splitter.split_documents(documents)
    return chunks

