"""
Module providing a function of input
"""

import os
from datetime import datetime
from load_files import load_configs_file


def __display_results(group_name, start_date, end_date, save_path):
    """
    Display the current inputs for user confirmation.
    """
    print("\nPlease confirm the following details:")
    print(f"1. Group Name: {group_name}")
    print(f"2. Start Date: {start_date}")
    print(f"3. End Date: {end_date}")
    print(f"4. Save Path: {save_path}")


def __input_validate_group_name():
    """
    Prompt the user for a group name and validate that it's not empty.
    """
    while True:
        group_name = input("Enter the group name: ").strip()
        if group_name:
            return group_name
        print("- Error: Group name cannot be empty.")


def __input_validate_date(prompt):
    """
    Prompt the user for a date and validate the format is 'dd-mm-yyyy'.
    """
    while True:
        date_input = input(prompt).strip()
        try:
            return datetime.strptime(date_input, '%d-%m-%Y')
        except ValueError:
            print("- Error: Invalid date format. Please use 'dd-mm-yyyy'.")


def __input_validate_save_path():
    """
    Prompt the user for a directory path and validate it exists.
    """
    while True:
        save_path = input(
            "Enter the directory path where files should be saved: ").strip()
        if os.path.isdir(save_path):
            return save_path
        print("- Error: Invalid path. Please ensure the directory exists.")


def __update_parameters(choice, group_name, start_date_obj, end_date_obj, save_path):
    """
    Allow the user to update a specific parameter based on their choice.
    """
    match choice:
        case 1:
            group_name = __input_validate_group_name()
        case 2:
            start_date_obj = __input_validate_date(
                "Enter the start date (dd-mm-yyyy): ")
        case 3:
            end_date_obj = __input_validate_date(
                "Enter the end date (dd-mm-yyyy): ")
            while end_date_obj < start_date_obj:
                print("- Error: End date must be after or equal to the start date.")
                end_date_obj = __input_validate_date(
                    "Enter the end date (dd-mm-yyyy): ")
        case 4:
            save_path = __input_validate_save_path()

    return group_name, start_date_obj, end_date_obj, save_path


def __while_input(group_name, start_date_obj, end_date_obj, save_path):
    """
    Prompt the user for correct information
    """
    while True:
        __display_results(group_name, start_date_obj.strftime(
            '%d-%m-%Y'), end_date_obj.strftime('%d-%m-%Y'), save_path)

        confirm = input("Is the information correct? (y/n): ").strip().lower()
        if confirm == 'y':
            return group_name, start_date_obj, end_date_obj, save_path
        elif confirm == 'n':
            print("\nWhich parameter would you like to change?")
            print("1. Group Name")
            print("2. Start Date")
            print("3. End Date")
            print("4. Save Path")
            try:
                choice = int(
                    input("Enter the number of the parameter to change: ").strip())
                if choice in {1, 2, 3, 4}:
                    group_name, start_date_obj, end_date_obj, save_path = __update_parameters(
                        choice, group_name, start_date_obj, end_date_obj, save_path)
                else:
                    print("- Error: Invalid choice. Please select a valid option.")
            except ValueError:
                print("- Error: Please enter a number between 1 and 4.")
        else:
            print("- Error: Please enter 'y' or 'n'.")


def choose_download_type():
    """
    Prompt the user for input choose download type.
    """
    print("Choose download type an option:")
    print("1. General")
    print("2. Specific - group by theme")

    while True:
        try:
            choice = int(input("Enter the option number: ").strip())
            if 1 <= choice <= 2:
                break
            else:
                print("- Error: Invalid option.")
        except ValueError:
            print("- Error: Please enter a valid number.\n")
    return choice


def manual_input():
    """
    Prompt the user for input manually.
    """
    group_name = __input_validate_group_name()
    start_date_obj = __input_validate_date(
        "Enter the start date (dd-mm-yyyy): ")
    end_date_obj = __input_validate_date("Enter the end date (dd-mm-yyyy): ")

    while end_date_obj < start_date_obj:
        print("- Error: End date must be after or equal to the start date.")
        end_date_obj = __input_validate_date(
            "Enter the end date (dd-mm-yyyy): ")

    save_path = __input_validate_save_path()

    group_name, start_date_obj, end_date_obj, save_path = __while_input(
        group_name, start_date_obj, end_date_obj, save_path)

    return group_name, start_date_obj, end_date_obj, save_path


def load_config_input():
    """
    Prompt the user to choose a config from the file.
    """
    id_obj = 1
    configs = load_configs_file('data/configs.json')

    if configs is None:
        print("- Error: No configurations available.")
        return None

    print("Choose a configuration:")
    for config in configs:
        print(f"{id_obj}. {config['description']}")
        id_obj += 1

    while True:
        try:
            id_obj = int(input("Enter the config ID: ").strip())
            if 1 <= id_obj <= len(configs):
                break
        except ValueError:
            print("- Error: Invalid input.")
    
    selected_config = configs[id_obj-1]
    print(f"\nYou selected: {selected_config['description']}")
    config = selected_config['config']

    # Extract config parameters or ask the user if missing
    group_name = config.get("groupName") or __input_validate_group_name()
    start_date_obj = datetime.strptime(config.get("startDate"), '%d-%m-%Y') if config.get(
        "startDate") is not None else __input_validate_date("Enter the start date (dd-mm-yyyy): ")
    end_date_obj = datetime.strptime(config.get("endDate"), '%d-%m-%Y') if config.get(
        "endDate") is not None else __input_validate_date("Enter the end date (dd-mm-yyyy): ")

    while end_date_obj < start_date_obj:
        print("- Error: End date must be after or equal to the start date.")
        end_date_obj = __input_validate_date(
            "Enter the end date (dd-mm-yyyy): ")

    save_path = config.get("savePath") or __input_validate_save_path()

    group_name, start_date_obj, end_date_obj, save_path = __while_input(
         group_name, start_date_obj, end_date_obj, save_path)

    return group_name, start_date_obj, end_date_obj, save_path