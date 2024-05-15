import datetime
from common import *
from ui import helps, get_const

STRINGS = 'strings.json'
TABLES = 'tables.json'

# Получаем строковые данные из файл
weekdays_names = get_const(STRINGS, 'weekdays_names')
months_names = get_const(STRINGS, 'months_names')
menu_entries = get_const(STRINGS, 'menu_entries')
dd = [i for i in get_const(STRINGS, 'days')]
holydays = get_const(STRINGS, 'holydays')
requests = dict(get_const(STRINGS, 'requests'))
messages = dict(get_const(STRINGS, 'messages'))
tables = dict(get_const(TABLES, 'tables'))

# Функция возвращает текущие год и мясяц в виде ГГГГ-ММ и логичское значение
def get_current_period(cur):
    was_changed = False
    # Если не получается получить значение - генерируем его и записываем в БД
    current_period = check_data_in_table(cur, 'config')

    if current_period is None:
        current_period = (cur.execute("SELECT date()").fetchone())[0][:7]
        cur.execute('INSERT INTO config VALUES(?)', (current_period, ))
        was_changed = True
    else:
        current_period = current_period[0]

    return current_period, was_changed


# Функция возвращает параметры для текущего периода и логическое значение
def get_period_params(cur, current_period):
    res, was_changed = None, False
    
    while res is None:
        res = cur.execute('SELECT * FROM period_params WHERE period = ?', (current_period,)).fetchone()

        # Если нет данных за период - вставляет в БД значения по-умолчанию
        if res is None:
            dp = check_data_in_table(cur, 'default_params')
            cur.execute("INSERT INTO period_params ('period', 'salary', 'bonus', 'dprise', 'tax') VALUES (?, ?, ?, ?, ?)", (current_period, *dp))
            was_changed = True
    
    return dict(map(lambda *args: args, ('period', 'salary', 'first', 'second', 'relax', 'bonus', 'dprise', 'tax'), res) ), was_changed


# Функция возвращает данные за текущий период в виде списка кортежей или None
def get_period_data(cur, current_period):
    return cur.execute("SELECT rowid, * FROM period_data WHERE date LIKE ? ORDER BY date", (current_period + '-%', )).fetchall()


# Функция принимает значение в виде названия дня или даты в виде ДД.ММ.ГГГГ
# и возвращает строку с датой в виде ГГГГ-ММ-ДД
def get_date(d):
    if d == 'now' or d == 'today' or d.startswith('n'):
        return datetime.date.today()
    elif d == 'yesterday' or d.startswith('y'):
        return datetime.date.today() - datetime.timedelta(1)
    elif d == 'tomorrow' or d.startswith('t'):
        return datetime.date.today() + datetime.timedelta(1)
    elif d == '':
        return None

    td = d.split('.')
    if len(d) > 2:
        if len(td[2]) < 4:
            td[2] = '20' + td[2]
        return '-'.join(td[::-1])
    else:
        return None


# Функция запрашивает ввод от пользователя
# и возвращает строку (символ команды) и массив (с аргументами команды)
# При остутствии чего-либо возвращает None
def command_parser(commands):
    line = input('>> ').lower().strip().split(' ')

    if line[0] not in commands or line[0] == '':
        return None, None
    elif line[0] in commands:
        if len(line) == 1:
            return line[0], None
        else:
            return line[0], line[1:]


# Функция изменяет текущий период, записанный в БД
# Возвращает логическое значение
def change_period(cur, current_period, direction):
    cp = datetime.date.fromisoformat(current_period + '-10')

    if direction == 'p':
        td = datetime.timedelta(days=-31)
        cp += td
    elif direction == 'n':
        td = datetime.timedelta(days=31)
        cp += td 

    return cur.execute('UPDATE config SET selected_period = ?', (cp.strftime("%Y-%m"), ))


# Функция запрашивает ввод от пользователя в зависимости от переданной строки
def get_args_from_user(where):
    print(requests[where], end='')
    return input().strip().split(' ')


# Функция получает аргументы или запрашивает их и вносит данные в БД
# Возвращает логическое значение
def add_line(cur, *args):
    args = args[0]
    if args is None: args = get_args_from_user('add')
    if len(args) < 2: return helps(messages['nea'])

    d = get_date(args[0])
    if d is None: return helps(messages['cc'])
    
    dh, nh = 0, 0
    try: 
        dh = str_to_float(args[1])
        nh = str_to_float(args[2])
    except: 
        pass
        
    return cur.execute('INSERT INTO period_data VALUES(?, ?, ?)', (d, dh, nh))


