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

    def process_page(url, soup):
        image_exts = ('.jpeg', '.jpg', '.png', '.gif', '.bmp', '.svg', '.webp')
        pdf_ext = '.pdf'

        for a in soup.find_all('a', href=True):
            href = a['href']
            abs_href = urljoin(url, href)

            href_lower = href.lower()

            if href_lower.endswith(pdf_ext):
                # Remplacer le lien PDF par texte + (PDF: url)
                new_text = f"{a.get_text(strip=True)} (PDF: {abs_href})"
                a.replace_with(new_text)

            elif href_lower.endswith(image_exts):
                # Pour les images, on insère le texte spécial devant le texte du lien
                # Ex: "->Télécharger l'affiche<-" devient
                # "Voici le lien vers l'image : URL ->Télécharger l'affiche<-"

                original_text = a.get_text(strip=True)
                new_text = f"Voici le lien vers l'image : {abs_href} {original_text}"
                a.replace_with(new_text)

        # Extraire le texte modifié
        if soup.body:
            text = soup.body.get_text(separator='\n', strip=True)
        else:
            text = ''
        return text

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

            text = process_page(url, soup)

            if text.strip():
                file_path = os.path.join(output_dir, f"{title}.txt")
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(text)
                print(f"Texte sauvegardé avec liens PDF et images insérés : {file_path}")
            else:
                print("Page vide, pas de fichier créé.")

            # Ajouter les liens à visiter
            for link in soup.find_all('a', href=True):
                abs_link = urljoin(url, link['href'])
                if abs_link.startswith(start_url) and abs_link not in visited:
                    to_visit.append(abs_link)

        except Exception as e:
            print(f'Failed to crawl {url}: {e}')
        visited.add(url)

if __name__ == '__main__':
    run_crawler()
