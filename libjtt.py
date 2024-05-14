import datetime
from common import *
from ui import helps, get_const
from init_db import *

weekdays_names = get_const('strings.json', 'weekdays_names')
months_names = get_const('strings.json', 'months_names')
menu_entries = get_const('strings.json', 'menu_entries')
dd = [i for i in get_const('strings.json', 'days')]
holydays = get_const('strings.json', 'holydays')

messages = {
    'no_line': 'No line with entered number',
    'not_impl': 'Not implemented yet',
    'ua': 'Unsupported action',
    'need_number': 'A number is required',
    'cc': "Can't convert date",
    'nea': 'Not enought arguments',
    'ndip': 'Нет данных за указанный период...',
    'main_help':
        "'a date, day hours and night hours' you worked\n'c param value' to set or change period parameter to value\n'r' number of line to remove\n'n' go to the next month\n'p' go to the previous month\n'h' show this help\n'q' quit",
}


# ФУНКЦИИ ПОЛУЧЕНИЯ ДАННЫХ ИЗ БД

def get_current_period(cur):
    # Функция получает объект-указатель на ДБ
    # Функция возвращает кортеж из двух элементов (str, bool)
    was_changed = False
    current_period = check_data_in_table(cur, 'config')

    if current_period is None:
        # Получаем текущий период из БД и запоминаем его
        current_period = (cur.execute("SELECT date()").fetchone())[0][:7]
        cur.execute('INSERT INTO config VALUES(?)', (current_period, ))
        was_changed = True
    else:
        # Если получилось получить значение из БД, приводим его к виду ГГГГ-ММ
        current_period = current_period[0]

    return current_period, was_changed

def get_period_params(cur, current_period):
    # Функция обращается к БД для получения расчетных данных за период
    # Если нет данных за период - вставляет в БД значения по-умолчанию
    # Возвращает кортеж из (словарь с данными, логическое значение)
    res, was_changed = None, False
    
    while res is None:
        res = cur.execute('SELECT * FROM period_params WHERE period = ?', (current_period,)).fetchone()

        if res is None:
            dp = check_data_in_table(cur, 'default_params')
            cur.execute("INSERT INTO period_params ('period', 'salary', 'bonus', 'dprise', 'tax') VALUES (?, ?, ?, ?, ?)", (current_period, *dp))
            was_changed = True
    
    return dict(map(lambda *args: args, ('period', 'salary', 'first', 'second', 'relax', 'bonus', 'dprise', 'tax'), res) ), was_changed

def get_period_data(cur, current_period):
    # Функция обращается к БД и извлекает строки данных за указанный период
    # Возвращает список кортежей или None
    return cur.execute("SELECT rowid, * FROM period_data WHERE date LIKE ? ORDER BY date", (current_period + '-%', )).fetchall()

def get_date(d):
    # Передаем в функцию название и получаем дату
    if d == 'now' or d == 'today' or d.startswith('n'):
        return datetime.date.today()
    elif d == 'yesterday' or d.startswith('y'):
        return datetime.date.today() - datetime.timedelta(1)
    elif d == 'tomorrow' or d.startswith('t'):
        return datetime.date.today() + datetime.timedelta(1)
    elif d == '':
        return None
    
    # Если передано не название, пытаемся разбить его по символу точки
    td = d.split('.')
    # Если элементов больше 2, то возращаем дату 
    if len(d) > 2:
        if len(td[2]) < 4:
            td[2] = '20' + td[2]
        return '-'.join(td[::-1])
    else:
        return None


# ФУНКЦИИ - ДЕЙСТВИЯ

def command_parser(commands):
    # Запрашивает ввод комманды в виде 'команда' 'аругменты'
    line = input('>> ').lower().strip().split(' ')

    # Нет ввода или комманда не поддерживается
    if line[0] not in commands or line[0] == '':
        return None, None
    elif line[0] in commands:
        # Ввод только комманды, без аргументов
        if len(line) == 1:
            return line[0], None
        # Ввод подходящей команды с аргментами
        else:
            return line[0], line[1:]


