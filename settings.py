import json
import os

SETTINGS_PATH = "settings.json"

def load_settings():
    if os.path.exists(SETTINGS_PATH):
        with open(SETTINGS_PATH, "r") as f:
            return json.load(f)
    else:
        return {}

def save_settings(settings):
    with open(SETTINGS_PATH, "w") as f:
        json.dump(settings, f, indent=4)

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def main():
    settings = load_settings()
    clear_screen()

    while True:
        action = input("SETTINGS: ")

        if action == "/exit":
            break

        elif action == "/list":
            print("Current Settings:")
            for key, value in settings.items(): print(f"{key}: {value}")

        elif action.startswith("/set"):
            parts = action.split()
            if len(parts) == 3:
                key, value = parts[1], parts[2]
                settings[key] = value
                save_settings(settings)
                print(f"Setting '{key}' set to '{value}'.")
            else:
                print("Invalid format. Use '/set <key> <value>'.")

        elif action.startswith("/add"):
            parts = action.split()
            if len(parts) == 3:
                key, value = parts[1], parts[2]
                if key in settings:
                    print(f"Setting '{key}' already exists.")
                else:
                    settings[key] = value
                    save_settings(settings)
                    print(f"Setting '{key}' added.")
            else:
                print("Invalid format. Use '/add <key> <value>'.")

        elif action.startswith("/points"):
            parts = action.split()
            if len(parts) == 2:
                value = parts[1]
                settings['threshold'] = int(value)
                save_settings(settings)
                print(f"Points set to {value}.")
            else:
                print("Invalid format. Use '/points <value>'.")      

        elif action.startswith("/rem"):
            parts = action.split()
            if len(parts) == 2:
                key = parts[1]
                if key in settings:
                    del settings[key]
                    save_settings(settings)
                    print(f"Setting '{key}' removed.")
                else:
                    print(f"Setting '{key}' not found.")
            else:
                print("Invalid format. Use '/remove <key>'.")

        else:
            print("Invalid command. Please enter /points, /set, /rem, /list, or /exit.")

if __name__ == "__main__":
    main()
