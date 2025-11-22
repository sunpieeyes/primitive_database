import time
from prompt import string

# -------------------
# Обработка ошибок
# -------------------
def handle_db_errors(func):
    """Декоратор для централизованной обработки ошибок."""
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except FileNotFoundError:
            print("Ошибка: Файл данных не найден. Возможно, база данных не инициализирована.")
        except KeyError as e:
            print(f"Ошибка: Таблица или столбец {e} не найден.")
        except ValueError as e:
            print(f"Ошибка валидации: {e}")
        except Exception as e:
            print(f"Произошла непредвиденная ошибка: {e}")

        # Если функция упала — возвращаем первый аргумент, если есть
        if args:
            return args[0]
        return None
    return wrapper

# -------------------
# Подтверждение действия
# -------------------
def confirm_action(action_name):
    """Фабрика декоратора, запрашивает подтверждение для опасных операций."""
    def decorator(func):
        def wrapper(*args, **kwargs):
            answer = string(f'Вы уверены, что хотите выполнить "{action_name}"? [y/n]: ').strip().lower()
            if answer != "y":
                print("Операция отменена.")
                if args:
                    return args[0]
                return None
            return func(*args, **kwargs)
        return wrapper
    return decorator

# -------------------
# Логирование времени выполнения
# -------------------
def log_time(func):
    """Декоратор для замера времени выполнения функции."""
    def wrapper(*args, **kwargs):
        start = time.monotonic()
        result = func(*args, **kwargs)
        end = time.monotonic()
        print(f"Функция {func.__name__} выполнилась за {end - start:.3f} секунд.")
        return result
    return wrapper

# -------------------
# Кэширование
# -------------------
def create_cacher():
    """Создает замыкание для кэширования результатов."""
    cache = {}
    def cache_result(key, value_func):
        if key in cache:
            return cache[key]
        result = value_func()
        cache[key] = result
        return result
    return cache_result
