import os

base_dir      = os.path.abspath(os.path.dirname(__file__))
project_dir   = os.path.dirname(os.path.abspath(__file__))
database_path = os.path.join(project_dir,"db", "dblibrary.db")
print('database_path =',database_path)
class Config(object):
    DEBUG=True
    SECRET_KEY='My Secret Key'
    SQLALCHEMY_DATABASE_URI = database_path

