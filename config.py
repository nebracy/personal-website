import os


basedir = os.path.dirname(__file__)


class Config:
    TESTING = False
    SECRET_KEY = os.getenv('FLASK_SECRET_KEY')
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_SERVER = os.getenv('FLASK_MAIL_SERVER', 'smtppro.zoho.com')
    MAIL_USERNAME = os.getenv('FLASK_MAIL_USERNAME')
    MAIL_PASSWORD = os.getenv('FLASK_MAIL_PASSWORD')
    MAIL_DEFAULT_SENDER = os.getenv('FLASK_MAIL_DEFAULT_SENDER')
    SQLALCHEMY_DATABASE_URI = os.getenv('FLASK_DB_URI', f'sqlite:///{os.path.join(basedir, "github.db")}')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    S3_FOLDER = None


class Development(Config):
    TESTING = True
    SECRET_KEY = 'default-secret-key'
    MAIL_SERVER = 'smtp.gmail.com'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    # SERVER_NAME = 'local.nebracy.com:443'


class Staging(Config):
    TESTING = True
    S3_FOLDER = 'static/staging'


class Production(Config):
    S3_FOLDER = 'static/production'
