import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from dotenv import load_dotenv
from flask_jwt_extended import JWTManager

from config import config

load_dotenv()

db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager()

def create_app(config_name = os.getenv("FLASK_CONFIG")):

    # * Create flask app
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    #* initialise necessary extensions
    db.init_app(app)
    migrate.init_app(app,db)
    jwt.init_app(app)

    #* insert necessary blueprints
    from .api import api_blueprint
    app.register_blueprint(api_blueprint, url_prefix = '/api/v1')

    #* register models and schemas in app context
    from app import models
    from app import schema

    return app