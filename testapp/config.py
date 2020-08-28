import os


class DevConfig():
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = "postgres+psycopg2://postgres:password@localhost:5432/usertable"
    SECRET_KEY = os.urandom(32)
