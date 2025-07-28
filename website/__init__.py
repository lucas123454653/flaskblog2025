"""This module initializes the Flask app, database, and login manager.

It registers blueprints, sets configuration values, and sets up the user loader
function for Flask-Login. It also creates the database if it doesn't exist.
"""

# import external libraries
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

db = SQLAlchemy()
DB_NAME = "database.db"


def create_app():
    """
    Create and configure the Flask application instance.

    This function sets up the app config, initializes extensions like
    SQLAlchemy and Flask-Login, registers the auth and views blueprints,
    and creates the database if it doesn't already exist.

    Returns:
        Flask: Configured Flask application instance.
    """
    app = Flask(__name__)
    app.config['SECRET_KEY'] = "YjoZHYUzTS"

    database_uri = f"sqlite:///{DB_NAME}"
    app.config['SQLALCHEMY_DATABASE_URI'] = database_uri

    db.init_app(app)

    # import blueprints
    from .views import views
    from .auth import auth

    # register blueprints
    app.register_blueprint(views, url_prefix="/")
    app.register_blueprint(auth, url_prefix="/")

    from .models import User

    with app.app_context():
        db.create_all()
        print("Created Database!")

    login_manager = LoginManager()
    login_manager.login_view = "auth.login"
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app
