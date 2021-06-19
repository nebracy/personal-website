import os


basedir = os.path.dirname(__file__)


class Config:
    SECRET_KEY = os.getenv('FLASK_SECRET_KEY')
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_SERVER = os.getenv('FLASK_MAIL_SERVER', 'smtppro.zoho.com')
    MAIL_USERNAME = os.getenv('FLASK_MAIL_USERNAME')
    MAIL_PASSWORD = os.getenv('FLASK_MAIL_PASSWORD')
    MAIL_DEFAULT_SENDER = os.getenv('FLASK_MAIL_DEFAULT_SENDER')
    SQLALCHEMY_DATABASE_URI = os.getenv('FLASK_DB_URI', f'sqlite:///{os.path.join(basedir, "github.db")}')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    STATIC_PATH = ''


class Production(Config):
    S3_FOLDER = 'static/production'


class Staging(Config):
    S3_FOLDER = 'static'
    STATIC_PATH = '/staging'


class Development(Config):
    S3_FOLDER = None
    SECRET_KEY = 'default-secret-key'
    MAIL_SERVER = 'smtp.gmail.com'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    TESTING = True
    PRESERVE_CONTEXT_ON_EXCEPTION = False
    DEBUG = True
    ENV = 'development'
    # SERVER_NAME = 'local.nebracy.com:443'
