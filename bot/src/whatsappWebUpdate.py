import argparse
from bot.src import bot, helpers
from datetime import datetime
import requests
import os

CONFIG_API_URL = os.getenv("DH_API")

if __name__ == '__main__':
    TODAY = datetime.today()

    update_logger = helpers.setup_logger('update_logger')

    config_response = requests.get(CONFIG_API_URL + "/get_em")
    config_data = config_response.json()
    workers, tokens, aemtli, entsorgen = config_data

    update_logger.info(f'loaded list of workers: {workers} and ämtli: {aemtli}')

    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--full", action="store_true",
                        help="show what's happening")
    args = parser.parse_args()
    if args.full:
        headfull = args.full
    else:
        headfull = None

    driver_og = bot.createBrowserInstance(website='https://web.whatsapp.com', headfull=headfull, wait_time_instance=120)
    update_logger.info('Opened the browser')

    for worker in workers:
        bot.selectContact(driver=driver_og, contact=worker, wait_time_select=120)
        update_logger.info(f"Updated messages of {worker}")
    update_logger.info('Closed the browser')