def change_period(cur, current_period, direction):
    cp = datetime.date.fromisoformat(current_period + '-10')

    if direction == 'p':
        td = datetime.timedelta(days=-31)
        cp += td
    elif direction == 'n':
        td = datetime.timedelta(days=31)
        cp += td 

    rv = cur.execute('UPDATE config SET selected_period = ?', (cp.strftime("%Y-%m"), ))
    if rv is None:
        return False
    else:
        return True

def add_line(cur, *args):
    # Получает указатель и произвольное количетво аргументов для добавления строки в БД
    # Возвращает логическое значение успеха выполнения
    args = args[0]
    
    # Если аргументов нет - запраишваем их
    if args is None:
        print('Enter date, dh, nh')
        args = input().strip().split(' ')

    # Если аргументов не хватате - сообщаем об этом и выходим
    if len(args) < 2:
        helps(messages['nea'])
        return False
    # Значения по-умолчанию
    d, dh, nh = None, 0, 0
    
    # Пытаемся получить из аргумента приемлемое значение
    # Или, сообщив об ошибке, выходим
    d = get_date(args[0])
    if d is None:
        helps(messages['cc'])
        return False
    
    # Пытаемя преобразовать аргументы в float         
    try: 
        dh = str_to_float(args[1])
        nh = str_to_float(args[2])
    except: 
        pass
        
    # Вносим данные
    return cur.execute('INSERT INTO period_data VALUES(?, ?, ?)', (d, dh, nh))

def remove_line(cur, period_data, *args):
    # Получает указатель и необязательный аргумент для удаления из БД
    # Возвращает логическое значение успеха выполнения
    args = args[0]

    # Если аргументов нет - запраишваем их
    if args is None:
        print('Enter number of line to remove')
        num = input().strip()
    else:
        num = args[0]

    # Пытаемся преобразовать аргумент в int
    try:
        num = int(num)
    except:
        helps(messages['need_number'])
        return False

    if num > 0 and num <= len(period_data):
       # Удаляем данные если есть подходящая строка
       return cur.execute('DELETE FROM period_data where rowid = ?', (period_data[num - 1][0],))
    else:
        helps(messages['no_line'])
        return False
     

# ФУНКЦИИ ВЫЧИСЛЕНИЙ И ВЫВОДЫ

def pretty_period(current_period):
    d = current_period.split('-')
    return f'{months_names[int(d[1]) - 1]} {d[0]}'

def pretty_period_data(pd):
    # Получает список кортежей
    # Возвращает измененный список кортежей
    ppd = list()
    l = 0
    while l != len(pd):
        gd = datetime.date.fromisoformat(pd[l][1])
        ppd.append(
                (l + 1, gd.strftime('%d.%m.%y'), weekdays_names[gd.weekday()], pd[l][2], pd[l][3])
                )
        l += 1

    return ppd

def get_work_days(current_period):
    # Получает текущий период и определяем количество рабочих дней в нем
    # Учитываются праздничные дни, заданные в кортеже holydays
    # Возвращает целое число
    jdays = 0
    
    sd = datetime.datetime.strptime(current_period + '-01', '%Y-%m-%d')
    
    ed = (sd + datetime.timedelta(days=31)).replace(day=1) 

    while sd < ed:
        if sd.isoweekday() < 6 and not sd.strftime('%m-%d') in holydays: 
            jdays += 1
        sd += datetime.timedelta(days=1)

    return jdays

def calculate(period_params, period_data):
    if period_params is None:
        return None

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
            (f"Оклад {int(RD['SALARY'])}", f"Д/Ч {RD['JDAYS']}/{RD['NORM_H']}", f"заЧас {RD['PER_HOUR']}"), 
            (f"Налог {RD['TAX']}", f"ВсегоЧ {RD['TH']}", f"Ночные {RD['NH']}"), 
            (f"Грязн {RD['DIRTY']}", f"Чист {RD['CLEAR']}", f"Факт {RD['FACT']}")
            ]

