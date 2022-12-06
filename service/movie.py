from dao.model.movie import MovieSchema


movie_schema = MovieSchema()
movies_schema = MovieSchema(many=True)


class MovieService:
    def __init__(self, movie_dao):
        self.movie_dao = movie_dao

    def get_all(self, args):
        """Возвращает все фильмы.
        Фильтрует результаты средствами sql, если были заданы фильтры.
        Для тех эндпоинтов, которые возвращают несколько записей, нужно организовать пагинацию через URL-параметр page,
        а на страницу будет возвращать по 12 записей.
        Параметр page - необязательный, а значит, если он не указан - нужно вернуть все записи.

        Так как мы хотим получать Новинки, для эндпонта GET /movies/ нужно еще добавить необязательный параметр status.
        Если он присутствует и имеет значение new — возвращаем записи в отсортированном виде (самые свежие),
        иначе возвращаем в том порядке, в котором они лежат в базе.
        """

        # Все фильмы без фильтрации по порядку
        if not args:
            movies = self.movie_dao.get_all()
            return movies_schema.dump(movies)


        status = args.pop("status", None)
        page = args.pop("page", None)

        if not args:

            if status == "new" and page is not None:
                # Все фильмы без фильтрации в обратном порядке по странично
                movies = self.movie_dao.get_all_new_page(int(page))
            elif page is not None:
                # Все фильмы без фильтрации по порядку по странично
                movies = self.movie_dao.get_all_page(int(page))
            elif status == "new":
                # Все фильмы без фильтрации в обратном порядке
                movies = self.movie_dao.get_all_new()
            else:
                # Все фильмы без фильтрации по порядку
                movies = self.movie_dao.get_all()

            return movies_schema.dump(movies)


        allowed_filter_list = ["director_id", "genre_id", "year"]

        filter_list = []

        for arg in args:
            if arg in allowed_filter_list:
                filter_list.append(f"{arg} = {args.get(arg)}")
            else:
                return None

        filter = ' AND '.join(filter_list)

        if status == "new" and page is not None:
            # Отфильтрованные фильмы в обратном порядке по странично
            movies = self.movie_dao.get_filtered_new_page(filter, int(page))
        elif page is not None:
            # Отфильтрованные фильмы по порядку по странично
            movies = self.movie_dao.get_filtered_page(filter, int(page))
        elif status == "new":
            # Отфильтрованные фильмы в обратном порядке
            movies = self.movie_dao.get_filtered_new(filter)
        else:
            # Отфильтрованные фильмы по порядку
            movies = self.movie_dao.get_filtered(filter)

        return movies_schema.dump(movies)

    def create(self, data):
        """Добавляет фильм"""
        movie = self.movie_dao.create(data)

        return movie_schema.dump(movie)

    def get_one(self, mid):
        """Возвращает 1 фильм по id"""
        movie = self.movie_dao.get_one(mid)

        return movie_schema.dump(movie)

    def update(self, data):
        """Обновляет фильм по id и всем полям таблицы"""
        mid = data.get('id')

        movie = self.movie_dao.get_one(mid)

        if not movie:
            return None

        movie.title = data.get("title")
        movie.description = data.get("description")
        movie.trailer = data.get("trailer")
        movie.year = data.get("year")
        movie.rating = data.get("rating")
        movie.genre_id = data.get("genre_id")
        movie.director_id = data.get("director_id")

        return movie_schema.dump(self.movie_dao.update_info(movie))

    def delete(self, mid):
        """Удаляет фильм по id"""
        movie = self.movie_dao.get_one(mid)

        if not movie:
            return None

        self.movie_dao.delete(movie)

        return movie_schema.dump(movie)
