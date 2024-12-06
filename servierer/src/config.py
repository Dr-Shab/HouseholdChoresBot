import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    CONFIG_PATH = os.path.join(basedir, os.getenv('CONFIG_FILE'))
    PUBLIC_ADDRESS = os.getenv('PUBLIC_ADR')
    CHECKIN_ADDRESS = os.getenv('CHECKIN_URI')

if __name__ == '__main__':
    test = Config()
    print("CONFIG_PATH:", test.CONFIG_PATH)
    print("PUBLIC_ADDRESS:", test.PUBLIC_ADDRESS)