import os


class Config:
    TESTING = False
    SECRET_KEY = os.getenv('FLASK_SECRET_KEY', 'default-secret-key')
    MAIL_SERVER = os.getenv('FLASK_MAIL_SERVER', 'smtp.gmail.com')
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.getenv('FLASK_MAIL_USERNAME')
    MAIL_PASSWORD = os.getenv('FLASK_MAIL_PASSWORD')
    MAIL_DEFAULT_SENDER = os.getenv('FLASK_MAIL_DEFAULT_SENDER')
    SQLALCHEMY_DATABASE_URI = os.getenv('FLASK_DB_URI', 'sqlite:///:memory:')
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class Development(Config):
    TESTING = True
    SERVER_NAME = os.getenv('FLASK_SERVER_NAME', 'local.nebracy.com:5000')


class Staging(Config):
    TESTING = True


class Production(Config):
    SECRET_KEY = os.getenv('FLASK_SECRET_KEY')
    MAIL_SERVER = os.getenv('FLASK_MAIL_SERVER', 'smtp-relay.gmail.com')
