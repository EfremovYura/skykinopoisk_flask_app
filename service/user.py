import base64
import hashlib
import hmac

from dao.model.user import UserSchema
from constants import PWD_HASH_SALT, PWD_HASH_ITERATIONS

user_schema = UserSchema()
users_schema = UserSchema(many=True)


class UserService:
    def __init__(self, user_dao):
        self.user_dao = user_dao

    def get_all(self, args):
        """Возвращает всех пользователей.
        Фильтрует результаты средствами sql, если были заданы фильтры.
        """
        if not args:
            users = self.user_dao.get_all()
            return users_schema.dump(users)

        allowed_filter_list = ["role"]

        filter_list = []

        for arg in args:
            if arg in allowed_filter_list:
                filter_list.append(f"{arg} = {args.get(arg)}")
            else:
                return None

        text_filter = ' AND '.join(filter_list)

        users = users_schema.dump(self.user_dao.get_filtered(text_filter))

        return users

    def create(self, data):
        """Добавляет пользователя"""
        user = self.user_dao.create(data)

        return user_schema.dump(user)

    def get_one(self, uid):
        """Возвращает 1 пользователя по id"""
        user = self.user_dao.get_one(uid)

        return user_schema.dump(user)

    def get_by_email(self, email):
        user = self.user_dao.get_by_email(email)

        return user_schema.dump(user)

    def update_info(self, data):
        """Обновляет информацию пользователя """

        user = self.user_dao.get_by_email(data.get("email"))

        user.name = data.get("name") or user.name
        user.surname = data.get("surname") or user.surname
        user.favorite_genre = data.get("favorite_genre") or user.favorite_genre

        user = self.user_dao.update(user)

        if not user:
            return None

        return user_schema.dump(user)

    def update_password(self, data):
        """Обновляет пароль пользователя """

        email = data.get("email")
        old_password = data.get("password_1")
        new_password = data.get("password_2")

        user = self.user_dao.get_by_email(email)

        if self.compare_passwords(user.password, old_password):
            new_password_hash = self.get_hash(new_password)
            user.password = new_password_hash
        else:
            raise Exception()

        user = self.user_dao.update(user)

        if not user:
            return None

        return user_schema.dump(user)

    def delete(self, uid):
        """Удаляет пользователя по id"""
        user = self.user_dao.get_one(uid)

        if not user:
            return None

        self.user_dao.delete(user)

        return user_schema.dump(user)

    def get_hash(self, password):
        return base64.b64encode(hashlib.pbkdf2_hmac(
            'sha256',
            password.encode('utf-8'),  # Convert the password to bytes
            PWD_HASH_SALT,
            PWD_HASH_ITERATIONS
        ))

    def compare_passwords(self, password_hash, request_password):
        return hmac.compare_digest(
            base64.b64decode(password_hash),
            hashlib.pbkdf2_hmac('sha256',
                                request_password.encode('utf-8'),  # Convert the password to bytes
                                PWD_HASH_SALT,
                                PWD_HASH_ITERATIONS
                                )
        )
