from dao.sqlite_dao import DAO
from dao.model.movie import Movie

from sqlalchemy import text
from constants import ITEMS_PER_PAGE

class MovieDAO(DAO):
    def __init__(self, session):
        self.session = session
        self.model = Movie
