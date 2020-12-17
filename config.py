import os


class Config:
    TESTING = False
    SECRET_KEY = os.getenv('FLASK_SECRET_KEY', 'default-secret-key')
    MAIL_SERVER = os.getenv('FLASK_MAIL_SERVER', 'smtp.gmail.com')
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USE_SSL = False
    MAIL_USERNAME = os.getenv('FLASK_MAIL_USERNAME')
    MAIL_PASSWORD = os.getenv('FLASK_MAIL_PASSWORD')
    SQLALCHEMY_DATABASE_URI = os.getenv('FLASK_DB_URI', 'sqlite:///:memory:')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SERVER_NAME = os.getenv('FLASK_SERVER_NAME', 'nebracy.com')


class Development(Config):
    TESTING = True
    SERVER_NAME = 'local.nebracy.com'   # Add/Update hosts file


class Staging(Config):
    pass


class Production(Config):
    pass
