import json, datetime, os, subprocess

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
    print('/help - Show this message.')
    print('/exit - Exit the program.')

def Autopilot(args):
    if args == 'on':
        subprocess.run(["powershell.exe", "-Command", "Start-Process python -ArgumentList autopilot.pyw -WindowStyle Hidden"], shell=True)
        print('Autopilot enabled.')
    elif args == 'off':
        with open('process', 'r') as file:
            pid = int(file.read())
            subprocess.run(["powershell.exe", "-Command", f"taskkill /F /PID {pid}"], shell=True)
            print('Autopilot disabled.')
    elif args == 'status':
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

def Points(args):
    if len(args) < 1:
        print("Invalid command. Use '/points <add/rem/list> <number>' (number not required for list).")
        return

    command = args[0]

    if command == 'add':
        if len(args) < 2:
            print("Invalid command. Use '/points add <number>'.")
            return
        try:
            number = int(args[1])
        except ValueError:
            print("Invalid number. Please provide a valid integer.")
            return

        with open(points_file, 'r+', encoding='utf-16') as file:
            content = file.read()
            file.seek(0, 0)
            new_line = f'/ {current_date} - {datetime.datetime.now().strftime("%I:%M %p")}\n'
            file.write(new_line * number + content)
        print(f'Now: {Count()}/{expected_points}')

    elif command == 'rem':
        if len(args) < 2:
            print("Invalid command. Use '/points rem <number>'.")
            return
        try:
            number = int(args[1])
        except ValueError:
            print("Invalid number. Please provide a valid integer.")
            return

        with open(points_file, 'r+', encoding='utf-16') as file:
            lines = file.readlines()
            file.seek(0)
            remaining_lines = []
            removed_lines = 0
            for line in lines:
                if line.startswith('/ ') and removed_lines < number:
                    removed_lines += 1
                else:
                    remaining_lines.append(line)
            file.writelines(remaining_lines)
            file.truncate()
        print(f'Now: {Count()}/{expected_points}')

    elif command == 'list':
        count = 0
        with open(points_file, 'r', encoding='utf-16') as file:
            lines = file.readlines()
            for line in lines:
                date_time_str = line.strip()
                if date_time_str.startswith('/ ') and current_date in date_time_str:
                    count += 1
            remaining_count = count
        print(f'Points added today: {remaining_count}')

    else:
        print("Invalid command. Use '/points <add/rem/list> <number>' (number not required for list).")

settings = load_settings()
expected_points = settings['threshold']
points_file = settings['points_file']
current_date = datetime.datetime.now().strftime("%m/%d/%y")

clear_screen()
print('Valid commands: /points, /hosts, /settings, /autopilot, /help and /exit.')

while True:
    command = input('PC> ')
    if command == '/help':
        print(Help())
    elif command.startswith('/points'):
        parts = command.split(' ')
        if len(parts) >= 2: Points(parts[1:])
        else: print(f'Points: {Count()}/{expected_points}')
    elif command == '/hosts':
        exec(open('hosts.py').read())
    elif command == '/settings':
        exec(open('settings.py').read())
    elif command.startswith('/autopilot'):
        parts = command.split(' ')
        Autopilot(parts[1])
    elif command == '/exit':
        break
    else:
        print("Invalid command. Use '/help' to see a list of valid commands.")
