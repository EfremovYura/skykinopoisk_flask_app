from dao.sqlite_dao import DAO
from dao.model.genre import Genre


class GenreDAO(DAO):
    def __init__(self, session):
        self.session = session
        self.model = Genre
