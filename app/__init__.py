from flask import Flask
from config import config
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os
from dotenv import load_dotenv

load_dotenv()

db = SQLAlchemy()
migrate = Migrate()

def create_app(config_name = os.getenv("FLASK_CONFIG")):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    db.init_app(app)
    migrate.init_app(app,db)

    from .api import api_blueprint
    app.register_blueprint(api_blueprint, url_prefix = '/api/v1')

    from app import models
    from app import schema

    return app