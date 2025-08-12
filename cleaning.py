import re

def clean_text_keep_urls(text):
    # Trouver toutes les URLs (http, https)
    url_pattern = r'https?://[^\s,;]+'
    urls = re.findall(url_pattern, text)

    # Supprimer les URLs du texte
    text_no_urls = re.sub(url_pattern, '', text)

    # Nettoyer le texte restant

    # Supprimer balises HTML
    text_no_urls = re.sub(r'<[^>]+>', '', text_no_urls)

    # Supprimer emails
    text_no_urls = re.sub(r'\S+@\S+\.\S+', '', text_no_urls)

    # Supprimer numéros de téléphone (formats simples)
    text_no_urls = re.sub(r'(\+?\d{1,3}[-.\s]?)?(\(?\d{2,4}\)?[-.\s]?)?[\d\s\-]{5,}', '', text_no_urls)

    # Remplacer espaces multiples, retours à la ligne multiples par un espace simple
    text_no_urls = re.sub(r'\s+', ' ', text_no_urls)

    # Supprimer caractères invisibles / non imprimables
    text_no_urls = ''.join(ch for ch in text_no_urls if ch.isprintable() or ch.isspace())

    # Supprimer espaces en début/fin
    text_no_urls = text_no_urls.strip()

    # Réinjecter les URLs, une par ligne à la fin du texte nettoyé
    if urls:
        clean_text = text_no_urls + '\n' + '\n'.join(urls)
    else:
        clean_text = text_no_urls

    return clean_text


filename = 'infos_txt/ENSAM_lista_complementaire_admis_prep_int.txt.txt'

with open(filename, encoding='utf-8') as f:
    raw_text = f.read()


cleaned = clean_text_keep_urls(raw_text)
print(cleaned)
