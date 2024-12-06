"""
Module to handle file operations for loading configurations.

This module provides functionality to load and parse JSON files, enabling
retrieval of specific elements based on user-defined keys.

Modules:
    - json: Parses JSON data.
    - os: Validates file paths.
"""

import json
import os
from logger_config import setup_logging

# Configure logging
logging = setup_logging()

def read_json_config(path, root_element):
    """
    Load a specific element from a JSON configuration file.

    This function reads a JSON file from the provided path, parses its content,
    and retrieves the value corresponding to the specified root element.

    Args:
        path (str): The file path to the JSON configuration file.
        root_element (str): The top-level key whose value is to be retrieved.

    Returns:
        list or None: The value associated with `root_element` in the JSON file
                      if it exists, or `None` if the file does not exist or the
                      key is not found.

    Logs:
        - Error: If the file is not found at the specified path.
    """
    if not os.path.exists(path):
        print(f"- Error: Configuration file not found at {path}")
        logging.error("- Error: Configuration file not found at %s", path)
        return None
    
    with open(path, 'r', encoding="utf-8") as file:
        data = json.load(file)
    return data.get(root_element, [])