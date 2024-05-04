import requests
import subprocess

def update_file_from_url(url, filename):
  startupinfo = subprocess.STARTUPINFO()
  startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW

  try:
    process = subprocess.Popen(["python", __file__, url, filename], stdout=subprocess.PIPE, stderr=subprocess.PIPE, startupinfo=startupinfo)
    output, error = process.communicate()

    if error:
      print(f"Error downloading file: {error.decode()}")
    else:
      print(output)
      print(f"File downloaded successfully: {filename}")
  except requests.exceptions.RequestException as e:
    print(f"Error: {e}")

url = "https://raw.githubusercontent.com/Sandstorrm/parental-control/main/main.pyw"
filename = "main.pyw"

update_file_from_url(url, filename)
