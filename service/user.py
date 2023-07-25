import base64
import hashlib
import hmac

from dao.model.user import UserSchema
from constants import PWD_HASH_SALT, PWD_HASH_ITERATIONS
from service.base_service import BaseService


class UserService(BaseService):
    dao_object_schema = UserSchema()
    dao_objects_schema = UserSchema(many=True)

    def get_all(self, args: dict) -> list[dict] | None:
        """Возвращает всех пользователей.
        Фильтрует результаты средствами sql, если были заданы фильтры.
        """
        if not args:
            users = self.dao.get_all()
            return self.dao_objects_schema.dump(users)

        allowed_filter_list = ["role"]

        filter_list = []

        for arg in args:
            if arg in allowed_filter_list:
                filter_list.append(f"{arg} = {args.get(arg)}")
            else:
                return None

        text_filter = ' AND '.join(filter_list)

        return self.dao_objects_schema.dump(self.dao.get_filtered(text_filter))

    def create(self, data: dict) -> dict:
        """Добавляет пользователя"""
        user = self.dao.create(data)

        return self.dao_object_schema.dump(user)

    def get_one(self, uid: int) -> dict:
        """Возвращает 1 пользователя по id"""
        user = self.dao.get_one(uid)

        return self.dao_object_schema.dump(user)

    def get_by_email(self, email: str) -> dict:
        user = self.dao.get_by_email(email)

        return self.dao_object_schema.dump(user)

    def update_info(self, data: dict) -> dict | None:
        """Обновляет информацию пользователя """

        user = self.dao.get_by_email(data.get("email"))

        user.name = data.get("name") or user.name
        user.surname = data.get("surname") or user.surname
        user.favorite_genre = data.get("favorite_genre") or user.favorite_genre

        user = self.dao.update(user)

        if not user:
            return None

        return self.dao_object_schema.dump(user)

    def update_password(self, data: dict) -> dict | None:
        """Обновляет пароль пользователя """

        email = data.get("email")
        old_password = data.get("password_1")
        new_password = data.get("password_2")

        user = self.dao.get_by_email(email)

        if self.compare_passwords(user.password, old_password):
            new_password_hash = self.get_hash(new_password)
            user.password = new_password_hash
        else:
            raise Exception()

        user = self.dao.update(user)

        if not user:
            return None

        return self.dao_object_schema.dump(user)

    def delete(self, uid: int) -> dict | None:
        """Удаляет пользователя по id"""
        user = self.dao.get_one(uid)

        if not user:
            return None

        self.dao.delete(user)

        return self.dao_object_schema.dump(user)

    @staticmethod
    def get_hash(password: str):
        return base64.b64encode(hashlib.pbkdf2_hmac(
            'sha256',
            password.encode('utf-8'),
            PWD_HASH_SALT,
            PWD_HASH_ITERATIONS
        ))

    @staticmethod
    def compare_passwords(password_hash, request_password):
        return hmac.compare_digest(
            base64.b64decode(password_hash),
            hashlib.pbkdf2_hmac('sha256',
                                request_password.encode('utf-8'),
                                PWD_HASH_SALT,
                                PWD_HASH_ITERATIONS
                                )
        )
