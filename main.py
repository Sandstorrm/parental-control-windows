import json, datetime, os, subprocess, time

def load_settings():
    if os.path.exists('settings.json'):
        with open('settings.json', 'r') as f:
            return json.load(f)
    else:
        return {}

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def Count():
    count = 0
    points_file = 'points.txt'
    if not os.path.exists(points_file):
        with open(points_file, 'w'):
            print('Points file created.')

    today = datetime.date.today()
    yesterday = today - datetime.timedelta(days=1)
    current_date = today.strftime('%m/%d/%y')
    yesterday_date = yesterday.strftime('%m/%d/%y')

    with open(points_file, 'r', encoding='utf-16') as file:
        for line in file:
            date_time_str = line.strip()
            if current_date in date_time_str:
                count += 1

            if  yesterday_date in date_time_str:
                date_part, time_part = date_time_str.split(' - ')
                hour, minute_part = time_part.split(':')
                minute, period = minute_part.split()
                if period == 'PM' and int(hour) >= 10:
                    count += 1
    return count

def Help():
    print('Valid commmands:')
    print('/points - Show current points.')
    print('/hosts - Add or remove websites from the hosts file.')
    print('/settings - Change settings.')
    print('/autopilot - Enable, disable or check the status of autopilot.')
    print('/update - Update the program.')
    print('/help - Show this message.')
    print('/exit - Exit the program.')

def Autopilot(command):
    if command == 'on':
        subprocess.run(["powershell.exe", "-Command", "Start-Process python -ArgumentList autopilot.pyw -WindowStyle Hidden"], shell=True)
        print('Autopilot enabled.')
    elif command == 'off':
        with open('process', 'r') as file:
            pid = int(file.read())
            subprocess.run(["powershell.exe", "-Command", f"taskkill /F /PID {pid}"], shell=True)
            print('Autopilot disabled.')
    elif command == 'status':
        try:
            with open('process', 'r') as file:
                pid = int(file.read())
            result = subprocess.run(["tasklist", "/FI", f"PID eq {pid}"], capture_output=True, text=True)
            if "python" in result.stdout:
                print(f"Autopilot is running with PID {pid}")
            else:
                print("Autopilot is not running")
        except FileNotFoundError:
            print("Autopilot is not running")
    else:
        print("Invalid command. Use '/autopilot on/off'.")

settings = load_settings()
expected_points = settings['threshold']
points_file = settings['points_file']
current_date = datetime.datetime.now().strftime("%m/%d/%y")

clear_screen()
print('Valid commands: /points, /hosts, /settings, /autopilot, /update, /help and /exit.')

while True:
    command = input('PC> ')
    if command == '/help':
        print(Help())
    elif command == '/points':
        print(f'Points: {Count()}/{expected_points}')
    elif command == '/hosts':
        exec(open('hosts.py').read())
    elif command == '/settings':
        exec(open('settings.py').read())
    elif command.startswith('/autopilot'):
        parts = command.split(' ')
        Autopilot(parts[1])
    elif command == '/update':
        print("Updating...")
        subprocess.run(["powershell.exe", "-Command", "python update"], shell=True)
    elif command == '/exit':
        break
    else:
        print("Invalid command. Please enter /points, /hosts, /settings, /autopilot, /update, /help and /exit.")