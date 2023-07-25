import calendar
import datetime
import jwt

from constants import JWT_ALGO, JWT_SECRET
from service.user import UserService


class AuthService:

    def __init__(self, user_service: UserService):
        self.user_service = user_service

    def check_user_password(self, email: str, password: str) -> None:
        user = self.user_service.get_by_email(email)

        if not user:
            raise Exception()

        if not self.user_service.compare_passwords(user.get("password"), password):
            raise Exception()

    @staticmethod
    def generate_tokens(email: str) -> dict:

        data = {
            "email": email
        }

        days130 = datetime.datetime.utcnow() + datetime.timedelta(days=130)
        data["exp"] = calendar.timegm(days130.timetuple())
        refresh_token = jwt.encode(data, JWT_SECRET, algorithm=JWT_ALGO)

        minutes60 = datetime.datetime.utcnow() + datetime.timedelta(minutes=60)
        data["exp"] = calendar.timegm(minutes60.timetuple())
        access_token = jwt.encode(data, JWT_SECRET, algorithm=JWT_ALGO)

        return {"access_token": access_token, "refresh_token": refresh_token}

    def check_token(self, token: str) -> str:
        data = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGO])
        email = data.get("email")
        exp = data.get("exp")

        user = self.user_service.get_by_email(email)

        if not user:
            raise Exception()

        now = calendar.timegm(datetime.datetime.utcnow().timetuple())
        if exp <= now:
            raise Exception()

        return email

    def check_tokens(self, access_token: str, refresh_token: str) -> str:

        email_a_token = self.check_token(access_token)
        email_r_token = self.check_token(refresh_token)

        if email_a_token == email_r_token:
            return email_a_token
        else:
            raise Exception()
