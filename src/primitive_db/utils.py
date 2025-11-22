import json
import os

DATA_DIR = "data"

def load_metadata(filepath):
    """Загружает метаданные из JSON файла. Если файл не найден, возвращает пустой словарь."""
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)
            return data if isinstance(data, dict) else {}
    except FileNotFoundError:
        return {}


def save_metadata(filepath, data):
    """Сохраняет метаданные в JSON файл."""
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

def load_table_data(table_name):
    """Загружает данные таблицы из JSON файла. Если файла нет — возвращает пустой список."""
    filepath = os.path.join(DATA_DIR, f"{table_name}.json")
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return []

def save_table_data(table_name, data):
    """Сохраняет данные таблицы в JSON файл."""
    os.makedirs(DATA_DIR, exist_ok=True)
    filepath = os.path.join(DATA_DIR, f"{table_name}.json")
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
