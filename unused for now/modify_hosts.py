import os

# Define the path to the hosts file
hosts_path = r"C:\\Windows\\System32\\drivers\\etc\\hosts"

# Define a function to add a website to the hosts file
def add_website(website):
    with open(hosts_path, 'a') as file:
        file.write(f"10.0.0.1 {website}\\n")  # Add a newline character at the end
    print(f"{website} has been added to the hosts file.")

# Define a function to remove a website from the hosts file
def remove_website(website):
    with open(hosts_path, 'r') as file:
        lines = file.readlines()

    with open(hosts_path, 'w') as file:
        for line in lines:
            if not line.startswith(f"10.0.0.1 {website}"):
                file.write(line)

    print(f"{website} has been removed from the hosts file.")

# Define a function to list all blocked websites
def list_blocked_websites():
    with open(hosts_path, 'r') as file:
        lines = file.readlines()

    blocked_websites = [line.split()[1] for line in lines if line.startswith("10.0.0.1")]

    print("Blocked websites:")
    for website in blocked_websites:
        print(website)

# Ask the user whether they want to add or remove a website
action = input("HOSTS: ")

if action.startswith("/add"):
    website = action.split()[1]  # Get the website from the input string
    add_website(website)
elif action.startswith("/rem"):
    website = action.split()[1]  # Get the website from the input string
    remove_website(website)
elif action == "/list":
    list_blocked_websites()
else:
    print("Invalid action. Please enter '/add {website}', '/rem {website}', or '/list'.")
