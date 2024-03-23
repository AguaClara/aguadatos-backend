"""Flask configuration variables."""
import os  
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))

#create 'instance' folder in the root directory if not existent
if not os.path.exists(os.path.join(basedir, 'instance')):
    os.makedirs(os.path.join(basedir, 'instance'))

class Config:
    """Set Flask configuration from .env file."""
    DEBUG = False
    TESTING = False

    # General Config
    SECRET_KEY = os.environ.get('SECRET_KEY')
    FLASK_APP = os.environ.get('FLASK_APP')
    FLASK_ENV = os.environ.get('FLASK_ENV')

    # Flask-SQLAlchemy
    SQLALCHEMY_DATABASE_URI = os.environ.get("SQLALCHEMY_DATABASE_URI", default=f"sqlite:///{os.path.join(basedir, 'instance', "aguadatos.db")}")
    SQLALCHEMY_ECHO = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class ProductionConfig(Config):
    SQLALCHEMY_ECHO = False

class DevelopmentConfig(Config):
    DEBUG = True

class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URI',
                                             default=f"sqlite:///{os.path.join(basedir, 'instance', 'test_aguadatos.db')}")