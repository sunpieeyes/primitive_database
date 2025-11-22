VALID_TYPES = {"int", "str", "bool"}

def create_table(metadata, table_name, columns):
    """Создаёт таблицу с указанными столбцами. Добавляет ID:int автоматически."""
    if table_name in metadata:
        print(f'Ошибка: Таблица "{table_name}" уже существует.')
        return metadata

    table_columns = {"ID": "int"}  # Автоматический ID

    for col in columns:
        if ":" not in col:
            print(f"Некорректное значение: {col}. Попробуйте снова.")
            return metadata
        name, typ = col.split(":", 1)
        if typ not in VALID_TYPES:
            print(f"Некорректное значение: {typ}. Попробуйте снова.")
            return metadata
        table_columns[name] = typ

    metadata[table_name] = table_columns
    print(f'Таблица "{table_name}" успешно создана со столбцами: {", ".join(f"{k}:{v}" for k,v in table_columns.items())}')
    return metadata

def drop_table(metadata, table_name):
    """Удаляет таблицу из метаданных."""
    if table_name not in metadata:
        print(f'Ошибка: Таблица "{table_name}" не существует.')
        return metadata
    del metadata[table_name]
    print(f'Таблица "{table_name}" успешно удалена.')
    return metadata

def list_tables(metadata):
    """Показывает список всех таблиц."""
    if not metadata:
        print("Нет таблиц.")
        return
    for table in metadata:
        print(f"- {table}")
