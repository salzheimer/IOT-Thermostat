def load_config(filename="config.txt"):
    """Reads a config file and returns a dictionary of settings."""
    config = {}
    try:
        with open(filename, 'r') as file:
            for line in file:
                line = line.strip()
                if line and not line.startswith('#'):  # Ignore empty lines and comments
                    try:
                        key, value = line.split('=', 1)
                        config[key.strip()] = value.strip()
                    except ValueError:
                        print(f"Warning: Skipping invalid line in config file: {line}")
    except OSError as e:
        print(f"Error reading config file: {e}")
        # Optionally handle default values here if the file is missing
        config['ssid'] = 'DefaultSSID'
        config['password'] = 'DefaultPW'
        
    return config


def main()->None:
    config = load_config()
    print("Loaded configuration:")
    for key, value in config.items():
        print(f"{key}: {value}")    

if __name__ == "__main__":
    main()