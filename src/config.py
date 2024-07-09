from dotenv import load_dotenv
import os

path = os.path.join(os.path.dirname(__file__), "../.env")

if os.path.exists(path):
    load_dotenv(path)


class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv("SQLALCHEMY_DATABASE_URI", "sqlite:///:memory")
    SQLALCHEMY_TRACK_MODIFICATIONS = os.getenv("SQLALCHEMY_TRACK_MODIFICATIONS", True)
    SECRET_KEY = os.getenv('SECRET_KEY', 'LlqFlLo6fGAYfn9')

class Development(Config):
    DEBUG = True


class Production(Config):
    DEBUG = False


config = {
    'production' : Production,
    'development' : Development
}