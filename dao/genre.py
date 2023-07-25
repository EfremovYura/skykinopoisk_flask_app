from dao.sqlite_base_dao import DAO
from dao.model.genre import Genre


class GenreDAO(DAO):
    def __init__(self, session):
        super().__init__(session, Genre)
