import schedule
import time
import update_corpus1 from update_corpus


def update_corpus():
    update_corpus1()


# Schedule update every 45 minutes
schedule.every(45).minutes.do(update_corpus)


while True:
    schedule.run_pending()
    time.sleep(1)
