from prettytable import PrettyTable

from .decorators import confirm_action, create_cacher, handle_db_errors, log_time
from .utils import load_table_data

# Подключаем кэш
cache = create_cacher()


# -------------------
# Работа с таблицами
# -------------------
@handle_db_errors
def create_table(metadata, table_name, columns):
    if table_name in metadata:
        raise ValueError(f'Tаблица "{table_name}" уже существует.')
    schema = {"ID": "int"}
    for col in columns:
        if ":" not in col:
            raise ValueError(f'Некорректное значение: {col}')
        name, typ = col.split(":")
        if typ not in ["int", "str", "bool"]:
            raise ValueError(f'Некорректное значение: {typ}')
        schema[name] = typ
    metadata[table_name] = schema
    cols_str = ", ".join(f"{k}:{v}" for k, v in schema.items())
    print(f'Таблица "{table_name}" успешно создана со столбцами: {cols_str}')
    return metadata


@handle_db_errors
@confirm_action("удаление таблицы")
def drop_table(metadata, table_name):
    if table_name not in metadata:
        raise KeyError(f'Таблица "{table_name}" не существует.')
    metadata.pop(table_name)
    print(f'Таблица "{table_name}" успешно удалена.')
    return metadata


@handle_db_errors
def list_tables(metadata):
    if not metadata:
        print("Нет таблиц.")
        return metadata
    for table in metadata:
        print(f"- {table}")
    return metadata


# -------------------
# CRUD операции
# -------------------
@handle_db_errors
@log_time
def insert(metadata, table_name, values, table_data):
    if not isinstance(table_data, list):
        table_data = []

    if table_name not in metadata:
        raise KeyError(table_name)
    schema = metadata[table_name]
    if len(values) != len(schema) - 1:
        raise ValueError("Количество значений не соответствует количеству столбцов")

    new_id = max([row["ID"] for row in table_data], default=0) + 1
    record = {"ID": new_id}

    for (col, typ), val in zip(list(schema.items())[1:], values):
        if typ == "int":
            val = int(val)
        elif typ == "bool":
            val = val if isinstance(val, bool) else str(val).lower() == "true"
        record[col] = val

    table_data.append(record)
    print(f'Запись с ID={new_id} успешно добавлена в таблицу "{table_name}".')
    return table_data


@handle_db_errors
@log_time
def select(metadata, table_name, table_data, where_clause=None):
    if not isinstance(table_data, list):
        table_data = []

    if table_name not in metadata:
        raise KeyError(table_name)

    if where_clause:
        cache_key = (table_name, frozenset(where_clause.items()))
        cached_result = cache(cache_key, lambda: None)
        if cached_result:
            filtered = cached_result
        else:
            filtered = [
                row
                for row in table_data
                if all(row.get(k) == v for k, v in where_clause.items())
            ]
            cache(cache_key, lambda: filtered)
    else:
        filtered = table_data

    if not filtered:
        print("Нет записей.")
        return []

    table = PrettyTable()
    table.field_names = list(metadata[table_name].keys())
    for row in filtered:
        table.add_row([row.get(f) for f in table.field_names])
    print(table)
    return filtered


@handle_db_errors
@log_time
def update(metadata, table_name, table_data, set_clause, where_clause):
    if not isinstance(table_data, list):
        table_data = []

    if table_name not in metadata:
        raise KeyError(table_name)
    updated_count = 0
    for row in table_data:
        if all(row.get(k) == v for k, v in where_clause.items()):
            for k, v in set_clause.items():
                typ = metadata[table_name][k]
                if typ == "int":
                    v = int(v)
                elif typ == "bool":
                    v = v if isinstance(v, bool) else str(v).lower() == "true"
                row[k] = v
            updated_count += 1
    print(f"{updated_count} запись(и) успешно обновлена(ы) в таблице \"{table_name}\".")
    return table_data


@handle_db_errors
@confirm_action("удаление записи")
@log_time
def delete(metadata, table_name, table_data, where_clause):
    if not isinstance(table_data, list):
        table_data = []

    if table_name not in metadata:
        raise KeyError(table_name)
    new_data = [
        row
        for row in table_data
        if not all(row.get(k) == v for k, v in where_clause.items())
    ]
    deleted_count = len(table_data) - len(new_data)
    print(f"{deleted_count} запись(и) успешно удалена(ы) из таблицы \"{table_name}\".")
    return new_data


@handle_db_errors
def info(metadata, table_name):
    if table_name not in metadata:
        raise KeyError(table_name)
    table_data = load_table_data(table_name)
    if not isinstance(table_data, list):
        table_data = []
    schema = metadata[table_name]
    print(f"Таблица: {table_name}")
    cols_str = ", ".join(f"{k}:{v}" for k, v in schema.items())
    print(f"Столбцы: {cols_str}")
    print(f"Количество записей: {len(table_data)}")


# -------------------
# Помощь
# -------------------
def print_help():
    print("\n***Процесс работы с таблицей***")
    print("Функции:")
    print("<command> create_table <имя_таблицы> <столбец1:тип> .. - создать таблицу")
    print("<command> list_tables - показать список всех таблиц")
    print("<command> drop_table <имя_таблицы> - удалить таблицу")
    print("<command> insert into <имя_таблицы> values (...) - добавить запись")
    print("<command> select from <имя_таблицы> [where ...] - прочитать записи")
    print("<command> update <имя_таблицы> set ... where ... - обновить запись")
    print("<command> delete from <имя_таблицы> where ... - удалить запись")
    print("<command> info <имя_таблицы> - информация о таблице")
    print("<command> exit - выход из программы")
    print("<command> help - справочная информация\n")
