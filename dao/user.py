from dao.sqlite_base_dao import DAO
from dao.model.user import User
from setup_db import db


class UserDAO(DAO):
    def __init__(self, session):
        super().__init__(session, User)

    def get_by_email(self, email: str) -> db.Model:
        return self.session.query(self.model).filter(self.model.email == email).first()
