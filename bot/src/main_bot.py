from datetime import datetime
import random
import bot
import helpers
from config import Config
import argparse
import requests

DB_API_URL = Config.DB_API_URL
CONFIG_API_URL = Config.CONFIG_API_URL

TODAY = datetime.today()

duties_logger = helpers.setup_logger('duties_logger')
service_logger = helpers.setup_logger('service_logger')

saturday_text = Config.SATURDAY_TEXT
monday_text = Config.MONDAY_TEXT
tuesday_text = Config.TUESDAY_TEXT

def parse_arguments():
    parser = argparse.ArgumentParser(description="Run the main application with specified options.")
    parser.add_argument("-d", "--day", type=str,
                        help="Specify the weekday (e.g., Monday, Tuesday, etc.)")
    parser.add_argument("-f", "--full", action="store_true",
                        help="Enable full debugging output")
    parser.add_argument("-w", "--waittime", type=int,
                        help="Wait time between actions in seconds")
    return parser.parse_args()

def main(waittime):
    args = parse_arguments()
    if args.day:
        weekday = args.day
    else:
        weekday = TODAY.strftime('%A')
    if args.full:
        headfull = args.full
    else:
        headfull = None

    config_response = requests.get(CONFIG_API_URL + "/get_em")
    config_data = config_response.json()
    workers, tokens, aemtli, entsorgen = config_data
    duties_logger.info(f'loaded list of workers: {workers} and ämtli: {aemtli}')

    try:
        driver_og = bot.createBrowserInstance(website='https://web.whatsapp.com', headfull=headfull,
                                              wait_time_instance=waittime)
        duties_logger.info('Opened the browser')

        if weekday == 'Saturday':
            wikilinks_response = requests.get(CONFIG_API_URL + "/wiki_how")
            wiki_links = wikilinks_response.json()

            for contact in workers:
                job = aemtli[workers.index(contact)]
                token = None
                for token_id in tokens:
                    if tokens.get(token_id) == contact:
                        token = token_id
                        break
                if token is None:
                    text = "Error token not found please contact your local admin"
                    bot.sendMessage(driver=driver_og, contact=contact, message=text)
                    duties_logger.info("token not found")
                    break

                tokenlink_response = requests.post(CONFIG_API_URL + "/get_token_link", json={'token': token})
                link = tokenlink_response.text
                wikilink = random.choice(wiki_links[job])

                text = saturday_text.format(job=job, link=link, wikilink=wikilink)
                bot.sendMessage(driver=driver_og, contact=contact, message=text, wait_time_send=waittime / 10)
                duties_logger.info(f'{contact} received the message')

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


        elif weekday == 'Monday':
            for contact in workers:
                job = aemtli[workers.index(contact)]
                text = monday_text.format(job=job)
                bot.sendMessage(driver=driver_og, contact=contact, message=text, wait_time_send=waittime / 10)
                duties_logger.info(f'{contact} received the message')

            check_work = requests.get(DB_API_URL + "/")
            if check_work.status_code == 200:
                duties_logger.info('checked who did work and updated DB')
            else:
                duties_logger.info('work check did not work')

            storem = requests.get(CONFIG_API_URL + "/store_em")
            if storem.status_code == 200:
                duties_logger.info("saved list of workers and ämtlis")
            else:
                duties_logger.info(f"storing workers and ämtlis failed")


        elif weekday == 'Tuesday':
            abfall = entsorgen[0]
            worker = workers[aemtli.index("Scheiss entsorgen")]
            text = tuesday_text.format(abfall=abfall)
            bot.sendMessage(driver=driver_og, contact=worker, message=text, wait_time_send=waittime / 10)

            duties_logger.info(f'{worker} received the message')

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

        driver_og.quit()
        duties_logger.info('Closed the browser')
        return True

    except Exception as e:
        duties_logger.error(f"Something didn't work, here is the stacktrace:\n{str(e)} "
                            f"with a write/send wait time of: {waittime/10} seconds\n")
        return False

if __name__ == "__main__":
    counter = 1
    result = False
    while counter < 4 and not result:
        service_logger.info(f'Starting Whatsappbot, round: {counter} '
                            f'with a load wait time of: {counter * 150} seconds\n')
        result = main(waittime=counter * 150)
        counter += 1
