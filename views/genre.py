from flask import request
from flask_restx import Resource, Namespace
from container import genre_service
from deccorators import auth_required

genres_ns = Namespace("genres")


@genres_ns.route("/")
class GenresView(Resource):
    @auth_required
    def get(self):
        """
        Возвращает список всех жанров
        """
        args = request.args.to_dict()

        genres = genre_service.get_all(args)

        if not genres:
            return "Не найдено", 404

        return genres, 200


@genres_ns.route("/<int:gid>")
class GenreView(Resource):
    @auth_required
    def get(self, gid):
        """Возвращает подробную информацию о жанре"""
        genre = genre_service.get_one(gid)

        if not genre:
            return "Не найдено", 404

        return genre, 200
