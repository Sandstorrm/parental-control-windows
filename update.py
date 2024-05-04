import requests

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

url = ""
filename = ""

update_file_from_url(url, filename)