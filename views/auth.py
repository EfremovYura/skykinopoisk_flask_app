from flask import request, abort
from flask_restx import Resource, Namespace
from container import user_service, auth_service


auth_ns = Namespace("auth")


@auth_ns.route("/register")
class RegisterView(Resource):
    """Передавая email и пароль, создаем пользователя в системе."""
    def post(self):
        req_json = request.json

        email = req_json.get("email")
        password = req_json.get("password")
        name = req_json.get("name")
        surname = req_json.get("surname")
        favorite_genre = req_json.get("favorite_genre", 1)

        if None in [email, password]:
            abort(400)

        user_in_db = user_service.get_by_email(email)

        if user_in_db:
            return "Пользователь с таким именем уже существует, для обновления используйте метод put", 404

        password_hash = user_service.get_hash(password)

        data = {
            "email": email,
            "password": password_hash,
            "name": name,
            "surname": surname,
            "favorite_genre": favorite_genre
        }

        user = user_service.create(data)

        return user, 201


@auth_ns.route("/login")
class AuthView(Resource):
    def post(self):
        """
        Передаем email и пароль и, если пользователь прошел аутентификацию,
        возвращаем пользователю ответ в виде json.
        """

        req_json = request.json

        email = req_json.get("email")
        password = req_json.get("password")

        if None in [email, password]:
            return "not correct credentials", 400

        try:
            auth_service.check_user_password(email, password)
            tokens = auth_service.generate_tokens(email)
        except Exception:
            return "not correct credentials", 400

        return tokens, 201

    def put(self):
        """Принимаем пару токенов и, если они валидны, создаем пару новых."""

        req_json = request.json

        refresh_token = req_json.get("refresh_token")
        access_token = req_json.get("access_token")

        try:
            email = auth_service.check_tokens(access_token, refresh_token)
        except Exception:
            return "not correct credentials", 400

        if email:
            try:
                tokens = auth_service.generate_tokens(email)
            except Exception:
                return "not correct credentials", 400

        return tokens, 201
