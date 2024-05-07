import os
import subprocess

HOSTS_PATH = r"C:\Windows\System32\drivers\etc\hosts"

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def flush_dns():
    try:
        result = subprocess.run(["ipconfig", "/flushdns"], capture_output=True, text=True, check=True)
        if "success" in result.stdout.lower():
            print("DNS cache flushed.")
    except subprocess.CalledProcessError as e:
        print(f"Error flushing DNS cache: {e}")

def add_website(website):
    with open(HOSTS_PATH, 'a') as file:
        file.write(f"10.0.0.1 {website}\n")
    print(f"{website} has been added to the hosts file.")
    flush_dns()

def remove_website(website):
    lines = []
    website_found = False
    with open(HOSTS_PATH, 'r') as file:
        lines = file.readlines()

    with open(HOSTS_PATH, 'w') as file:
        for line in lines:
            if line.startswith(f"10.0.0.1 {website}" or line.startswith("192.178.50.78")):
                website_found = True
            else:
                file.write(line)

    if website_found:
        print(f"{website} has been removed from the hosts file.")
        flush_dns()
    else:
        print(f"{website} was not found in the hosts file.")

def list_blocked_websites():
    blocked_websites = []
    with open(HOSTS_PATH, 'r') as file:
        lines = file.readlines()
        blocked_websites = [line.split()[1] for line in lines if line.startswith("10.0.0.1") or line.startswith("192.178.50.78")]

    print("Blocked websites:")
    for website in blocked_websites:
        print(website)

def main():
    print('Valid commands: /list, /add, /rem, /help and /exit.')
    while True:
        action = input("HOSTS> ")

        if action == "/exit":
            break
        elif action == "/list":
            list_blocked_websites()
        elif action == "/help":
            print('Valid commands:')
            print('/list - List blocked websites.')
            print('/add - Add a website to the hosts file.')
            print('/rem - Remove a website from the hosts file.')
            print('/help - Show this message.')
            print('/exit - Exit the program.')
        elif action.startswith("/add"):
            parts = action.split()
            if len(parts) > 1:
                website = parts[1]
                add_website(website)
            else:
                print("Please provide a website to add.")
        elif action.startswith("/rem"):
            parts = action.split()
            if len(parts) > 1:
                website = parts[1]
                remove_website(website)
            else:
                print("Please provide a website to remove.")
        else:
            print("Invalid command. Please enter /add {website}, /rem {website}, /list, or /exit.")

if __name__ == "__main__":
    clear_screen()
    main()
