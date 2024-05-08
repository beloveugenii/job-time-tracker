import datetime
from time import sleep

weekdays_names = ('пн', 'вт', 'ср', 'чт', 'пт', 'сб', 'вс')

dd = ['now', 'tomorrow', 'yesterday']

months_names = ('январь', 'февраль', 'март', 'апрель', 'май', 'июнь', 'июль', 'август', 'сентябрь', 'октябрь', 'ноябрь', 'декабрь')

holydays = ('05-01', '01-01', '05-09', '03-08', '02-23')

messages = {
    'no_line': 'No line with entered number',
    'not_impl': 'Not implemented yet',
    'ua': 'Unsupported action',
    'need_number': 'A number is required',
    'cc': "Can't convert date",
    'nea': 'Not enought arguments',
    'main_help':
        "'a date, day hours and night hours' you worked\n'c param value' to set or change period parameter to value\n'r' number of line to remove\n'n' go to the next month\n'p' go to the previous month\n'h' show this help\n'q' quit",
}

def get_current_period(cur):
    # Функция получает объект-указатель на ДБ
    # Функция возвращает кортеж из двух элементов (str, bool)
    was_changed = False
    current_period = (cur.execute('SELECT selected_period FROM config').fetchone())

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
            dp = cur.execute('SELECT * FROM default_params').fetchone()
            cur.execute("INSERT INTO period_params ('period', 'salary', 'bonus', 'dprise', 'tax') VALUES (?, ?, ?, ?, ?)", (current_period, *dp))
            was_changed = True
    
    return dict(map(lambda *args: args, ('period', 'salary', 'first', 'second', 'relax', 'bonus', 'dprise', 'tax'), res) ), was_changed

def get_period_data(cur, current_period):
    # Функция обращается к БД и извлекает строки данных за указанный период
    # Возвращает список кортежей или None
    return cur.execute("SELECT rowid,* FROM period_data WHERE date LIKE ? ORDER BY date", (current_period + '-%', )).fetchall()


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

def help(*args):

    print(messages[args[0]])

    if len(args) > 1:
        sleep(args[1])
    else:
        empty_input = input()





        

    


def add_line(cur, *args):
    # Получает указатель и произвольное количетво аргументов для добавления строки в БД
    # Возвращает логическое значение успеха выполнения
    args = args[0]
    
    # Если аргументов нет - запраишваем их
    if len(args) == 0:
        print('Enter date, dh, nh')
        args = input().strip().split(' ')

    # Если аргументов не хватате - сообщаем об этом и выходим
    if len(args) < 2:
        help('nea')
        return False
    # Значения по-умолчанию
    d, dh, nh = None, 0, 0
    
    # Пытаемся получить из аргумента приемлемое значение
    # Или, сообщив об ошибке, выходим
    d = get_date(args[0])
    if d is None:
        help('cc')
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
    if len(args) == 0:
        print('Enter number of line to remove')
        num = input().strip().split(' ')
    else:
        num = args[0]
    
    # Пытаемся преобразовать аргумент в int
    try:
        num = int(num)
    except:
        help('need_number')
        return False

    if num > 0 and num <= len(period_data):
       # Удаляем данные если есть подходящая строка
       return cur.execute('DELETE FROM period_data where rowid = ?', (period_data[num - 1][0],))
    else:
        help('no_line')
        return False
        





    
def str_to_float(str=0):
    try:
        str = float(str)
    except:
        str = 0.0

    return str


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


def command_parser(commands):
    line = input('>> ').lower().strip().split(' ')

    if len(line) == 0 or line[0] not in commands:
            # если комманда не поддерживается
        help('ua')
        return '', ''
    elif len(line) == 1 and line[0] in commands:
            # если поддерживается, но нет аргументов
        return line[0], ''
    elif len(line) > 1:
            # если поддерживается и есть аргументы
        return line[0], line[1:]



