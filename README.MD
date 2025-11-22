# Primitive Database

Простая консольная база данных с поддержкой операций CRUD, декораторов для обработки ошибок, логирования времени и кэширования.

## Описание проекта

Проект реализует мини-базу данных с возможностью:
- Создавать и удалять таблицы
- Добавлять, обновлять, удалять и выбирать записи
- Просматривать информацию о таблицах
- Логировать время выполнения команд
- Подтверждать опасные операции
- Кэшировать результаты выборки

Проект полностью построен на функциях, без использования классов. Хранение данных осуществляется в JSON-файлах.

---

## Установка

1. Клонируйте репозиторий:
```bash
git clone https://github.com/sunpieeyes/primitive_database
cd project2_Shevchenko_Sergey

2. Установите зависимости через poetry:
poetry install

Запуск проекта
poetry run project

3. ОСНОВНЫЕ КОМАНДЫ
Работа с таблицами

Создать таблицу:

create_table <имя_таблицы> <столбец1:тип> <столбец2:тип> ...

Пример:
create_table users name:str age:int is_active:bool

Показать список таблиц:
list_tables

Удалить таблицу:
drop_table <имя_таблицы>

4. CRUD ОПЕРАЦИИ

Добавить запись:
insert into <имя_таблицы> values (<значение1>, <значение2>, ...)

Прочитать записи:
select from <имя_таблицы> [where column=value]

Обновить запись:
update <имя_таблицы> set column=value where column=value

Удалить запись:
delete from <имя_таблицы> where column=value

Информация о таблице:
info <имя_таблицы>

5. ДОПОЛНИТЕЛЬНО

Справка по командам:
help

Выход из программы:
exit

6. ПРИМЕР СЦЕНАРИЯ РАБОТЫ
>>> create_table users name:str age:int is_active:bool
Таблица "users" успешно создана со столбцами: ID:int, name:str, age:int, is_active:bool

>>> insert into users values ("Alice", 25, True)
Запись с ID=1 успешно добавлена в таблицу "users".

>>> select from users
+----+-------+-----+-----------+
| ID | name  | age | is_active |
+----+-------+-----+-----------+
| 1  | Alice | 25  | True      |
+----+-------+-----+-----------+

>>> update users set age=26 where name="Alice"
1 запись(и) успешно обновлена(ы) в таблице "users".

>>> delete from users where name="Alice"
1 запись(и) успешно удалена(ы) из таблицы "users".

>>> drop_table users
Таблица "users" успешно удалена.

7.ТРЕБОВАНИЯ

Python 3.12+
Poetry
Библиотеки:
    prettytable
    prompt