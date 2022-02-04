from os import getenv
from pathlib import Path


class Config:
    SECRET_KEY = getenv('FLASK_SECRET_KEY')
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_SERVER = getenv('FLASK_MAIL_SERVER', 'smtp.gmail.com')
    MAIL_USERNAME = getenv('FLASK_MAIL_USERNAME')
    MAIL_PASSWORD = getenv('FLASK_MAIL_PASSWORD')
    MAIL_DEFAULT_SENDER = getenv('FLASK_MAIL_DEFAULT_SENDER', 'contact@nicolebracy.com')
    MAIL_RECIPIENT = getenv('FLASK_MAIL_RECIPIENT')
    SQLALCHEMY_DATABASE_URI = getenv('FLASK_DB_URI', f'sqlite:///{Path(__file__).parent / "github.db"}')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    RECAPTCHA_PUBLIC_KEY = getenv('RECAPTCHA_PUBLIC_KEY')
    RECAPTCHA_PRIVATE_KEY = getenv('RECAPTCHA_PRIVATE_KEY')
    RECAPTCHA_DATA_ATTRS = {'theme': 'dark'}
    STATIC_PATH = ''


class Production(Config):
    S3_FOLDER = 'static/production'


class Staging(Config):
    S3_FOLDER = 'static'
    STATIC_PATH = '/staging'


class Development(Config):
    S3_FOLDER = None
    SECRET_KEY = 'default-secret-key'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    TESTING = True
    PRESERVE_CONTEXT_ON_EXCEPTION = False
    DEBUG = True
    ENV = 'development'
    # SERVER_NAME = 'local.nicolebracy.com:443'
