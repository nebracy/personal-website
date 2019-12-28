import os
from nebracy import app

db_path = os.path.join(app.instance_path, 'github.db')
default_db_path = 'sqlite:///{}'.format(db_path)


class Config:
    DEBUG = True
    SECRET_KEY = os.getenv('FLASK_SECRET_KEY', 'tempkey')
    MAIL_SERVER = os.getenv('FLASK_MAIL_SERVER', 'smtp.gmail.com')
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USE_SSL = False
    MAIL_USERNAME = os.getenv('FLASK_MAIL_USERNAME')
    MAIL_PASSWORD = os.getenv('FLASK_MAIL_PASSWORD')
    SQLALCHEMY_DATABASE_URI = os.getenv('FLASK_DB_URI', default_db_path)
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevelopmentConfig(Config):
    pass


class TestingConfig(Config):
    pass


class ProductionConfig(Config):
    DEBUG = False
