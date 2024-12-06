from datetime import datetime
import random
import helpers
from config import Config
import requests

DB_API_URL = Config.DB_API_URL
CONFIG_API_URL = Config.CONFIG_API_URL

TODAY = datetime.today()

duties_logger = helpers.setup_logger('duties_logger')

saturday_text = Config.SATURDAY_TEXT
monday_text = Config.MONDAY_TEXT
tuesday_text = Config.TUESDAY_TEXT

def main():
    config_response = requests.get(CONFIG_API_URL + "/get_em")
    config_data = config_response.json()
    workers, tokens, aemtli, entsorgen = config_data

    duties_logger.info(config_data)

    wikilinks_response = requests.get(CONFIG_API_URL + "/wiki_how")
    wiki_links = wikilinks_response.json()

    duties_logger.info(wiki_links)

    for contact in workers:
        job = aemtli[workers.index(contact)]
        token = None
        for token_id in tokens:
            if tokens.get(token_id) == contact:
                token = token_id
                break
        if token is None:
            duties_logger.info("token not found")
            break

        tokenlink_response = requests.post(CONFIG_API_URL + "/get_token_link", json={'token': token})
        link = tokenlink_response.text
        wikilink = random.choice(wiki_links[job])

        duties_logger.info(f"token_link: {link}")
        duties_logger.info(f"wiki_link: {wikilink}")

    duties_logger.info(wiki_links)

    rotate = requests.post(CONFIG_API_URL + "/rotate_list", json={"category": "workers"})
    if rotate.status_code == 200:
        duties_logger.info("rotated list of workers")
    else:
        duties_logger.info(f"rotating workers failed")

    storem = requests.get(CONFIG_API_URL + "/store_em")
    if storem.status_code == 200:
        duties_logger.info("saved list of workers and ämtlis")
    else:
        duties_logger.info(f"storing workers and ämtlis failed")

    duties_logger.info("finished block one")

    for contact in workers:
        job = aemtli[workers.index(contact)]
        duties_logger.info(job)

    check_work = requests.get(DB_API_URL + "/check_work")
    if check_work:
        duties_logger.info('checked who did work and updated DB')
    else:
        duties_logger.info('work check did not work')

    storem = requests.get(CONFIG_API_URL + "/store_em")
    if storem.status_code == 200:
        duties_logger.info("saved list of workers and ämtlis")
    else:
        duties_logger.info(f"storing workers and ämtlis failed")

    duties_logger.info("finished block two")

    abfall = entsorgen[0]
    worker = workers[aemtli.index("Scheiss entsorgen")]
    duties_logger.info(f'{worker} received the message: ´{abfall}')

    rotate = requests.post(CONFIG_API_URL + "/rotate_list", json={"category": "entsorgung"})
    if rotate.status_code == 200:
        duties_logger.info("rotated list of entsorgungsplan")
    else:
        duties_logger.info(f"rotating entsorgung failed")

    storem = requests.get(CONFIG_API_URL + "/store_em")
    if storem.status_code == 200:
        duties_logger.info("saved list of workers and ämtlis")
    else:
        duties_logger.info(f"storing workers and ämtlis failed")

    duties_logger.info("finished all tests")

if __name__ == "__main__":
    main()
