from flask import Flask
from .config import Config
from .extensions import db, login_manager, bcrypt, mail, oauth

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Init extensions
    db.init_app(app)
    login_manager.init_app(app)
    bcrypt.init_app(app)
    mail.init_app(app)
    oauth.init_app(app)

    # Google OAuth setup
    oauth.register(
        name='google',
        client_id=app.config['GOOGLE_CLIENT_ID'],
        client_secret=app.config['GOOGLE_CLIENT_SECRET'],
        access_token_url='https://accounts.google.com/o/oauth2/token',
        access_token_params=None,
        authorize_url='https://accounts.google.com/o/oauth2/auth',
        authorize_params={
            'scope': 'openid email profile',
            'prompt': 'consent'
        },
        api_base_url='https://www.googleapis.com/oauth2/v1/',
        userinfo_endpoint='https://openidconnect.googleapis.com/v1/userinfo'
    )

    from .main.routes import main
    from .auth.routes import auth
    app.register_blueprint(main)
    app.register_blueprint(auth)

    return app


