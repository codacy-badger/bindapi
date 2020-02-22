from flask import Flask
from apibank.routes import configure_routes
from redis import StrictRedis

redisClient = StrictRedis(host='redis', port=6379,  encoding="utf-8", decode_responses=True)


def create_app():
    flask_app = Flask(__name__)
    flask_app.config['DEBUG'] = True
    configure_routes(flask_app)
    return flask_app
