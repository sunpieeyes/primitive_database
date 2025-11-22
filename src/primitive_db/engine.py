import shlex
from .utils import load_metadata, save_metadata
from .core import create_table, drop_table, list_tables

METADATA_FILE = "db_meta.json"

def print_help():
    """Выводит справку по доступным командам."""
    print("\n***Процесс работы с таблицей***")
    print("Функции:")
    print("<command> create_table <имя_таблицы> <столбец1:тип> .. - создать таблицу")
    print("<command> list_tables - показать список всех таблиц")
    print("<command> drop_table <имя_таблицы> - удалить таблицу")
    print("\nОбщие команды:")
    print("<command> exit - выход из программы")
    print("<command> help - справочная информация\n")

def run():
    """Основной цикл программы."""
    while True:
        metadata = load_metadata(METADATA_FILE)
        try:
            user_input = input(">>>Введите команду: ")
        except (EOFError, KeyboardInterrupt):
            print("\nДо свидания!")
            break

        if not user_input.strip():
            continue

        try:
            args = shlex.split(user_input)
        except ValueError as e:
            print(f"Ошибка разбора команды: {e}")
            continue

        command = args[0]
        if command == "create_table":
            if len(args) < 2:
                print("Некорректная команда. Нужно указать имя таблицы и хотя бы один столбец.")
                continue
            table_name = args[1]
            columns = args[2:]
            metadata = create_table(metadata, table_name, columns)
            save_metadata(METADATA_FILE, metadata)

        elif command == "drop_table":
            if len(args) != 2:
                print("Некорректная команда. Нужно указать имя таблицы.")
                continue
            table_name = args[1]
            metadata = drop_table(metadata, table_name)
            save_metadata(METADATA_FILE, metadata)

        elif command == "list_tables":
            list_tables(metadata)

        elif command == "help":
            print_help()

        elif command == "exit":
            print("До свидания!")
            break

        else:
            print(f"Функции {command} нет. Попробуйте снова.")
