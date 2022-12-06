from dao.sqlite_dao import DAO
from dao.model.user import User


class UserDAO(DAO):
    def __init__(self, session):
        self.session = session
        self.model = User

    def get_by_email(self, email):
        return self.session.query(self.model).filter(self.model.email == email).first()
