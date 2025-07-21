
# import external libraries
from flask import Flask

# create app function
# returns app
def create_app():
    app = Flask(__name__)

    # import views from views.py
    from .views import views
    # import auth from auth.py
    from .auth import auth

    # register blueprints
    app.register_blueprint(views, url_prefix="/")
    app.register_blueprint(auth, url_prefix="/")


    return app