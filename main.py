#!/usr/bin/env python3

import sqlite3, readline, signal, sys, re, datetime
from ui import *
from libjtt import *

PROG_NAME = 'job-time-tracker'
VERSION = '0.1.0'
DB_NAME = sys.path[0] + '/data.db'

(db_was_changed, period_was_changed) = (False, False)

con = sqlite3.connect(DB_NAME)
cur = con.cursor()

create_tables(cur)
#  con.commit()
while True:
    current_period = (cur.execute('SELECT selected_period FROM config').fetchone())
    print(current_period)
    #  exit(0)

    if current_period is None:
        current_period = datetime.date.today().strftime("%Y-%m")
        cur.execute('UPDATE config SET selected_period = ?', (current_period, ))
        #  con.commit()

    
    for l in cur.execute("SELECT * FROM period_data WHERE date LIKE ?", (current_period + '-%', )).fetchall():
        print(l)

    action = input('>> ').lower().strip()

    if action == 'q': break
    elif action == 'a':
        print('Пока необходимо вводить данные в формате ГГГГ-ММ-ДД Д.Ч Н.Ч')
        line = input().split(' ')
        cur.execute('insert into period_data values(?, ?, ?)', line)
    elif action == 'p':
        prev_period = datetime.date.fromisoformat(current_period + '-01') - datetime.timedelta(days=31)
        #  current_period = prev_period.strftime("%Y-%m")
        cur.execute('UPDATE config SET selected_period = ?', (prev_period.strftime("%Y-%m"), ))

        #  current_date_was_changed = True
    #  elif action == 'n': 
        #  current_date += datetime.timedelta(days = 31)
        #  current_period = current_date.strftime("%Y-%m")
        #  cur.execute('UPDATE config SET selected_period = ?', (current_period, ))
        #  con.commit()
    con.commit()
con.close()




#  #  # Enable SIG handlers and configure readline
#  #  readline.set_completer_delims('\n,')

#  #  # Get user data and diary from db
#  #  user_data = get_user_data_by_id(cur, user_id)


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

