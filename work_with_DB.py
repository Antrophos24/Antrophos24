#!/bin/python3.7
import re
import sys
import psycopg2
'''заказчик потребовал изменить все 4000 названий узлов в системе мониторинга Zabbix и предоставил актуальный список названий
с учетом что все они начинаются на номера, удалось составить два списка, где каждая строка с названием из старого списка соответствовала строке с новым названием данного узла'''

#открываем на чтение txt файлы со старыми и новыми названиями
f = open("old.txt", "r")
n = open("new.txt", "r")

num = 1

for l in f:
		#чтобы корректно работало во втором файле добавил первую пустую строку, так как код меняет 1 строку old на 2 строку new и тд.
        a = l
        b = next(n)
		#подключаемся к PostgreSQL БД и циклом меняем строки из одного списка на строку другого
        command2 = "update public.hosts set name = replace(hosts.name, %s, %s);"
        conn = psycopg2.connect(dbname='zabbix', user='admin', password='mypass', host='10.200.10.23')
        cursor = conn.cursor()
        got = (a,b)
        #добавил print, чтобы наглядно видеть какая строка на какую меняется, вводимую команду и какой номер по счету (для наглядности чтобы увидеть ошибку и остановить код, а потом быстро продолжить не сначала, а с нужного момента)
		print(a)
        print(b)
        cursor.execute(command2, got)
        conn.commit()
        print(command2)
        cursor.close()
        conn.close()
        print(num)
        num = num + 1
