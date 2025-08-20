from langchain.text_splitter import RecursiveCharacterTextSplitter


def chunk_text(text, chunk_size=800, chunk_overlap=100, separators=None):
    if separators is None:
        separators = ["\n\n","\n", "- ", "> ", ".", "!", "?", " ", ""]

    # Initialiser le splitter avec paramètres
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        separators=separators
    )

    chunks = text_splitter.split_text(text)
    return chunks


# filename = 'infos_txt/ENSAM CASA - Projet FINCOM.txt'

# with open(filename, encoding='utf-8') as f:
#     raw_text = f.read()
# clean = clean_text_keep_lines_and_paragraphs(raw_text) 
 
# chunks = chunk_text(clean)
# for i, chunk in enumerate(chunks):
#     print(f"--- Chunk {i+1} (taille {len(chunk)}) ---")
#     print(chunk)
#     print()

