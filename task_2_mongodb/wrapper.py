from pymongo.errors import PyMongoError


def mongo_wrapper(func):
    """
    Декоратор для обгортки функцій MongoDB і автоматизованої обробки помилок.
    """
    def wrapper(db, *args, **kwargs):
        try:
            return func(db, *args, **kwargs)
        except PyMongoError as e:
            print(f"Помилка при роботі з базою даних: {e}")
    return wrapper