import json
import os

def load_configs_file(path):
    """
    Load configurations from the JSON file.
    """
    if not os.path.exists(CONFIG_FILE_PATH):
        print(f"- Error: Configuration file not found at {CONFIG_FILE_PATH}")
        logging.error(f"- Error: Configuration file not found at {CONFIG_FILE_PATH}");
        return []
    
    with open(CONFIG_FILE_PATH, 'r') as file:
        data = json.load(file)
    return data.get("configs", [])