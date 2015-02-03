import os
basedir = os.path.abspath(os.path.dirname(__file__))

#db
SQLALCHEMY_DATABASE_URI = 'postgresql://xxx:xxx@localhost:5432/m_hero'
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')

#Markov chaine pow
N = 2

#twitter
CONSUMER_KEY = 'xxxx'
CONSUMER_SECRET = 'xxxx'
ACCESS_TOKEN = 'xxxx'
ACCESS_TOKEN_SECRET = 'xxxx'