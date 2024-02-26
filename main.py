#!/usr/bin/env python3

import sqlite3, readline, signal, sys, re
from ui import *

PROG_NAME = 'jtt-parser'
VERSION = '0.1.0'
DB_NAME = sys.path[0] + '/data.db'

con = sqlite3.connect(DB_NAME)
cur = con.cursor()

cur.execute('CREATE TABLE IF NOT EXISTS data (date TEXT, dh REAL, nh REAL)')
cur.execute('CREATE TABLE IF NOT EXISTS config (period TEXT, salary REAL, first REAL, second REAL, relax REAL, bonus REAL, dprise REAL, tax REAL)')

for file in sys.argv[1:]:
    f = open(file, 'r')
    config = dict.fromkeys(['period', 'selary','first', 'second', 'relax', 'bonus', 'dprise', 'tax'], None)
    data_lines = list()

    for line in f:
        line=line[:-1]

        # ищем параметры конфигурации
        sep = line.find('=')
        if sep != -1:
            (k, v) = (line[:sep], line[sep+1:])
            config[k] = v
        # остальные строки
        else:
            pass

    print(config)
            

#  current_date = datetime.date.today().isoformat()

#  def get_dates():
    #  import datetime
    #  current_date = datetime.date.today().isoformat()
    #  date_tuple = current_date.split('-')
    #  start_date = datetime.date.fromisoformat('-'.join(date_tuple[:2] + ['01']))
    #  end_date = datetime.date.fromisoformat(date_tuple[0] + '-' + str(int(date_tuple[1]) + 1).zfill(2) + '-01')
    #  return (current_date, start_date, end_date)


#  (current_date, start_date, end_date) = get_dates()
#  db_was_changed = False
#  current_date_was_changed = True
#  #  cur.execute('INSERT INTO data VALUES(?, ?, ?)', (date, match[2], match[3]))
#  #  data_from_db = cur.execute('SELECT * FROM data where date >= date(?, \'start of month\')', (current_date.isoformat(),)).fetchall()
#  #  con.commit()

#  #  # Enable SIG handlers and configure readline
#  #  signal.signal(signal.SIGINT, sigint_handler)
#  #  readline.set_completer_delims('\n,')

#  #  # Try to get id of current user
#  #  user_id = get_user_id_from_db(cur)

#  #  if user_id is None:
    #  #  user_id = set_user(cur)
    #  #  con.commit()

#  #  # Get user data and diary from db
#  #  user_data = get_user_data_by_id(cur, user_id)

#  #  food_list = get_food_list(cur)

#  #  while True:
    #  #  screen_name = 'diary'
    #  #  ui.clear()
    #  #  if db_was_changed:
        #  #  food_list = get_food_list(cur)
        #  #  db_was_changed = False

   

    #  #  diary = get_data_for_diary(cur, current_date.strftime('%Y-%m-%d'), user_id)
    #  #  kcal_norm = libsd.get_calories_norm(user_data)
    #  #  kcal_per_day = '%.1f' % sum([line[2] for line in diary])
