from flask import request, abort
from flask_restx import Resource, Namespace
from container import user_service, auth_service
from deccorators import auth_required

user_ns = Namespace("user")


@user_ns.route("/")
class PersonalCabinetView(Resource):
    @auth_required
    def get(self):
        """Получить информацию о пользователе (его профиль)."""

        header_data = request.headers['Authorization']
        token = header_data.split("Bearer ")[-1]

        try:
            email = auth_service.check_token(token)
        except Exception as e:
            print("JWT Decode Exception", e)
            abort(401)

        user = user_service.get_by_email(email)

        # Удалим хэш пароля из вывода
        del user["password"]

        return user, 200

    @auth_required
    def patch(self):
        """Изменить информацию пользователя (имя, фамилия, любимый жанр)."""

        header_data = request.headers['Authorization']
        token = header_data.split("Bearer ")[-1]

        try:
            email = auth_service.check_token(token)
        except Exception as e:
            print("JWT Decode Exception", e)
            abort(401)

        req_json = request.json
        req_json["email"] = email

        user = user_service.update_info(req_json)

        if not user:
            return "Не найдено", 404

        # Удалим хэш пароля из вывода
        del user["password"]

        return user, 200


@user_ns.route("/password")
class PersonalCabinetView(Resource):
    @auth_required
    def put(self):
        """Обновить пароль пользователя, для этого нужно отправить два пароля password_1 и password_2."""
        header_data = request.headers['Authorization']
        token = header_data.split("Bearer ")[-1]

        try:
            email = auth_service.check_token(token)
        except Exception as e:
            print("JWT Decode Exception", e)
            abort(401)

        req_json = request.json
        req_json["email"] = email

        try:
            user = user_service.update_password(req_json)
        except Exception:
            abort(401)

        if not user:
            return "Не найдено", 404

        # Удалим хэш пароля из вывода
        del user["password"]

        return user, 200
