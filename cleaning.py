import re

def clean_text_keep_lines_and_paragraphs(text):
    # 1. Supprimer balises HTML
    text = re.sub(r'<[^>]+>', '', text)

    # 2. Supprimer emails
    text = re.sub(r'\S+@\S+\.\S+', '', text)

    # 3. Supprimer numéros de téléphone (formats simples)
    text = re.sub(r'(\+?\d{1,3}[-.\s]?)?(\(?\d{2,4}\)?[-.\s]?)?[\d\s\-]{5,}', '', text)

    # 4. Protéger doubles sauts de ligne
    text = text.replace('\n\n', '<<PARA>>')

    # 5. Protéger sauts de ligne simples restants
    text = text.replace('\n', '<<LINE>>')

    # 6. Remplacer tous les autres espaces blancs par un espace
    text = re.sub(r'\s+', ' ', text)

    # 7. Remettre les sauts simples
    text = text.replace('<<LINE>>', '\n')

    # 8. Remettre les doubles sauts de ligne
    text = text.replace('<<PARA>>', '\n\n')

    # 9. Supprimer espaces en début/fin
    text = text.strip()

    return text


# filename = 'infos_txt/ENSAM CASA - Projet FINCOM.txt'

# with open(filename, encoding='utf-8') as f:
#     raw_text = f.read()
    
#print(clean_text_keep_lines_and_paragraphs(raw_text))
