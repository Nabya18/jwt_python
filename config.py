import os
from datetime import datetime, timedelta

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or '17d12f754a0b418eaab9eb3ef876165e'
    DATABASE_PATH = os.environ.get('DATABASE_PATH') or 'urls.db'
    JWT_EXPIRATION_DELTA = timedelta(hours=1)

    DEBUG = False
    TESTING = False

    SHORT_URL_LENGTH = 6
    MAX_URL_LENGTH = 2048

class DevelopmentConfig(Config):
    DEBUG = True
    DATABASE_PATH = 'dev_urls.db'

class TestingConfig(Config):
    TESTING = True
    DATABASE_PATH = ':memory' #use in-memory sqlite
    SECRET_KEY = 'test-secret-key'

class ProductionConfig(Config):
    SECRET_KEY = os.environ.get('SECRET_KEY')
    DATABASE_PATH = os.environ.get('DATABASE_PATH') or 'prod_urls.db'

    if not SECRET_KEY:
        raise ValueError("No SECRET_KEY set for production environment")


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}