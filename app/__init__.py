from flask import Flask
from .config import Config
from .extensions import db
import os

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Init extensions
    db.init_app(app)

    # Register blueprints
    from .main.routes import main
    app.register_blueprint(main)

    return app

