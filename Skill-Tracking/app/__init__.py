from flask import Flask
from config import Config

from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)


    login_manager.init_app(app)

    with app.app_context():
        from .routes import routes
        app.register_blueprint(routes, url_prefix='/')
        db.app = app
        db.init_app(app)
        db.create_all()

    @login_manager.user_loader
    def load_user(user_id):
        from .models import User  # Importing inside the function to avoid circular imports
        return User.query.get(int(user_id))
        
    return app
