import os
from datetime import timedelta

from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY")
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes = int(os.getenv("JWT_ACCESS_TOKEN_EXPIRES")))
    
    @staticmethod
    def init_app(app):
        pass

class DevelopmentConfig(Config):
    # * Configuration used in development environments only
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.getenv("DEV_DATABASE_URL")

class TestingConfig(Config):
    # * Configuration used in unit and integration testing
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.getenv("TEST_DATABASE_URL")

config = {
    "development" : DevelopmentConfig,
    "testing" : TestingConfig,
    "default" : DevelopmentConfig
}

