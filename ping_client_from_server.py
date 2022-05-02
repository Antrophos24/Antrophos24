#!/bin/python3.7
from pyzabbix.api import ZabbixAPI
import paramiko
import socket
import time
import re
import sys

'''скрипт проверяет доступность, заходит по ssh на BRAS и пингует с него оборудование клиента. Внедрил в систему мониторинга Zabbix, чтобы можно было с панели одной кнопкой проверять доступность.
Пример вывода при успешном подключении и пинге: 0.00% packet loss min = 11.8ms, avg = 17.8ms, max = 24.4ms'''

#ip-address, логин и пароль изменены на случайные
brasip = '17.147.13.17'
brasuser = 'admin'
braspass = 'pass'

#проверяет доступность BRAS
def ssh_invoke(cmd, hostname, username, password):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        client.connect(hostname=hostname, username=username, password=password, timeout=5)
    except socket.timeout:
        print(f'Host: {hostname} is unreachable, timed out')
        return False
    except paramiko.AuthenticationException:
        print(f'Invalid credentials for {username}:{password}')
        return False
    except paramiko.ssh_exception.NoValidConnectionsError:
        print(f'Connection refused by {hostname}')
        return False
    else:
        channel = client.invoke_shell(width=100, height=1000)
        time.sleep(3)
        channel.send('\n'+cmd+'\n')
        time.sleep(15)
        channel_data = str()
        out = channel.recv(99999)
        out = out.decode("ascii")
        channel.close()
        return out

#отправляет команду cmd, из полученного вывода регулярным выражением переменные packets и times забирают нужные строки
def main():
    c_ip = sys.argv[1]
    cmd = (f'ping {c_ip} router 70240 size 1400 count 8 timeout 1')
    try:
        big_output = ssh_invoke(cmd, brasip, brasuser, braspass)
        packets = re.findall('received, (.*)\r', big_output)[0]
        times = re.findall('round-trip (.*), stddev', big_output)[0]
        print(packets)
        print(times)
    except:
        print("Устройство недоступно")

if __name__ == "__main__":
    main()
