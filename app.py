from flask import Flask, render_template
from flask_restx import Api

from config import Config
from setup_db import db

from views.director import directors_ns
from views.genre import genres_ns
from views.movie import movies_ns
from views.user import user_ns
from views.auth import auth_ns


def create_app(config_object):
    # функция создания основного объекта app
    application = Flask(__name__)
    application.config.from_object(config_object)
    register_extensions(application)
    return application


def register_extensions(application):
    # функция подключения расширений (Flask-SQLAlchemy, Flask-RESTx, ...)
    db.init_app(application)
    api = Api(application)

    api.add_namespace(movies_ns)
    api.add_namespace(genres_ns)
    api.add_namespace(directors_ns)
    api.add_namespace(user_ns)
    api.add_namespace(auth_ns)


app = create_app(Config())
app.debug = True


@app.errorhandler(404)
def not_found():
    return "Ничего не нашлось!"


if __name__ == '__main__':
    app.run(host="localhost", port=10001, debug=True)
