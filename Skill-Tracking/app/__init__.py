from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

# Initialize extensions
db = SQLAlchemy()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize extensions within the app context
    with app.app_context():
        # Initialize SQLAlchemy
        db.init_app(app)

        # Initialize login manager
        login_manager.init_app(app)

        # Import models here to avoid circular imports
        from .models import User  # Replace with your actual User model
        
        # Create database tables (if they don't exist)
        with app.app_context():
            db.create_all()

        # Register blueprints
        from .routes import routes
        app.register_blueprint(routes, url_prefix='/')

    # Define the user_loader callback for Flask-Login
    @login_manager.user_loader
    def load_user(user_id):
        from .models import User  # Import inside the function to avoid circular import
        return User.query.get(int(user_id))

    return app
