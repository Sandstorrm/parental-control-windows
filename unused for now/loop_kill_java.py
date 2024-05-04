import paramiko
import time

ip = '192.168.0.37'
user = 'sand'
passwd = 'sandstorm'


def ssh_command(ip, user, passwd):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(ip, username=user, password=passwd)
    
    while True:
        _, stdout, _ = client.exec_command('taskkill /f /im javaw.exe')
        output = stdout.readlines()
        print('\n'.join(output))
        time.sleep(5)

ssh_command(ip, user, passwd)
