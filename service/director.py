from dao.model.director import DirectorSchema
from service.base_service import BaseService


class DirectorService(BaseService):
    dao_object_schema = DirectorSchema()
    dao_objects_schema = DirectorSchema(many=True)
