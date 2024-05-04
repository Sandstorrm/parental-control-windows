import requests
import subprocess
import sys, os

def update_file_from_url(url, filename):

  try:
    response = requests.get(url, stream=True)
    response.raise_for_status()

    with open(filename, "wb") as f:
      for chunk in response.iter_content(1024):
        f.write(chunk)

    print(f"File downloaded successfully: {filename}")
  except requests.exceptions.RequestException as e:
    print(f"Error downloading file: {e}")

def run_pyw_script(script_path):
    pythonw_executable = os.path.join(sys.prefix, "pythonw3.12.exe")
    subprocess.Popen([pythonw_executable, script_path])
  
main_url = "https://raw.githubusercontent.com/Sandstorrm/parental-control/main/main.pyw"
filename = "main.pyw"

settings_url = "https://raw.githubusercontent.com/Sandstorrm/parental-control/main/settings.json"
settings_filename = "settings.json"

subprocess.run(["taskkill", "/F", "/IM", "pythonw3.12.exe"])

update_file_from_url(main_url, filename)
update_file_from_url(settings_url, settings_filename)

run_pyw_script(os.path.abspath(filename))