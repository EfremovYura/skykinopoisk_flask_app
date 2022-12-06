from dao.model.genre import GenreSchema


genre_schema = GenreSchema()
genres_schema = GenreSchema(many=True)


class GenreService:
    def __init__(self, genre_dao):
        self.genre_dao = genre_dao

    def get_all(self, args):
        """Возвращает список жанров"""

        status = args.pop("status", None)
        page = args.pop("page", None)

        if status == "new" and page is not None:
            # Все жанры в обратном порядке по странично
            genres = self.genre_dao.get_all_new_page(int(page))
        elif page is not None:
            # Все жанры по порядку по странично
            genres = self.genre_dao.get_all_page(int(page))
        elif status == "new":
            # Все жанры в обратном порядке
            genres = self.genre_dao.get_all_new()
        else:
            # Все жанры по порядку
            genres = self.genre_dao.get_all()

        return genres_schema.dump(genres)

    def create(self, data):
        """Создает жанр"""
        genre = self.genre_dao.create(data)

        return genre_schema.dump(genre)

    def get_one(self, gid):
        """Возвращает 1 жанр по id"""
        genre = self.genre_dao.get_one(gid)

        return genre_schema.dump(genre)

    def update(self, data):
        """Обновляет жанр по id и всем полям таблицы"""
        gid = data.get('id')

        genre = self.genre_dao.get_one(gid)

        if not genre:
            return None

        genre.name = data.get("name")

        genre = self.genre_dao.update_info(genre)

        return genre_schema.dump(genre)

    def delete(self, gid):
        """Удаляет жанр по id"""
        genre = self.genre_dao.get_one(gid)

        if not genre:
            return None

        self.genre_dao.delete(genre)

        return genre_schema.dump(genre)
