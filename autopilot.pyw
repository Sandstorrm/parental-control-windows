import subprocess, shutil, time, json, os, sqlite3
from urllib.parse import urlparse
from main import Count
from hosts import add_website, remove_website

def insure_pid():
    pid = os.getpid()
    print("pid: " + str(pid))
    with open('process', 'w') as file:
        file.write(str(pid))

def load_settings():
    with open('settings.json', 'r') as f:
        return json.load(f)

def punish():
    failed_command = load_settings()['failed_command']
    startupinfo = subprocess.STARTUPINFO()
    startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
    result = subprocess.Popen(["powershell", "-Command", failed_command], stdout=subprocess.PIPE, startupinfo=startupinfo)
    output = result.communicate()[0].decode()
    print(output)

def manage_visited_websites(action):
    orig_db_path = 'C:\\Users\\sands\\AppData\\Local\\Google\\Chrome\\User Data\\Default\\History'
    script_dir = os.path.dirname(os.path.abspath(__file__))
    temp_db_path = os.path.join(script_dir, 'temp_history.db')
    shutil.copy2(orig_db_path, temp_db_path)

    try:
        con = sqlite3.connect(temp_db_path)
        cursor = con.cursor()
        cursor.execute("SELECT url FROM urls")
        urls = cursor.fetchall()
        con.close()

        website_domains = set()
        for url in urls:
            parsed_url = urlparse(url[0])
            website_domain = parsed_url.netloc.split(':')[0]
            website_domains.add(website_domain)

        sorted_website_domains = sorted(website_domains)

        if action == 'add':
            for domain in sorted_website_domains:
                add_website(domain)
        elif action == 'rem':
            for domain in sorted_website_domains:
                remove_website(domain)
        else:
            print("Invalid action. Please use 'add' or 'rem'.")
    finally:
        os.remove(temp_db_path)

def main():
    insure_pid()
    settings = load_settings()
    threshold = settings['threshold']
    success_delay = settings['success_delay']
    failed_delay = settings['failed_delay']
    points_file = settings['points_file']

    while True:
        count = Count(points_file)

        if count >= threshold:
            print(f"Done with: {count}")
            manage_visited_websites('rem')
            time.sleep(success_delay)
        else:
            print(f"Only {count}, Expected: {threshold}")
            punish()
            previous_websites = set()
            for _ in range(failed_delay // 5):
                time.sleep(5)
                website_domains = manage_visited_websites('check')
                new_websites = website_domains - previous_websites
                for domain in new_websites:
                    add_website(domain)
                previous_websites = website_domains

if __name__ == '__main__':
    main()
