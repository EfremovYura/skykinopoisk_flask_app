from dao.sqlite_dao import DAO
from dao.model.director import Director


class DirectorDAO(DAO):
    def __init__(self, session):
        self.session = session
        self.model = Director
