import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    CONFIG_PATH = os.path.join(basedir, os.getenv('CONFIG_FILE'))
    DATABASE_URI = 'sqlite:///' + os.path.join(basedir, os.getenv('DATABASE_NAME'))
    CONFIG_API_URL = os.getenv("DH_API")

if __name__ == '__main__':
    test = Config()
    print("CONFIG_PATH:", test.CONFIG_PATH)
    print("DATABASE_URI:", test.DATABASE_URI)
