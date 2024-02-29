import datetime

def create_tables(cur):
    tables_was_created = 0
    stmts = (
        'CREATE TABLE IF NOT EXISTS period_data (date TEXT, dh REAL, nh REAL)', 
        'CREATE TABLE IF NOT EXISTS period_params (period TEXT, salary REAL, first REAL, second REAL, relax REAL, bonus REAL, dprise REAL, tax REAL)',
        'CREATE TABLE IF NOT EXISTS config (selected_period TEXT)',
        )

    for stmt in stmts:
        cur.execute(stmt)


weekdays_names = ('Пн', 'Вт', 'Ср', 'Чт', 'Пт', 'Сб', 'Вс')

from time import sleep

messages = {
    'not_impl': 'Not implemented yet',
    'ua': 'Unsupported action',
    'small_str': 'Too small string',
    'need_number': 'A number is required',
    'diary':
        "Enter the name of the food to be entered in the diary\n'n' go to the next day\n'p' go to the previous day\n'l' show food in database\n't' go to sport assistant\n'h' show this help\n'q' quit",
}

def help(*args):

    print(messages[args[0]])

    if len(args) > 1:
        sleep(args[1])
    else:
        empty_input = input()

def get_period_params(cur, current_period):
    # Функция обращается к БД и извлекает строку с данными для расчета за указанный период
    res = cur.execute('SELECT * FROM period_params WHERE period = ?', (current_period,)).fetchone()

    if res is None:
        return None
    else:
        # Возвращает словарь с параметрами
        return dict(map(lambda *args: args, ('period', 'salary', 'first', 'second', 'relax', 'bonus', 'dprise', 'tax'), res) )


def get_period_data(cur, current_period):
    period_data = list()
    
    # Функция обращается к БД и извлекает строки данных за указанный период
    res = cur.execute("SELECT * FROM period_data WHERE date LIKE ?", (current_period + '-%', )).fetchall()

    if res is None:
        return None
    else:
        for line in res:
            given_date = datetime.date.fromisoformat(line[0])
            new_look = given_date.strftime('%d.%m.%y')
            wday = weekdays_names[given_date.weekday()]

            period_data.append((new_look, wday, line[1], line[2]))
    
    # функция возвращает список кортежей в дополненном и измененном виде
        return period_data
    



def calculate(period_params, period_date):
    total_work_days = 23
    per_day = 0



def isfloat(what):
    if what.startswith('-'):
        what = what[1:]
    parts = what.split('.')
    return len(parts) == 2 and parts[0].isnumeric() and parts[1].isnumeric()

def is_valid(value, type_str, char_list = None):

    v_types = ( 'is_number', 'is_num', 'is_float', 'is_fl',
        'is_negative', 'is_neg', 'in_lst', 'in_ls', 'len_g', )

    if type_str not in v_types:
        raise ValueError(f'"{type_str}" is not implemented yet')

    value = str(value).strip()

    return (
        type_str.startswith('is_num') and value.isnumeric() or
        type_str.startswith('is_neg') and value.startswith('-') or
        type_str.startswith('is_fl') and isfloat(value) or
        type_str.startswith('in_ls') and value in char_list# or
        #  type_str.startswith('len_g') and len(value) >
    )

