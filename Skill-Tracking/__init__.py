from flask import Flask
from config import Config
from .database import db
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from dotenv import load_dotenv
import os

load_dotenv()

db = SQLAlchemy()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    login_manager.init_app(app)

    with app.app_context():
        from .routes import routes
        app.register_blueprint(routes, url_prefix='/')

    @login_manager.user_loader
    def load_user(user_id):
        from .models import User  # Importing inside the function to avoid circular imports
        return User.query.get(int(user_id))
        
    return app
