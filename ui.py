# CHANGELOG
#  v0.0.1
#  Первый выпуск Perl-библиотеки для построения простого пользовательского интерфейса
	#  - библиотека оформлена в виде модуля
	#  - добавлена POD-документация

#  v0.0.1b
#  Первый выпуск Python-библиотеки, ее функционал приближен к Perl версии

#  v0.0.1c
#  Из обеих библиотек удалены функции demo() и loop(), функция screen() больше не
#  поддерживает автодополнение

#  v0.0.2
#  Остановка разработки Perl-версии
#  Вся информация будет содержаться в файле с функциями

#  v0.0.2.1
#  Коментарии на русском
#  line() теперь может принимать любой символ для печати 

from os import get_terminal_size                       

version = '0.0.2'

def line(sep=None):
    if sep is None:
        sep = '-'
    
    print(sep * get_terminal_size()[0])

def clear():
    # clears the screen
    print('\033[H\033[2J', end='')

def promt(what):
    # takes a string
    what = str(what)
    # return gived string in looks 'String: '
    return input(what[0].upper() + what[1:] + ': ')

def get_fields_len(array):
    # В функцию передается массив, где каждый элемент - строка таблицы
    fields = []

    # Количество строк - это длина массива (сверху вниз)
    rows = len(array)
    
    # Для каждой строки определяется количество элементов в ней
    # Количество колонок таблицы - наибольшее количество элементов в какой-то строке
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

def hide_cursor():
    print("\033[?25l")

def restore_cursor():
    print("\033[?25h")

def save_cursor_pos():
    print("\033[s")

def restore_cursor_pos():
    print("\033[u")

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


