import logging
import json
import os
from datetime import datetime, timedelta
from validation import *
from download import download_all_media

# Path to the config file
CONFIG_FILE_PATH = 'data/configs.json'

def load_configs():
    """Load configurations from the JSON file."""
    if not os.path.exists(CONFIG_FILE_PATH):
        print(f"- Error: Configuration file not found at {CONFIG_FILE_PATH}")
        logging.error(f"- Error: Configuration file not found at {CONFIG_FILE_PATH}");
        return []
    
    with open(CONFIG_FILE_PATH, 'r') as file:
        data = json.load(file)
    return data.get("configs", [])

def display_results(group_name, start_date, end_date, save_path):
    """Display the current inputs for user confirmation."""
    print("\nPlease confirm the following details:")
    print(f"1. Group Name: {group_name}")
    print(f"2. Start Date: {start_date}")
    print(f"3. End Date: {end_date}")
    print(f"4. Save Path: {save_path}")

def update_parameters(choice, group_name, start_date, end_date, save_path):
    """Allow the user to update a specific parameter based on their choice."""
    if choice == 1:
        group_name = validate_group_name()
    elif choice == 2:
        start_date, start_date_obj = validate_date("Enter the start date (dd-mm-yyyy): ")
    elif choice == 3:
        while True:
            end_date, end_date_obj = validate_date("Enter the end date (dd-mm-yyyy): ")
            if datetime.strptime(end_date, '%d-%m-%Y') >= datetime.strptime(start_date, '%d-%m-%Y'):
                break
            print("- Error: End date must be after or equal to the start date.")
    elif choice == 4:
        save_path = validate_save_path()
    return group_name, start_date, start_date_obj, end_date, end_date_obj, save_path

async def manual_input():
    """Prompt the user for input manually."""
    group_name = validate_group_name()
    start_date, start_date_obj = validate_date("Enter the start date (dd-mm-yyyy): ")
    end_date, end_date_obj = validate_date("Enter the end date (dd-mm-yyyy): ")

    while end_date_obj < start_date_obj:
        print("- Error: End date must be after or equal to the start date.")
        end_date, end_date_obj = validate_date("Enter the end date (dd-mm-yyyy): ")

    save_path = validate_save_path()

    while True:
        display_results(group_name, start_date, end_date, save_path)

        confirm = input("Is the information correct? (y/n): ").strip().lower()
        if confirm == 'y':
            break
        elif confirm == 'n':
            print("\nWhich parameter would you like to change?")
            print("1. Group Name")
            print("2. Start Date")
            print("3. End Date")
            print("4. Save Path")
            try:
                choice = int(input("Enter the number of the parameter to change: ").strip())
                if choice in {1, 2, 3, 4}:
                    group_name, start_date, start_date_obj, end_date, end_date_obj, save_path = update_parameters(
                        choice, group_name, start_date, end_date, save_path)
                else:
                    print("- Error: Invalid choice. Please select a valid option.")
            except ValueError:
                print("- Error: Please enter a number between 1 and 4.")
        else:
            print("- Error: Please enter 'y' or 'n'.")

    ## await download_all_media(group_name, start_date_obj, end_date_obj, save_path)

async def load_config_input():
    """Prompt the user to choose a config from the file."""
    configs = load_configs()

    if not configs:
        print("- Error: No configurations available.")
        return

    print("Choose a configuration:")
    for config in configs:
        print(f"{config['id']}. {config['description']}")

    try:
        config_id = int(input("Enter the config ID: ").strip())
        selected_config = next((cfg for cfg in configs if cfg['id'] == config_id), None)

        if selected_config is None:
            print("- Error: Invalid config ID.")
            return

        print(f"\nYou selected: {selected_config['description']}")
        config = selected_config['config']

        # Extract config parameters or ask the user if missing
        group_name = config.get("groupName") or validate_group_name()
        start_date = config.get("startDate") or input("Enter the start date (dd-mm-yyyy): ").strip()
        start_date_obj = datetime.strptime(start_date, '%d-%m-%Y')
        end_date = config.get("endDate") or input("Enter the end date (dd-mm-yyyy): ").strip()
        end_date_obj = datetime.strptime(end_date, '%d-%m-%Y')

        while end_date_obj < start_date_obj:
            print("- Error: End date must be after or equal to the start date.")
            end_date = input("Enter the end date (dd-mm-yyyy): ").strip()
            end_date_obj = datetime.strptime(end_date, '%d-%m-%Y')

        save_path = config.get("savePath") or validate_save_path()

        display_results(group_name, start_date, end_date, save_path)
        confirm = input("Is the information correct? (y/n): ").strip().lower()
        if confirm == 'y':
            pass
            ## await download_all_media(group_name, start_date_obj, end_date_obj, save_path)
        else:
            print("- Error: Please confirm the information before proceeding.")

    except ValueError:
        print("- Error: Invalid input.")