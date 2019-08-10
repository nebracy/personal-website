import os
from nebracy import app

db_path = os.path.join(app.instance_path, 'github.db')


class Config:
    DEBUG = True
    SECRET_KEY = 'testkey'
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USE_SSL = False
    MAIL_USERNAME = ''
    MAIL_PASSWORD = ''
    SQLALCHEMY_DATABASE_URI = 'sqlite:///{}'.format(db_path)
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevelopmentConfig(Config):
    pass


class TestingConfig(Config):
    pass


class ProductionConfig(Config):
    DEBUG = False
