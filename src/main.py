"""
Main Module for Telegram Group Media Downloader.

This module serves as the entry point for the program, allowing users to either
load a configuration file or manually input parameters for downloading media
from a specified Telegram group within a date range.

Modules:
    - asyncio: Manages asynchronous operations for downloading media.
    - dotenv: Loader of environment variables
    - logger_config: Sets up logging configuration for tracking application activity.
    - user_input: Handles user input for configuration or manual parameters.
    - downloader: Manages the actual downloading of media from the Telegram group.

Functions:
    - main(): The main program loop that prompts the user for input and initiates the download process.
"""

import asyncio
from dotenv import load_dotenv
from logger_config import setup_logging
from user_input import get_input_from_config, get_manual_input
from downloader import download_media_from_group

# Configure logging
logging = setup_logging()

# Load environment variables
load_dotenv()


async def main():
    """
    Main function to initiate the Telegram Group Media Downloader.

    Prompts the user to choose between loading configuration from a file or
    entering parameters manually. Based on the input, it gathers necessary
    parameters and triggers the media download process.

    Workflow:
        1. Displays menu options for the user.
        2. Handles user input and validates the choice.
        3. Collects parameters via `load_config_input` or `manual_input`.
        4. Calls `download_all_media` to perform the download.

    Raises:
        ValueError: If the user inputs an invalid option number.
    """
    while True:
        print("Choose an option:")
        print("1. Load configuration from file")
        print("2. Enter parameters manually")

        try:
            choice = int(input("Enter the option number: ").strip())
            if choice == 1:
                group_name, start_date_obj, end_date_obj, save_path = get_input_from_config()
                break
            elif choice == 2:
                group_name, start_date_obj, end_date_obj, save_path = get_manual_input()
                break
            else:
                print("- Error: Invalid option.")
        except ValueError:
            print("- Error: Please enter a valid number.")

    await download_media_from_group(group_name, start_date_obj, end_date_obj, save_path)

if __name__ == "__main__":
    logging.info("Running Telegram Group Media Downloader")
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logging.critical("Program interrupted by user (Ctrl+C). Exiting.")
        print("\nProgram interrupted by user (Ctrl+C). Exiting.")
