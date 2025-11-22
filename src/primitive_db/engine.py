import shlex
import prompt
from .utils import load_metadata, save_metadata
from .core import (
    create_table,
    drop_table,
    list_tables,
    insert,
    select,
    update,
    delete,
    info,
    print_help,
)

METADATA_FILE = "db_meta.json"


def parse_where_clause(where_parts):
    """Парсит строку вида 'column = value' в словарь."""
    key, val = " ".join(where_parts).split("=")
    key = key.strip()
    val = val.strip().strip('"').strip("'")
    if val.lower() == "true":
        val = True
    elif val.lower() == "false":
        val = False
    elif val.isdigit():
        val = int(val)
    return {key: val}


def parse_set_clause(set_parts):
    """Парсит строку вида 'column = value' в словарь для update."""
    key, val = " ".join(set_parts).split("=")
    key = key.strip()
    val = val.strip().strip('"').strip("'")
    if val.lower() == "true":
        val = True
    elif val.lower() == "false":
        val = False
    elif val.isdigit():
        val = int(val)
    return {key: val}


def run():
    """Главный цикл программы."""
    print("*** Добро пожаловать в базу данных ***")
    metadata = load_metadata(METADATA_FILE)

    while True:
        user_input = prompt.string(">>> Введите команду: ")
        if not user_input:
            continue

        args = shlex.split(user_input)
        command = args[0].lower()

        if command == "exit":
            print("До свидания!")
            break

        elif command == "help":
            print_help()
            continue

        elif command == "create_table":
            table_name = args[1]
            columns = args[2:]
            metadata = create_table(metadata, table_name, columns)
            save_metadata(METADATA_FILE, metadata)

        elif command == "drop_table":
            table_name = args[1]
            metadata = drop_table(metadata, table_name)
            save_metadata(METADATA_FILE, metadata)

        elif command == "list_tables":
            list_tables(metadata)

        elif command == "insert":
            if args[1].lower() != "into" or "values" not in args:
                print("Некорректная команда insert.")
                continue
            table_name = args[2]
            values_str = user_input.split("values", 1)[1].strip()
            values_str = values_str.strip("()")
            values = [v.strip().strip('"').strip("'") for v in values_str.split(",")]
            insert(metadata, table_name, values)

        elif command == "select":
            if args[1].lower() != "from":
                print("Некорректная команда select.")
                continue
            table_name = args[2]
            if "where" in args:
                where_index = args.index("where") + 1
                where_clause = parse_where_clause(args[where_index:])
                select(metadata, table_name, where_clause)
            else:
                select(metadata, table_name)

        elif command == "update":
            table_name = args[1]
            set_index = args.index("set") + 1
            where_index = args.index("where")
            set_clause = parse_set_clause(args[set_index:where_index])
            where_clause = parse_where_clause(args[where_index + 1 :])
            update(metadata, table_name, set_clause, where_clause)

        elif command == "delete":
            if args[1].lower() != "from" or "where" not in args:
                print("Некорректная команда delete.")
                continue
            table_name = args[2]
            where_index = args.index("where") + 1
            where_clause = parse_where_clause(args[where_index:])
            delete(metadata, table_name, where_clause)

        elif command == "info":
            table_name = args[1]
            info(metadata, table_name)

        else:
            print(f"Функции {command} нет. Попробуйте снова.")
