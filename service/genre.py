from dao.model.genre import GenreSchema
from service.base_service import BaseService


class GenreService(BaseService):
    dao_object_schema = GenreSchema()
    dao_objects_schema = GenreSchema(many=True)
