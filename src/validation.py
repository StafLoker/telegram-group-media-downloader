import os
from datetime import datetime

def validate_group_name():
    """
    Prompt the user for a group name and validate that it's not empty.
    """
    while True:
        group_name = input("Enter the group name: ").strip()
        if group_name:
            return group_name
        print("- Error: Group name cannot be empty.")


def validate_date(prompt):
    """
    Prompt the user for a date and validate the format is 'dd-mm-yyyy'.
    """
    while True:
        date_input = input(prompt).strip()
        try:
            date_obj = datetime.strptime(date_input, '%d-%m-%Y')
            return date_input, date_obj
        except ValueError:
            print("- Error: Invalid date format. Please use 'dd-mm-yyyy'.")


def validate_save_path():
    """
    Prompt the user for a directory path and validate it exists.
    """
    while True:
        save_path = input("Enter the directory path where files should be saved: ").strip()
        if os.path.isdir(save_path):
            return save_path
        print("- Error: Invalid path. Please ensure the directory exists.")