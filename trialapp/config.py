import os

class DevConfig(object):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'postgres+psycopg2://postgres:password@127.0.0.1:5432/restaurantable'
    SECRET_KEY = os.urandom(32)


class ProdConfig(object):
    pass