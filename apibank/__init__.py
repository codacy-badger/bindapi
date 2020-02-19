from flask import Flask
from apibank.routes import configure_routes


def create_app():
    flask_app = Flask(__name__)
    # flask_app.config['SQLALCHEMY_DATABASE_URI'] = config.DATABASE_CONNECTION_URI
    flask_app.config['DEBUG'] = True
    # lask_app.app_context().push()
    # db.init_app(flask_app)
    # db.create_all()

    configure_routes(flask_app)
    return flask_app
