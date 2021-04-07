import os

basedir = os.path.abspath(  os.path.join(os.path.dirname(__file__),'..'))
database_path = "sqlite:///{}".format(os.path.join(basedir,"db", "dblibrary.db"))

class BaseConfig():
   DEBUG = False

class DevConfig(BaseConfig):
    FLASK_ENV = 'Development'
    SQLALCHEMY_DATABASE_URI = database_path
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SECRET_KEY = 'My Secret Key'
