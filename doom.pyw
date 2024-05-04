import datetime
import subprocess
import os
import time
import json

startupinfo = subprocess.STARTUPINFO()
startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
home_dir = os.path.expanduser("~")

def Count():
    count = 0
    with open(file_path, 'r', encoding='utf-16') as file:
        for line in file:
            if current_date in line:
                count += 1
    return count

while True:
    settings_path = os.path.join(home_dir,'settings.json')
    current_date = datetime.datetime.now().strftime("%m/%d/%y")
    with open(settings_path, 'r') as f: settings = json.load(f)
    threshold = settings['threshold']
    success_delay = settings['success_delay']
    failed_delay = settings['failed_delay']
    failed_command = settings['failed_command']
    relative_path = settings['relative_path']
    file_path = os.path.join(home_dir,relative_path)
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
