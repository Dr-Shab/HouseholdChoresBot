import json
import random, string
import uuid

import requests
from bs4 import BeautifulSoup as beausoup
import re
from config import Config

CONFIG_FILE = Config.CONFIG_PATH
ADDRESS = Config.PUBLIC_ADDRESS
CHECKADR = Config.CHECKIN_ADDRESS


def getem():
    with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
        data = json.load(f)

    workers = data['workers']
    tokens = data['tokens']
    aemtli = data['aemtli']
    entsorgen = data['entsorgungsplan']
    return workers, tokens, aemtli, entsorgen

def storethem(workers, tokens, aemtli, entsorgen):
    try:
        data = {'workers': workers, 'tokens': tokens, 'aemtli': aemtli, 'entsorgungsplan': entsorgen}
        with open(CONFIG_FILE, 'w', encoding='utf-8') as file:
            json.dump(data, file, ensure_ascii=False, indent=4)

        return True
    except Exception as e:
        return False

def generate_token(name, fake_salt):
    return uuid.uuid5(uuid.NAMESPACE_DNS, name+fake_salt).hex

def randomword(length):
   letters = string.ascii_lowercase
   return ''.join(random.choice(letters) for i in range(length))

def store_tokens(workers, aemtli, entsorgen):
    randomstring = randomword(10)
    tokens = {}
    for name in workers:
        tokens[generate_token(name, randomstring)] = name
    storethem(workers, tokens, aemtli, entsorgen)

def generate_link(token):
    link = ADDRESS + CHECKADR + token
    return link

def rotateList(lst):
    lst.insert(0, lst.pop())


def aemtli_cleaner(aemtli):
    new_aemtli = aemtli.copy()
    for idx, amt in enumerate(new_aemtli):
        if "+" in amt:
            new_aemtli.pop(idx)
            new = amt.replace("+ ", "")
            new_aemtli.insert(idx, new)

    # formating for the url
    for idx, amt in enumerate(new_aemtli):
        new_aemtli.pop(idx)
        new = amt.replace(" ", "+")
        new_aemtli.insert(idx, new)
    return new_aemtli


def wiki_how_help_links(amt):
    response = requests.get(f'https://de.wikihow.com/wikiHowTo?search={amt}')
    soup = beausoup(response.text, 'html.parser')

    link_list =[]
    for link in soup.find_all('a',
                              attrs={'href': re.compile("^https://")}):
        # display the actual urls
        link_list.append(link.get('href'))

    list_copy = link_list.copy()
    for link in list_copy:
        if link[:23] != 'https://de.wikihow.com/' or 'Experten' in link or 'Kategorie' in link:
            link_list.remove(link)

    return link_list

if __name__ == '__main__':
    aemtli = getem()[2]
    print(aemtli)

    workers, tokens, aemtli, entsorgen = getem()
    store_tokens(workers, aemtli, entsorgen)
    for contact in workers:
        work = aemtli[workers.index(contact)]
        token = None
        for token_id in tokens:
            if tokens.get(token_id) == contact:
                token = token_id
                break
        if token is None:
            text = "Error token not found please contact your local admin"
            break
        link = generate_link(token)
        text = f"*Reminder* Sie haben noch 24h Zeit um" \
               f"*{work}* zu erledigen! Bereits erledigt? klicke folgenden Link: {link}" \
               f"Brauchen Sie Unterstützung? " \
               f"random wiki link"

        print(link)