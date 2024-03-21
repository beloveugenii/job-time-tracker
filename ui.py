# libsui.py

from os import get_terminal_size
from time import sleep

version = '0.0.2.1'

def line(): print('-' * get_terminal_size()[0])

def clear(): print('\033[H\033[2J', end='')

def hide_cursor(): print("\033[?25l")

def restore_cursor(): print("\033[?25h")

def save_cursor_pos(): print("\033[s")

def restore_cursor_pos(): print("\033[u")

def promt(what):
    # takes a string
    what = str(what)
    # return gived string in looks 'String: '
    return input(what[0].upper() + what[1:] + ': ')

def get_fields_len(array):
    # takes a list of tuples
    fields = []

    # defines the number of rows and columns
    rows = len(array)
    try:
        cols =  max([len(col) for col in array])
    except ValueError:
        cols = 0
    
    # expands each row to the maximum number of columns
    for r in range(rows):
        while len(array[r]) < cols:
                array[r] = array[r] + ('',)
    
    # defines width of every columns
    for c in range(cols):
        fields.append(max(len(str(array[r][c])) for r in range(rows)))
    
    screen_width = get_terminal_size()[0]

    # defines wifth of empty fields 
    sep_len = (screen_width - sum(fields)) // ( len(fields) + 1)
    
    while sum(fields) + (cols + 1) * sep_len > screen_width:
        sep_len -= 1

    # returns list of every columns width and empty field width
    return fields, sep_len


def print_as_table(items, sep):
    # takes the list of tuples
    fields, sep_len = get_fields_len(items)

    # prints tuples elements in fieldd separating with empty spaces
    for row in items:
        for c in range(len(row)):
            print('%s%-*s' % (sep * sep_len, fields[c], row[c]), end='')
        else:
            print('%s' % (sep * sep_len,))



def header(text):
    # takes a string and transform it to list of tuples with single element
    # print a string in center of screen
    line()
    print_as_table([(text,), ],' ')
    line()

def menu(array, cols):
    # takes a list ol menu elements and columns number
    menu_lst = []
    array = list(map(lambda word: '[' + word[0]+ ']' + word[1:], array))

    if len(array) % 2 == 1 and cols % 2 == 0:
        array.append('')
    # convert list to list of tuples
    while len(array) > 0:
        tmp = []
        for t in range(cols):
            try:
                tmp.append(array.pop(0))
            except:
                pass
        menu_lst.append(tuple(tmp))

    # print list of tuples like menu
    line()
    if cols > 0:
        print_as_table(menu_lst, ' ')
        line()

def screen(header_title, func, menu_lst, menu_cols):
    # takes a list with header text, some function, menu list and number of menu columns
    # clear the screen and prints header, output of body function and menu
    clear()
    header(header_title)
    func()
    menu(menu_lst, menu_cols)


messages = {
    'not_impl': 'Not implemented yet',
    'ua': 'Unsupported action',
    'small_str': 'Too small string',
    'need_gender': 'A gender designation is required: [mM or fF]',
    'need_number': 'A number is required',
    'not_in_list': 'User with this number not in list',
    'interactive':
        "Enter the numbers of the required workout programs separated by spaces\n'c' for creating new training\n'r' to remove existed training\n'e' for editing the training\n'h' show this help\n'q' quit",
    'users':
        "Type user ID for choosing\n'n' create new user\n'dNUM' for removing user with id NUM\n'h' show this help\n'q' quit",
    'diary':
        "Enter the name of the food to be entered in the diary\n'n' go to the next day\n'p' go to the previous day\n'l' show food in database\n't' go to sport assistant\n'h' show this help\n'q' quit",
    'food_db':
        "Enter the name of the food to be entered in database\n'a' analyze the complex dish\n'r' remove from database\n'h' show this help\n'q' go back",
    'analyzer':
        "Enter the name of the food to be entered in the diary\n'c' create a new dish\n'r' remove an existing dish\n'h' show this help\n'q' quit",
    'activity':
        "1.2 – минимальная активность, сидячая работа, не требующая значительных физических нагрузок\n1.375 – слабый уровень активности: интенсивные упражнения не менее 20 минут один-три раза в неделю\n1.55 – умеренный уровень активности: интенсивная тренировка не менее 30-60 мин три-четыре раза в неделю\n1.7 – тяжелая или трудоемкая активность: интенсивные упражнения и занятия спортом 5-7 дней в неделю или трудоемкие занятия\n1.9 – экстремальный уровень: включает чрезвычайно активные и/или очень энергозатратные виды деятельности",
}


def show_help(*args):
    print(messages[args[0]])
    if len(args) > 1:
        sleep(args[1])
    else:
        empty_input = input()

class Completer():
    def __init__(self, options):
        self.options = sorted(options)
        return

    def complete(self, text, state):
        response = None
        if state == 0:
            # Если какой-то текст передан в метод
            if text:
                # вернуть список слов из списка, которые начинаются на текст
                self.matches = [s for s in self.options if s and s.startswith(text.lstrip())]
            else:
                # иначе вернуть весь список
                self.matches = self.options[:]

        # Вернуть элемент состояния из списка совпадений, если их много. 

        try:
            response = self.matches[state]
        except IndexError:
            response = None
        return response


