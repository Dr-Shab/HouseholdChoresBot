import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    CONFIG_PATH = os.path.join(basedir, os.getenv('CONFIG_FILE'))
    PROFILE_PATH = os.path.join(basedir, os.getenv('PROFILE_DIR'))
    CHROMIUM_PATH = os.getenv('CHROMIUM_BINARY')
    DB_API_URL = os.getenv("DB_API")
    CONFIG_API_URL = os.getenv("DH_API")

    PUBLIC_ADDRESS = os.getenv('PUBLIC_ADR')

    SATURDAY_TEXT = "*Reminder* Sie haben noch 48h Zeit um " \
                    "*{job}* zu erledigen! Bereits *erledigt?* Klicke folgenden Link: {link} " \
                    "Brauchen Sie *Unterstützung?* " \
                    "{wikilink}"

    MONDAY_TEXT = "Dringende Mitteilung vom Amt f.h. Harm. & allg. Wohl.bef.: Sie müssen diese Woche: *{job}*"

    TUESDAY_TEXT = "Kleiner Hinweis vom Amt f.h. Harmonie und allg. Wohlbefinden: Morgen wird {abfall} entsorgt :)"

if __name__ == '__main__':
    test = Config()
    print("CONFIG_PATH:", test.CONFIG_PATH)
    print("PROFILE_PATH:", test.PROFILE_PATH)
    print("CHROMIUM_PATH:", test.CHROMIUM_PATH)
    print("DB_API_URL", test.DB_API_URL)
    print("CONFIG_API_URL", test.CONFIG_API_URL)
    print("PUBLIC_ADDRESS:", test.PUBLIC_ADDRESS)