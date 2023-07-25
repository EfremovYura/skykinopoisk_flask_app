from dao.model.movie import MovieSchema
from service.base_service import BaseService


class MovieService(BaseService):
    dao_object_schema = MovieSchema()
    dao_objects_schema = MovieSchema(many=True)

    def get_all(self, args: dict) -> list[dict] | None:
        """Возвращает все фильмы. Выполняет фильтрацию, пагинацию, сортировку.
        """

        # Все фильмы без фильтрации по порядку
        if not args:
            movies = self.dao.get_all()
            return self.dao_objects_schema.dump(movies)

        status = args.pop("status", None)
        page = args.pop("page", None)

        arg_data = {
            "status": status,
            "page": page,
        }

        if not args:
            return super().get_all(arg_data)

        # Фильтрация
        allowed_filter_list = ["director_id", "genre_id", "year"]
        filter_list = []

        for arg in args:
            if arg in allowed_filter_list:
                filter_list.append(f"{arg} = {args.get(arg)}")
            else:
                return None

        user_filter = ' AND '.join(filter_list)

        if status == "new" and page is not None:
            # Отфильтрованные фильмы в обратном порядке по странично
            movies = self.dao.get_filtered_new_page(user_filter, int(page))
        elif page is not None:
            # Отфильтрованные фильмы по порядку по странично
            movies = self.dao.get_filtered_page(user_filter, int(page))
        elif status == "new":
            # Отфильтрованные фильмы в обратном порядке
            movies = self.dao.get_filtered_new(user_filter)
        else:
            # Отфильтрованные фильмы по порядку
            movies = self.dao.get_filtered(user_filter)

        return self.dao_objects_schema.dump(movies)

    def update(self, data: dict) -> dict | None:
        """Обновляет фильм по id и всем полям таблицы."""
        mid = data.get('id')

        movie = self.dao.get_one(mid)

        if not movie:
            return None

        movie.title = data.get("title")
        movie.description = data.get("description")
        movie.trailer = data.get("trailer")
        movie.year = data.get("year")
        movie.rating = data.get("rating")
        movie.genre_id = data.get("genre_id")
        movie.director_id = data.get("director_id")

        return self.dao_object_schema.dump(self.dao.update(movie))
