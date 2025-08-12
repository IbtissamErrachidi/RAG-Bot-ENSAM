import schedule
import time
from crawler import run_crawler
from clear import clear_output_folder

def update_corpus():
    print("Nettoyage du dossier avant mise à jour...")
    clear_output_folder()
    print("Lancement du crawling...")
    run_crawler()
    print("Mise à jour terminée.")


# Planifie la mise à jour toutes les 2 minutes
schedule.every(2).minutes.do(update_corpus)

print("Scheduler lancé. Ctrl+C pour arrêter.")

while True:
    schedule.run_pending()
    time.sleep(1)
