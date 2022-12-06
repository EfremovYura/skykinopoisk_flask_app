from dao.model.director import DirectorSchema


director_schema = DirectorSchema()
directors_schema = DirectorSchema(many=True)


class DirectorService:
    def __init__(self, director_dao):
        self.director_dao = director_dao

    def get_all(self, args):
        """Возвращает список режиссеров"""

        status = args.pop("status", None)
        page = args.pop("page", None)

        if status == "new" and page is not None:
            # Все режиссеры в обратном порядке по странично
            directors = self.director_dao.get_all_new_page(int(page))
        elif page is not None:
            # Все режиссеры по порядку по странично
            directors = self.director_dao.get_all_page(int(page))
        elif status == "new":
            # Все режиссеры в обратном порядке
            directors = self.director_dao.get_all_new()
        else:
            # Все режиссеры по порядку
            directors = self.director_dao.get_all()

        return directors_schema.dump(directors)

    def create(self, data):
        """Создает режиссера"""
        director = self.director_dao.create(data)

        return director_schema.dump(director)

    def get_one(self, gid):
        """Возвращает 1 режиссера по id"""
        director = self.director_dao.get_one(gid)

        return director_schema.dump(director)

    def update(self, data):
        """Обновляет режиссера по id и всем полям таблицы"""
        gid = data.get('id')

        director = self.director_dao.get_one(gid)

        if not director:
            return None

        director.name = data.get("name")

        director = self.director_dao.update_info(director)

        return director_schema.dump(director)

    def delete(self, gid):
        """Удаляет режиссера по id"""
        director = self.director_dao.get_one(gid)

        if not director:
            return None

        self.director_dao.delete(director)

        return director_schema.dump(director)
