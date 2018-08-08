import os.path
basedir = os.path.abspath(os.path.dirname(__file__))

DEBUG = True

SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://postgres:qwerty123@localhost/votation'

SQLALCHEMY_TRACK_MODIFICATIONS = True

SECRET_KEY = 'votation'