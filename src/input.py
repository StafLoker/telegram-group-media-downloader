"""
Input Handling Module.

This module provides functions to gather and validate user input, either manually or
through configuration files. It ensures data integrity for group names, date ranges,
and file paths.

Modules:
    - os: Validates file and directory paths.
    - datetime: Manages date input and validation.
    - load_files: Loads configurations from external JSON files.

Functions:
    - manual_input: Collects user input interactively.
    - load_config_input: Retrieves parameters from a predefined configuration file.
    - choose_download_type: Allows the user to choose a download mode.
"""

import os
from datetime import datetime
from load_files import read_json_config


def __show_input_summary(group_name, start_date, end_date, save_path):
    """
    Display the current inputs for user confirmation.

    Args:
        group_name (str): Name of the Telegram group.
        start_date (str): Start date in 'dd-mm-yyyy' format.
        end_date (str): End date in 'dd-mm-yyyy' format.
        save_path (str): Directory path where files will be saved.
    """
    print("\nPlease confirm the following details:")
    print(f"1. Group Name: {group_name}")
    print(f"2. Start Date: {start_date}")
    print(f"3. End Date: {end_date}")
    print(f"4. Save Path: {save_path}")


def __get_valid_group_name():
    """
    Prompt the user for a group name and validate that it's not empty.
    """
    while True:
        group_name = input("Enter the group name: ").strip()
        if group_name:
            return group_name
        print("- Error: Group name cannot be empty.")


def __get_valid_date(prompt):
    """
    Prompt the user for a date and validate its format ('dd-mm-yyyy').

    Args:
        prompt (str): The message to display when requesting input.

    Returns:
        datetime: Parsed date object.
    """
    while True:
        date_input = input(prompt).strip()
        try:
            return datetime.strptime(date_input, '%d-%m-%Y')
        except ValueError:
            print("- Error: Invalid date format. Please use 'dd-mm-yyyy'.")


def __get_valid__save_directory():
    """
    Prompt the user for a directory path and validate it exists.

    Returns:
        str: Validated directory path.
    """
    while True:
        save_path = input(
            "Enter the directory path where files should be saved: ").strip()
        if os.path.isdir(save_path):
            return save_path
        print("- Error: Invalid path. Please ensure the directory exists.")


def __modify_user_input(choice, group_name, start_date_obj, end_date_obj, save_path):
    """
    Allow the user to update a specific parameter based on their choice.

    Args:
        choice (int): Parameter choice (1: Group Name, 2: Start Date, 3: End Date, 4: Save Path).
        group_name (str): Current group name.
        start_date_obj (datetime): Current start date.
        end_date_obj (datetime): Current end date.
        save_path (str): Current save path.

    Returns:
        tuple: Updated values (group_name, start_date_obj, end_date_obj, save_path).
    """
    match choice:
        case 1:
            group_name = __get_valid_group_name()
        case 2:
            start_date_obj = __get_valid_date(
                "Enter the start date (dd-mm-yyyy): ")
        case 3:
            end_date_obj = __get_valid_date(
                "Enter the end date (dd-mm-yyyy): ")
            while end_date_obj < start_date_obj:
                print("- Error: End date must be after or equal to the start date.")
                end_date_obj = __get_valid_date(
                    "Enter the end date (dd-mm-yyyy): ")
        case 4:
            save_path = __get_valid__save_directory()

    return group_name, start_date_obj, end_date_obj, save_path


def __confirm_or_update_input(group_name, start_date_obj, end_date_obj, save_path):
    """
    Validate user-provided information and allow corrections if necessary.

    Args:
        group_name (str): Current group name.
        start_date_obj (datetime): Current start date.
        end_date_obj (datetime): Current end date.
        save_path (str): Current save path.

    Returns:
        tuple: Confirmed and possibly updated values.
    """
    while True:
        __show_input_summary(group_name, start_date_obj.strftime(
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
                    group_name, start_date_obj, end_date_obj, save_path = __modify_user_input(
                        choice, group_name, start_date_obj, end_date_obj, save_path)
                else:
                    print("- Error: Invalid choice. Please select a valid option.")
            except ValueError:
                print("- Error: Please enter a number between 1 and 4.")
        else:
            print("- Error: Please enter 'y' or 'n'.")


def select_download_mode():
    """
    Prompt the user to choose the download type.

    Returns:
        int: Option selected by the user (1: General, 2: Group by theme).
    """
    print("\nChoose download type an option:")
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
            print("- Error: Please enter a valid number.")
    return choice


def get_manual_input():
    """
    Collect all required input manually from the user.

    Returns:
        tuple: Parameters (group_name, start_date_obj, end_date_obj, save_path).
    """
    group_name = __get_valid_group_name()
    start_date_obj = __get_valid_date(
        "Enter the start date (dd-mm-yyyy): ")
    end_date_obj = __get_valid_date("Enter the end date (dd-mm-yyyy): ")

    while end_date_obj < start_date_obj:
        print("- Error: End date must be after or equal to the start date.")
        end_date_obj = __get_valid_date(
            "Enter the end date (dd-mm-yyyy): ")

    save_path = __get_valid__save_directory()

    group_name, start_date_obj, end_date_obj, save_path = __confirm_or_update_input(
        group_name, start_date_obj, end_date_obj, save_path)

    return group_name, start_date_obj, end_date_obj, save_path


def get_input_from_config():
    """
    Retrieve input parameters from a configuration file.

    Returns:
        tuple: Parameters (group_name, start_date_obj, end_date_obj, save_path).
    """
    id_obj = 1
    configs = read_json_config("data/configs.json", "configs")

    if configs is None:
        print("- Error: No configurations available.")
        return None

    print("\nChoose a configuration:")
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
    group_name = config.get("groupName") or __get_valid_group_name()
    start_date_obj = datetime.strptime(config.get("startDate"), '%d-%m-%Y') if config.get(
        "startDate") is not None else __get_valid_date("Enter the start date (dd-mm-yyyy): ")
    end_date_obj = datetime.strptime(config.get("endDate"), '%d-%m-%Y') if config.get(
        "endDate") is not None else __get_valid_date("Enter the end date (dd-mm-yyyy): ")

    while end_date_obj < start_date_obj:
        print("- Error: End date must be after or equal to the start date.")
        end_date_obj = __get_valid_date(
            "Enter the end date (dd-mm-yyyy): ")

    save_path = config.get("savePath") or __get_valid__save_directory()

    group_name, start_date_obj, end_date_obj, save_path = __confirm_or_update_input(
        group_name, start_date_obj, end_date_obj, save_path)

    return group_name, start_date_obj, end_date_obj, save_path
