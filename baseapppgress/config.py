class ProdConfig(object):
    pass


class DevConfig(object):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'postgres+psycopg2://postgres:password@127.0.0.1:5432/usertable'
    POSTS_PER_PAGE = 5

