with open('passwd') as f:
    password = f.read().strip()

class Config(object):
    SECRET_KEY = password
    SQLALCHEMY_DATABASE_URI = 'sqlite:///database.db'