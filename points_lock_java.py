import datetime
import subprocess
import os
import time
 
startupinfo = subprocess.STARTUPINFO()
startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
home_dir = os.path.expanduser("~")
command = "taskkill /f /im javaw.exe"
file_path = os.path.join(home_dir,'doom.txt')
print(file_path)
threshold = 12
 
def Count():
    count = 0
    with open(file_path, 'r', encoding='utf-16') as file:
        for line in file:
            if current_date in line:
                count += 1
    return count
 
while True:
    current_date = datetime.datetime.now().strftime("%m/%d/%y")
    count = int(Count())
    if count >= threshold:
        print(f"Done with: {count}")
        time.sleep(10)
    else:
        print(f"Only {count}, Expected: {threshold}")
        result = subprocess.Popen(["powershell", "-Command", command], stdout=subprocess.PIPE, startupinfo=startupinfo)
        output = result.communicate()[0].decode()
        print(output)
        time.sleep(5)