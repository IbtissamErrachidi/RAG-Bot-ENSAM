import os
import re
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

def run_crawler():
    start_url = 'https://ensam-casa.ma/'
    visited = set()
    to_visit = [start_url]

    output_dir = 'infos_txt'
    os.makedirs(output_dir, exist_ok=True)

    def clean_filename(s):
        s = re.sub(r'[\\/*?:"<>|]', '', s)
        s = s.strip()
        if len(s) > 100:
            s = s[:100]
        return s

    while to_visit:
        url = to_visit.pop(0)
        if url in visited:
            continue
        print(f'Crawling: {url}')
        try:
            response = requests.get(url)
            response.encoding = 'utf-8'
            soup = BeautifulSoup(response.text, 'html.parser')

            title = soup.title.string if soup.title else 'no_title'
            title = clean_filename(title)

            # Chercher un lien PDF sur la page
            pdf_link = None
            for a in soup.find_all('a', href=True):
                href = a['href']
                if href.lower().endswith('.pdf'):
                    pdf_link = urljoin(url, href)
                    break

            if pdf_link:
                # Si PDF trouvé, on sauve juste le lien dans un fichier texte
                file_path = os.path.join(output_dir, f"{title}_pdf_link.txt")
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(pdf_link)
                print(f"PDF trouvé, sauvegarde du lien: {file_path}")
            else:
                # Sinon, extraire le texte
                if soup.body:
                    text = soup.body.get_text(separator='\n', strip=True)
                else:
                    text = ''

                if text:
                    file_path = os.path.join(output_dir, f"{title}.txt")
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(text)
                    print(f"Texte sauvegardé: {file_path}")
                else:
                    print("Page sans texte ni PDF, pas de fichier créé.")

            # Ajouter les liens à visiter
            for link in soup.find_all('a', href=True):
                abs_link = urljoin(url, link['href'])
                if abs_link.startswith(start_url) and abs_link not in visited:
                    to_visit.append(abs_link)

        except Exception as e:
            print(f'Failed to crawl {url}: {e}')
        visited.add(url)
