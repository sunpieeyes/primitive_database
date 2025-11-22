import os
import json
from prettytable import PrettyTable
from .utils import load_metadata, save_metadata

DATA_DIR = "data"
os.makedirs(DATA_DIR, exist_ok=True)

# -------------------------
# Таблицы
# -------------------------

def create_table(metadata, table_name, columns):
    if table_name in metadata:
        print(f'Ошибка: Таблица "{table_name}" уже существует.')
        return metadata

    schema = {"ID": "int"}
    for col in columns:
        try:
            col_name, col_type = col.split(":")
        except ValueError:
            print(f"Некорректное значение: {col}. Попробуйте снова.")
            return metadata
        if col_type not in ["int", "str", "bool"]:
            print(f"Некорректный тип данных: {col_type}. Поддерживаются int, str, bool.")
            return metadata
        schema[col_name] = col_type

    metadata[table_name] = schema

    # создаем пустой JSON файл таблицы
    table_path = os.path.join(DATA_DIR, f"{table_name}.json")
    if not os.path.exists(table_path):
        with open(table_path, "w", encoding="utf-8") as f:
            json.dump([], f, indent=4)

    print(f'Таблица "{table_name}" успешно создана со столбцами: {", ".join(f"{k}:{v}" for k,v in schema.items())}')
    return metadata


def drop_table(metadata, table_name):
    if table_name not in metadata:
        print(f'Ошибка: Таблица "{table_name}" не существует.')
        return metadata

    del metadata[table_name]
    table_path = os.path.join(DATA_DIR, f"{table_name}.json")
    if os.path.exists(table_path):
        os.remove(table_path)

    print(f'Таблица "{table_name}" успешно удалена.')
    return metadata


def list_tables(metadata):
    if not metadata:
        print("Список таблиц пуст.")
        return
    for table in metadata:
        print(f"- {table}")


# -------------------------
# CRUD
# -------------------------

def load_table_data(table_name):
    path = os.path.join(DATA_DIR, f"{table_name}.json")
    if not os.path.exists(path):
        return []
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def save_table_data(table_name, data):
    path = os.path.join(DATA_DIR, f"{table_name}.json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)


def insert(metadata, table_name, values):
    if table_name not in metadata:
        print(f'Ошибка: Таблица "{table_name}" не существует.')
        return

    schema = metadata[table_name]
    if len(values) != len(schema) - 1:  # без ID
        print("Ошибка: количество значений не соответствует количеству столбцов.")
        return

    table_data = load_table_data(table_name)
    new_id = max([r["ID"] for r in table_data], default=0) + 1
    record = {"ID": new_id}

    for i, col_name in enumerate(list(schema.keys())[1:]):  # пропускаем ID
        col_type = schema[col_name]
        val = values[i]
        if col_type == "int":
            try:
                val = int(val)
            except ValueError:
                print(f"Некорректное значение для {col_name}: {val}")
                return
        elif col_type == "bool":
            if str(val).lower() == "true":
                val = True
            elif str(val).lower() == "false":
                val = False
            else:
                print(f"Некорректное значение для {col_name}: {val}")
                return
        record[col_name] = val

    table_data.append(record)
    save_table_data(table_name, table_data)
    print(f'Запись с ID={new_id} успешно добавлена в таблицу "{table_name}".')


def select(metadata, table_name, where_clause=None):
    if table_name not in metadata:
        print(f'Ошибка: Таблица "{table_name}" не существует.')
        return

    table_data = load_table_data(table_name)
    if where_clause:
        filtered = [
            r for r in table_data if all(r.get(k) == v for k, v in where_clause.items())
        ]
    else:
        filtered = table_data

    if not filtered:
        print("Нет записей.")
        return

    pt = PrettyTable()
    pt.field_names = list(metadata[table_name].keys())
    for row in filtered:
        pt.add_row([row[k] for k in pt.field_names])
    print(pt)


def update(metadata, table_name, set_clause, where_clause):
    if table_name not in metadata:
        print(f'Ошибка: Таблица "{table_name}" не существует.')
        return

    table_data = load_table_data(table_name)
    updated_count = 0
    for row in table_data:
        if all(row.get(k) == v for k, v in where_clause.items()):
            for k, v in set_clause.items():
                if k in row:
                    row[k] = v
            updated_count += 1

    save_table_data(table_name, table_data)
    print(f"Запись(и) с ID={updated_count} в таблице \"{table_name}\" успешно обновлена.")


def delete(metadata, table_name, where_clause):
    if table_name not in metadata:
        print(f'Ошибка: Таблица "{table_name}" не существует.')
        return

    table_data = load_table_data(table_name)
    new_data = [r for r in table_data if not all(r.get(k) == v for k, v in where_clause.items())]
    deleted_count = len(table_data) - len(new_data)
    save_table_data(table_name, new_data)
    print(f"Запись(и) с ID={deleted_count} успешно удалена из таблицы \"{table_name}\".")


def info(metadata, table_name):
    if table_name not in metadata:
        print(f'Ошибка: Таблица "{table_name}" не существует.')
        return
    schema = metadata[table_name]
    table_data = load_table_data(table_name)
    print(f"Таблица: {table_name}")
    print("Столбцы:", ", ".join(f"{k}:{v}" for k, v in schema.items()))
    print("Количество записей:", len(table_data))


def print_help():
    print("\n***Процесс работы с таблицей***")
    print("Функции:")
    print("<command> create_table <имя_таблицы> <столбец1:тип> .. - создать таблицу")
    print("<command> list_tables - показать список всех таблиц")
    print("<command> drop_table <имя_таблицы> - удалить таблицу")
    print("<command> insert into <имя_таблицы> values (...) - добавить запись")
    print("<command> select from <имя_таблицы> [where ...] - вывести записи")
    print("<command> update <имя_таблицы> set ... where ... - обновить запись")
    print("<command> delete from <имя_таблицы> where ... - удалить запись")
    print("<command> info <имя_таблицы> - информация о таблице")
    print("\nОбщие команды:")
    print("<command> exit - выход из программы")
    print("<command> help - справочная информация\n")
