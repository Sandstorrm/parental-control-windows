import subprocess
import time
import ctypes

def run_command(command):
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()
    return stdout, stderr

def lockout():
    command = input("Lockout: ")
    delay = None
    error_content = None
    error_title = None

    if command == "mc":
        delay = input("Enter delay (in seconds): ")
        error_content = input("Enter error content: ")
        if error_content:
            error_title = input("Enter error title: ")
            ctypes.windll.user32.MessageBoxW(None, error_content, error_title, 0)

    if delay:
        delay = int(delay)
        start_time = time.time()
        while time.time() - start_time < delay:
            stdout, stderr = run_command("taskkill /f /im javaw.exe")
            print(stdout.decode())
            time.sleep(5)
    else:
        stdout, stderr = run_command("taskkill /f /im javaw.exe")
        print(stdout.decode())

lockout()