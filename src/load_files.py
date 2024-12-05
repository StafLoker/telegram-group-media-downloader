"""
Module providing a function to load files.
"""

import json
import os
import logging

def load_json_file(path, root_element):
    """
    Load configurations from the JSON file.
    """
    if not os.path.exists(path):
        print(f"- Error: Configuration file not found at {path}")
        logging.error("- Error: Configuration file not found at %s", path)
        return None
    
    with open(path, 'r', encoding="utf-8") as file:
        data = json.load(file)
    return data.get(root_element, [])