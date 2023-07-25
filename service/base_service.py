from dao.user import UserDAO
from dao.sqlite_base_dao import DAO
from marshmallow import Schema


class BaseService:
    dao_object_schema = Schema()
    dao_objects_schema = Schema(many=True)

    def __init__(self, dao: DAO | UserDAO):
        self.dao = dao

    def get_all(self, args: dict) -> list[dict] | None:
        """Возвращает список объектов."""

        status = args.pop("status", None)
        page = args.pop("page", None)

        if status == "new" and page is not None:
            # Все объекты в обратном порядке по странично
            dao_objects = self.dao.get_all_new_page(int(page))
        elif page is not None:
            # Все объекты по порядку по странично
            dao_objects = self.dao.get_all_page(int(page))
        elif status == "new":
            # Все объекты в обратном порядке
            dao_objects = self.dao.get_all_new()
        else:
            # Все объекты по порядку
            dao_objects = self.dao.get_all()

        return self.dao_objects_schema.dump(dao_objects)

    def create(self, data: dict) -> list[dict]:
        """Создает объект."""
        dao_object = self.dao.create(data)

        return self.dao_object_schema.dump(dao_object)

    def get_one(self, gid: int) -> dict | None:
        """Возвращает 1 объект по id"""
        dao_object = self.dao.get_one(gid)

        return self.dao_object_schema.dump(dao_object)

    def update(self, data: dict) -> dict | None:
        """Обновляет объект по id и всем полям таблицы"""
        oid = data.get('id')

        dao_object = self.dao.get_one(oid)

        if not dao_object:
            return None

        dao_object.name = data.get("name")

        dao_object = self.dao.update(dao_object)

        return self.dao_object_schema.dump(dao_object)

    def delete(self, oid: int) -> dict | None:
        """Удаляет объект по id."""
        dao_object = self.dao.get_one(oid)

        if not dao_object:
            return None

        self.dao.delete(dao_object)

        return self.dao_object_schema.dump(dao_object)
