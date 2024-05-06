import datetime
import subprocess
import time
import json
import os

pid = os.getpid()
print("pid: " + pid)
with open('process', 'w') as file:
    file.write(str(pid))

startupinfo = subprocess.STARTUPINFO()
startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW

def Count():
    count = 0
    if not os.path.exists(points_file):
        with open(points_file, 'w', encoding='utf-16'):
            print('Points file created.')

    with open(points_file, 'r', encoding='utf-16') as file:
        for line in file:
            if current_date in line:
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
    count = int(Count())

    if count >= threshold:
        print(f"Done with: {count}")
        time.sleep(success_delay)
    else:
        print(f"Only {count}, Expected: {threshold}")
        result = subprocess.Popen(["powershell", "-Command", failed_command], stdout=subprocess.PIPE, startupinfo=startupinfo)
        output = result.communicate()[0].decode()
        print(output)
        time.sleep(failed_delay)