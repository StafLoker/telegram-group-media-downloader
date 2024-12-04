from datetime import datetime, timedelta
from validation import *
from download import *

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
    

# Main program
async def main():
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

    await download_all_media(group_name, start_date_obj, end_date_obj, save_path)


if __name__ == "__main__":
    asyncio.run(main())