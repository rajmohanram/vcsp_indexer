import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY')
    DB_FILE = os.path.join(basedir, 'data/app.db')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URI')\
        or 'sqlite:///' + DB_FILE
    SQLALCHEMY_TRACK_MODIFICATIONS = False
