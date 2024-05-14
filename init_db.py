# Создание таблиц в БД
# Вносить в словарь название таблицы в качестве ключа и параметры в качетсве значения

TABLES = {
        'period_data': '(date TEXT, dh REAL, nh REAL)',
        'period_params': '(period TEXT, salary REAL, first REAL, second REAL, relax REAL, bonus REAL, dprise REAL, tax REAL)',
        'config': '(selected_period TEXT)',
        'default_params': '(salary REAL, bonus REAL, dprise REAL, tax REAL)',
        }

def check_data_in_table(cur, table_name):
    # Функция получает указатель и имя таблицы
    # Если есть хоть одна запись - возвращает кортеж, иначе - None
    return cur.execute('SELECT * FROM ' + table_name).fetchone()

def create_tables(cur):
    # Функция получает объект указателя на БД, создает таблицы и заполняет их при необходимости
    ct = 'CREATE TABLE IF NOT EXISTS'

    for t, p in TABLES.items():
        cur.execute(' '. join((ct, t , p)))
    
    for table in ['default_params']:
        if check_data_in_table(cur, table) is None:
            cur.execute('INSERT INTO default_params VALUES(49504, 0.15, 0.04, 0.13)')


