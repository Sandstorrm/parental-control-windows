import requests
import subprocess

def update_file_from_url(url, filename):
  subprocess.run(["taskkill", "/F", "/IM", "pythonw3.12.exe"])

  try:
    response = requests.get(url, stream=True)
    response.raise_for_status()

    with open(filename, "wb") as f:
      for chunk in response.iter_content(1024):
        f.write(chunk)

    print(f"File downloaded successfully: {filename}")
  except requests.exceptions.RequestException as e:
    print(f"Error downloading file: {e}")

  subprocess.run(["pythonw3.12.exe main.pyw"])
  

url = "https://raw.githubusercontent.com/Sandstorrm/parental-control/main/main.pyw"
filename = "main.pyw"

update_file_from_url(url, filename)
