import datetime
import subprocess
import time
import json
import os

pid = os.getpid()
print("pid: " + str(pid))
with open('process', 'w') as file:
    file.write(str(pid))

startupinfo = subprocess.STARTUPINFO()
startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW

def Count(points_file):
    count = 0
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

while True:
    current_date = datetime.datetime.now().strftime("%m/%d/%y")
    with open('settings.json', 'r') as f: settings = json.load(f)
    threshold = settings['threshold']
    success_delay = settings['success_delay']
    failed_delay = settings['failed_delay']
    failed_command = settings['failed_command']
    points_file = settings['points_file']
    count = int(Count(points_file))

    if count >= threshold:
        print(f"Done with: {count}")
        time.sleep(success_delay)
    else:
        print(f"Only {count}, Expected: {threshold}")
        result = subprocess.Popen(["powershell", "-Command", failed_command], stdout=subprocess.PIPE, startupinfo=startupinfo)
        output = result.communicate()[0].decode()
        print(output)
        time.sleep(failed_delay)