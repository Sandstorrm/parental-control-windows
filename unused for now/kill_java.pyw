import paramiko

def ssh_command(ip, user, passwd, command):
    client = paramiko.SSHClient()
    # Automatically add untrusted hosts
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(ip, username=user, password=passwd)
    _, stdout, _ = client.exec_command(command)
    output = stdout.readlines()
    print('\n'.join(output))

# Replace with your details
ip = '192.168.0.37'
user = 'sand'
passwd = 'sandstorm'
command = 'taskkill /f /im javaw.exe'

ssh_command(ip, user, passwd, command)
