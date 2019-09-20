import os
class Config:
    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://wecode:190998st@localhost/pitches'
    SECRET_KEY='123'
class ProdConfig(Config):
    pass


class DevConfig(Config):
    DEBUG = True

config_options = {
'development':DevConfig,
'production':ProdConfig
}    