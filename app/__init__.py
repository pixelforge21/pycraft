import os
from flask import Flask
from .config import Config
from .extensions import db, migrate, login_manager, bcrypt, mail, oauth
from .models import User  # ensure models import after db

def create_app():
    app = Flask(__name__, static_folder="static", template_folder="templates")
    app.config.from_object(Config)

    # initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    bcrypt.init_app(app)
    mail.init_app(app)
    oauth.init_app(app)

    # Register google oauth client
    if app.config.get("GOOGLE_CLIENT_ID") and app.config.get("GOOGLE_CLIENT_SECRET"):
        oauth.register(
            name='google',
            client_id=app.config['GOOGLE_CLIENT_ID'],
            client_secret=app.config['GOOGLE_CLIENT_SECRET'],
            access_token_url='https://oauth2.googleapis.com/token',
            authorize_url='https://accounts.google.com/o/oauth2/v2/auth',
            api_base_url='https://www.googleapis.com/oauth2/v2/',
            client_kwargs={'scope': 'openid email profile'}
        )

    # Blueprints
    from .auth.routes import auth_bp
    from .main.routes import main_bp
    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp, url_prefix='/auth')

    # create DB tables if not exist (safe for dev)
    with app.app_context():
        db.create_all()

    return app


