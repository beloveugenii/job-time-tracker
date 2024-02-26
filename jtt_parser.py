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
    if file.find('.jtt') == -1:
        print(f'"file" IS NOT A JTT FILE')
        continue
    # открываем переданный файл
    f = open(file, 'r')

    # переменные, для хранения данных из файлов
    config = dict()
    data_lines = list()

    # парсинг файла
    for line in f:
        line = line[:-1]

        # ищем параметры конфигурации
        sep = line.find('=')
        if sep != -1:
            (k, v) = (line[:sep], line[sep+1:])
            config[k] = v
        # остальные строки
        else:
            match = line.split(' ')
            d = match[0].split('.')
            date = '-'.join(['20' + d[2], d[1], d[0]])
            data_lines.append((date, match[2], match[3]))

    cur.execute("INSERT INTO config VALUES (:period, :salary, :first, :second, :relax, :bonus, :dprise, :tax)", config) 
    for line in data_lines:
        cur.execute("INSERT INTO data VALUES (?, ?, ?)", line)

    con.commit()

    print(cur.execute("SELECT * from config").fetchall())
    print(cur.execute('SELECT * FROM data').fetchall())


