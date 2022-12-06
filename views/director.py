from flask import request
from flask_restx import Resource, Namespace
from container import director_service
from deccorators import auth_required


directors_ns = Namespace("directors")


@directors_ns.route("/")
class DirectorsView(Resource):
    @auth_required
    def get(self):
        """Возвращает список всех режиссеров"""

        args = request.args.to_dict()

        directors = director_service.get_all(args)

        if not directors:
            return "Не найдено", 404

        return directors, 200


@directors_ns.route("/<int:did>")
class DirectorView(Resource):
    @auth_required
    def get(self, did):
        """Возвращает подробную информацию о режиссере"""
        director = director_service.get_one(did)

        if not director:
            return "Не найдено", 404

        return director, 200
