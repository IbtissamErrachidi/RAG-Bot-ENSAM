from huggingface_hub import InferenceClient
from cleaning import clean_text_keep_lines_and_paragraphs
from chunking import chunk_text
from vectorisation import embed

# 1️⃣ Initialiser le client
client = InferenceClient(api_key="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")

def rag_answer(question, retriever_func,folder_path, clean_func, chunk_func, embed_func):
    # 2️⃣ Récupérer les documents
    context = retriever_func(question,folder_path, clean_func, chunk_func, embed_func)

    # 3️⃣ Créer le prompt
    prompt = prompt = f"""
    Vous êtes un assistant spécialisé dans l'école ENSAM Casablanca.
    Répondez de manière claire et concise aux questions sur l'ENSAM, ses formations, ses cycles d'ingénieur et ses procédures.
    Utilisez UNIQUEMENT le contexte fourni pour répondre.
    Si la réponse ne se trouve pas dans le contexte, répondez "Je ne sais pas".

    Contexte :
    {context}

    Question :
    {question}
    """

    # 4️⃣ Appeler le modèle en mode conversationnel
    response = client.chat.completions.create(
        model="HuggingFaceH4/zephyr-7b-beta",
        messages=[
            {"role": "system", "content": "Vous êtes un assistant spécialisé dans l'école ENSAM Casablanca.Répondez uniquement à la question posée en utilisant le contexte fourni.Répondez uniquement si l’information est confirmée dans le contexte.Ne générez pas d’autres questions ou suggestions.Si la réponse n’est pas dans le contexte, répondez 'Je ne sais pas'."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=512
    )

    # 5️⃣ Retourner la réponse
    return response.choices[0].message["content"]

# Exemple d'appel
question = "Comment s'inscrire à l'ENSAM ?"
answer = rag_answer(question, retriever_func,folder_path, clean_text_keep_lines_and_paragraphs, chunk_text, embed)
print(answer)
