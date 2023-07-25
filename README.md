# Проект "Кинопоиск" 

## Технологии:
- python 3.11
- Flask==2.0
- SQLAlchemy==1.4
- marshmallow==3.13
- PyJWT==2.6
- flask-restx==1.0
- pytest==7.1

## Эндпоинты для фильмов, жанров и режиссеров:
- GET /movies/
- GET /movies/{id}
- GET /genres/
- GET /genres/{id}
- GET /directors/
- GET /directors/{id}
    
Дополнительно реализована пагинация, сортировка и фильтрация.

## Эндпоинты авторизации:

- POST /auth/register — передавая  email и пароль, создаем пользователя в системе.
- POST /auth/login — передаем email и пароль и, если пользователь прошел аутентификацию, 
возвращаем пользователю ответ в виде:

  ```json
  {
     "access_token": "qwesfsdfa",
     "refresh_token": "kjhgfgjakda",
  }
  ```

- PUT /auth/login — принимаем пару токенов и, если они валидны, создаем пару новых.

## Эндпоинты работы с пользователями:

- GET /user/ — получить информацию о пользователе (его профиль).
- PATCH /user/ — изменить информацию пользователя (имя, фамилия, любимый жанр).
- PUT /user/password — обновить пароль пользователя, для этого нужно отправить два пароля *password_1* и *password_2.*


## Структура проекта
- Основной файл запуска программы в [app.py](app.py)
- Бизнес логика находится в [service](service)
- Описание моделей находится в [dao](dao)
- Class based view реализация представлений в [views](views)
- Документация для swager в [swagger.json](swagger.json)
- База данных SQlite в [test.db](test.db)
- Создание объекта SQLAlchemy в [setup_db.py](setup_db.py)
- Декоратор для проверки авторизации в [deccorators.py](deccorators.py)
- Первоначальные данные и скрипт для загрузки в БД в [create_data.py](create_data.py)
- Контейнер для связи сервисов и моделей в [container.py](container.py)
- Константы в [constants.py](constants.py)
- Настройки приложения в [config.py](config.py)

## Запуск приложения:
    python app.py
