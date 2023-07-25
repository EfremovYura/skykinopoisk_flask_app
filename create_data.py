# Модуль, чтобы создать БД с данными

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from dao.model.movie import Movie
from dao.model.genre import Genre
from dao.model.user import User
from dao.model.director import Director

from data import data

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

db.drop_all()
db.create_all()


with app.app_context():
    for movie in data["movies"]:
        movie_obj = Movie(
            id=movie["pk"],
            title=movie["title"],
            description=movie["description"],
            trailer=movie["trailer"],
            year=movie["year"],
            rating=movie["rating"],
            genre_id=movie["genre_id"],
            director_id=movie["director_id"],
        )
        with db.session.begin():
            db.session.add(movie_obj)

    for director in data["directors"]:
        director_obj = Director(
            id=director["pk"],
            name=director["name"],
        )
        with db.session.begin():
            db.session.add(director_obj)

    for genre in data["genres"]:
        genre_obj = Genre(
            id=genre["pk"],
            name=genre["name"],
        )
        with db.session.begin():
            db.session.add(genre_obj)

    for user in data["users"]:
        user_obj = User(
            id=user["id"],
            email=user["email"],
            password=user["password"],
            name=user["name"],
            surname=user["surname"],
            favorite_genre=user["favorite_genre"],
        )
        with db.session.begin():
            db.session.add(user_obj)
