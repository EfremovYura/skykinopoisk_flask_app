from dao.sqlite_base_dao import DAO
from dao.model.movie import Movie


class MovieDAO(DAO):
    def __init__(self, session):
        super().__init__(session, Movie)
