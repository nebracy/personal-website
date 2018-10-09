class Config:
    SECRET_KEY = 'testkey'
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USE_SSL = False
    MAIL_USERNAME = ''
    MAIL_PASSWORD = ''


class ProductionConfig(Config):
    pass


class TestConfig(Config):
    pass
