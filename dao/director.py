from dao.sqlite_base_dao import DAO
from dao.model.director import Director


class DirectorDAO(DAO):
    def __init__(self, session):
        super().__init__(session, Director)
