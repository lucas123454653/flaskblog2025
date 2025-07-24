
# import external libraries
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

db = SQLAlchemy()
DB_NAME = "database.db"


# create app function
# returns app
def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = "YjoZHYUzTS"
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    db.init_app(app)

    # import views from views.py
    from .views import views
    # import auth from auth.py
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