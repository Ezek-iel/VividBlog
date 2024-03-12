import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY")
    
    @staticmethod
    def init_app(app):
        pass

class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.getenv("DEV_DATABASE_URL")

class TestingConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.getenv("TESTING_DATABASE_URL")

config = {
    "development" : DevelopmentConfig,
    "testing" : TestingConfig,
    "default" : DevelopmentConfig
}