#  while(True):
    #  if current_date_was_changed:
        #  data_from_db = cur.execute('SELECT * FROM data where date >= ? and date <= ?', (start_date, end_date)).fetchall()
        #  current_date_was_changed = False

    #  screen(
        #  PROG_NAME + ': ' + current_date,
        #  lambda:
            #  print_as_table(data_from_db, ' '),
            #  (), 0
        #  )
    #  #  ui.screen(
        #  #  user_data['name'] + ': ' + libsd.HEADERS[screen_name] + ' ' + current_date.strftime('%Y-%m-%d'),
        #  #  lambda:
        #  #  ui.print_as_table( [('норма калорий'.upper(), '', kcal_norm)] + diary + [('всего'.upper(), '', kcal_per_day)],  ' ' ) if diary else print(libsd.EMPTY_BODY[screen_name] + f' {current_date}'),
        #  #  libsd.MENUS_ENTRIES[screen_name], 2)

    #  #  # Enable tab-completion
    #  #  readline.parse_and_bind('tab: complete')
    #  #  readline.set_completer(c.Completer([food[0] for food in food_list]).complete)

    #  action = input('>> ').lower().strip()
    #  if action == 'q': break
    #  elif action == 'p': 
        #  current_date -= datetime.timedelta(days = 31)
        #  current_date_was_changed = True
    #  elif action == 'n': 
        #  current_date += datetime.timedelta(days = 31)
        #  current_date_was_changed = True
    #  #  elif action == 's': os.system('python3 ' + SS_PATH + ' -i')
    #  #  elif action == 'h': helps.help(screen_name)

    #  #  elif action == 'u':
        #  #  user_id = set_user(cur)
        #  #  con.commit()
        #  #  user_was_changed = True

    #  #  elif action == 'l':
        #  #  screen_name = 'food_db'
        #  #  while True:
            #  #  ui.clear()
            #  #  res = get_food_data(cur)

            #  #  # Disable tab-completion
            #  #  readline.parse_and_bind('tab: \t')

            #  #  ui.screen(
                #  #  libsd.HEADERS[screen_name],
                #  #  lambda: ui.print_as_table( [('title','kcal','p', 'f', 'c',)] + res,  ' ') if res else print(libsd.EMPTY_BODY[screen_name]),
                #  #  libsd.MENUS_ENTRIES[screen_name], 2)

            #  #  action = input('>> ').lower().strip()

            #  #  if action == 'q': break
            #  #  elif action == 'h': helps.help(screen_name)
            #  #  elif action in 'ar': helps.help('not_impl', 1)

            #  #  elif action not in 'arqh' and len(action) > 3:

                #  #  new_food_params = {'kcal': 'калорийность', 'p': 'содержание белков',
                   #  #  'f': 'содержание жиров','c': 'содержание углеводов'}
                #  #  d = get_data(new_food_params, 1)
                #  #  d['title'] = action
                #  #  add_new_food(cur, d)
                #  #  con.commit()
                #  #  db_was_changed = True

            #  #  elif action == 'a':
                #  #  screen_name = 'analyzer'
                #  #  while True:
                    #  #  dishes_list = get_dishes_list(cur)
                    #  #  # АНАЛИЗАТОР РЕЦЕПТА
                    #  #  ui.screen(
                        #  #  libsd.HEADERS[screen_name],
                        #  #  lambda: print(*dishes_list) if dishes_list else print(libsd.EMPTY_BODY[screen_name]),
                        #  #  libsd.MENUS_ENTRIES[screen_name], 3)

                    #  #  action = input('>> ').lower().strip()

                    #  #  if action == 'q': break
                    #  #  elif action == 'c':
        #  #  #  введите список продуктов с указанием количества, помогает табуляция
        #  #  #  проверка, все ли продукты известны
        #  #  #  подсчет данныэ
        #  #  #  введите название блюда
        #  #  #  сохранение в бд dishes
                        #  #  print('Not implemented yet')
                        #  #  sleep(1)
    
                    #  #  elif action == 'r':
                        #  #  print('Not implemented yet')
                        #  #  sleep(1)

                    #  #  elif action == 'h':
                        #  #  print(libsd.MENU_HELPS[screen_name])
                        #  a = input()
    
                    #  else:
                        #  print('Unsupported action')
                        #  sleep(1)


           
            #  else: helps.help('ua', 1)

    #  elif action not in 'lpnqht' and len(action) > 2:
        #  new_entry = { 'date': current_date, 'user': user_id, }

        #  for el in [ i.strip() for i in action.split(',') ]:

            #  data = libsd.parse_line(el)

            #  new_entry['title'] = data[0]
            #  new_entry['value'] = data[1] if data[1] is not None else input(f"количество для '{new_entry['title'][:1].upper() + new_entry['title'][1:]}': ")

            #  if is_in_db(cur, new_entry['title']) is None:
                #  print(f'Похоже, что такого блюда как \'{new_entry["title"]}\' нет в базе\nТребуется ввод дополнительной инофрмации')

                #  # Добавляем новый продукт в БД
                #  d = get_data({'kcal': 'калорийность',
                          #  'p': 'содержание белков',
                          #  'f': 'содержание жиров',
                          #  'c': 'содержание углеводов'}, 1)

                #  d['title'] = new_entry['title']
                #  add_new_food(cur, d)
                #  con.commit()
                #  db_was_changed = True

            #  # Добавляем запись в дневник
            #  add_in_diary(cur, new_entry)
            #  con.commit()

    #  else: helps.help('ua', 1)