# Функция получает аргументы или запрашивает их
# и изменяет строку данных за период
# Возвращает логическое значение 
def edit_line(cur, period_data, *args):
    args, num = args[0], None
    if args is None: args = get_args_from_user('edit')
    
    if is_valid(args[0], 'is_num'):
        num = int(args[0])
        args = args[1:]
    else: 
        return helps(messages['need_number'])
    
    if len(args) < 2: return helps(messages['nea'])
   
    d = get_date(args[0])
    if d is None: return helps(messages['cc'])
    
    dh, nh = 0, 0
    try: 
        dh = str_to_float(args[1])
        nh = str_to_float(args[2])
    except: 
        pass
       
    if num > 0 and num <= len(period_data):
        return cur.execute('UPDATE period_data SET date = ?, dh = ?, nh = ? where rowid = ?', (d, dh, nh, period_data[num - 1][0],))
    else: 
        return helps(messages['no_line'])


# Функция получает аргумент или запрашивает его
# Удаляет строку из данных за период
def remove_line(cur, period_data, *args):
    args, num = args[0], None
    if args is None: args = get_args_from_user('remove')

    if is_valid(args[0], 'is_num'): 
        num = int(args[0])
    else: 
        return helps(messages['need_number'])

    if num > 0 and num <= len(period_data):
       return cur.execute('DELETE FROM period_data where rowid = ?', (period_data[num - 1][0],))
    else: 
        return helps(messages['no_line'])     


# Функция вовращает текущий месяц в более красивом виде
def pretty_period(current_period):
    d = current_period.split('-')
    return f'{months_names[int(d[1]) - 1]} {d[0]}'


# Функция получает список кортежей и возвращает его в более красивом виде
def pretty_period_data(pd):
    ppd = list()
    l = 0
    while l != len(pd):
        gd = datetime.date.fromisoformat(pd[l][1])
        ppd.append((l + 1, 
                    gd.strftime('%d.%m.%y'), 
                    weekdays_names[gd.weekday()], 
                    pd[l][2], 
                    pd[l][3])
                )
        l += 1
    return ppd


# Функция возвращает количество будних дней за вычетом праздичных
def get_work_days(current_period):
    jdays = 0
    sd = datetime.datetime.strptime(current_period + '-01', '%Y-%m-%d')
    ed = (sd + datetime.timedelta(days=31)).replace(day=1) 

    while sd < ed:
        if sd.isoweekday() < 6 and not sd.strftime('%m-%d') in holydays: 
            jdays += 1
        sd += datetime.timedelta(days=1)

    return jdays

# Функция возвращает список кортежей для вывода в сводке
def calculate(period_params, period_data):
    if period_params is None:
        return None

    calc_str = get_const(STRINGS, 'calc_str')
    RD = dict()

    RD['SALARY'] = period_params['salary']
    RD['JDAYS'] = get_work_days(period_params['period'])
    
    RD['NORM_H'] = RD['JDAYS'] * 8
    
    RD['FACT'] = int(str_to_float(period_params['first']) + str_to_float(period_params['second']) + str_to_float(period_params['relax']))

    RD['PER_HOUR'] = int(RD['SALARY'] / RD['NORM_H'])
    
    RD['TH'] = int(sum([row[2] + row[3] for row in period_data]))
    RD['NH'] = RD['TH'] - int(sum([row[2] for row in period_data]))

    RD['DIRTY'] = int((RD['TH'] * RD['PER_HOUR']) * (1 + period_params['dprise'] + period_params['bonus']) + (0.5 * RD['PER_HOUR'] * RD['NH']))
    
    RD['TAX'] = int(RD['DIRTY'] * period_params['tax'])

    RD['CLEAR'] = RD['DIRTY'] - RD['TAX']

    return [
            (f"{calc_str[0]} {int(RD['SALARY'])}", f"{calc_str[1]} {RD['JDAYS']}/{RD['NORM_H']}", f"{calc_str[2]} {RD['PER_HOUR']}"), 
            (f"{calc_str[3]} {RD['TAX']}", f"{calc_str[4]} {RD['TH']}", f"{calc_str[5]} {RD['NH']}"), 
            (f"{calc_str[6]} {RD['DIRTY']}", f"{calc_str[7]} {RD['CLEAR']}", f"{calc_str[8]} {RD['FACT']}")
            ]

# Функция проверяет, есть ли в таблице хоть одна запись
def check_data_in_table(cur, table_name):
    return cur.execute('SELECT * FROM ' + table_name).fetchone()

# Функция для начального создания таблиц в БД
def create_tables(cur):
    ct = 'CREATE TABLE IF NOT EXISTS'

    for t, p in tables.items():
        cur.execute(' '. join((ct, t , p)))
    
    for table in ['default_params']:
        if check_data_in_table(cur, table) is None:
            cur.execute('INSERT INTO default_params VALUES(49504, 0.15, 0.04, 0.13)')

