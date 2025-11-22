import shlex
import prompt
from .utils import load_metadata, save_metadata, load_table_data, save_table_data
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
from .decorators import handle_db_errors, create_cacher

METADATA_FILE = "db_meta.json"
DATA_DIR = "data/"

cache = create_cacher()

def parse_where_clause(where_parts):
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

@handle_db_errors
def run():
    print("*** Добро пожаловать в базу данных ***")
    metadata = load_metadata(METADATA_FILE) or {}


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
        elif command == "create_table":
            table_name = args[1]
            columns = args[2:]
            metadata = create_table(metadata, table_name, columns) or metadata
            save_metadata(METADATA_FILE, metadata)
        elif command == "drop_table":
            table_name = args[1]
            metadata = drop_table(metadata, table_name) or metadata
            save_metadata(METADATA_FILE, metadata)
        elif command == "list_tables":
            list_tables(metadata)
        elif command == "insert":
            if args[1].lower() != "into" or "values" not in args:
                print("Некорректная команда insert.")
                continue
            table_name = args[2]
            values_str = user_input.split("values", 1)[1].strip().strip("()")
            values = [v.strip().strip('"').strip("'") for v in values_str.split(",")]
            table_data = load_table_data(table_name)
            table_data = insert(metadata, table_name, values, table_data) or table_data
            save_table_data(table_name, table_data)
        elif command == "select":
            if args[1].lower() != "from":
                print("Некорректная команда select.")
                continue
            table_name = args[2]
            table_data = load_table_data(table_name)
            if "where" in args:
                where_index = args.index("where") + 1
                where_clause = parse_where_clause(args[where_index:])
                select(metadata, table_name, table_data, where_clause)
            else:
                select(metadata, table_name, table_data)
        elif command == "update":
            table_name = args[1]
            set_index = args.index("set") + 1
            where_index = args.index("where")
            set_clause = parse_set_clause(args[set_index:where_index])
            where_clause = parse_where_clause(args[where_index + 1:])
            table_data = load_table_data(table_name)
            table_data = update(metadata, table_name, table_data, set_clause, where_clause) or table_data
            save_table_data(table_name, table_data)
        elif command == "delete":
            table_name = args[2]
            where_index = args.index("where") + 1
            where_clause = parse_where_clause(args[where_index:])
            table_data = load_table_data(table_name)
            table_data = delete(metadata, table_name, table_data, where_clause) or table_data
            save_table_data(table_name, table_data)
        elif command == "info":
            table_name = args[1]
            info(metadata, table_name)
        else:
            print(f"Функции {command} нет. Попробуйте снова.")
