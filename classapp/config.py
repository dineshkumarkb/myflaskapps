import os

class DevConfig():
    EXPLAIN_TEMPLATE_LOADING = False
    SECRET_KEY = os.urandom(32)
    SQLALCHEMY_DATABASE_URI = 'postgres+psycopg2://postgres:password@127.0.0.1:5432/usertable'

