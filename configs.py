import os


class Config:
    DEBUG = True
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    LOG_PATH = os.path.join(BASE_DIR, "logs")
    LOG_FORMAT = '%(asctime)s  %(name)s [%(levelname)s] %(message)s'