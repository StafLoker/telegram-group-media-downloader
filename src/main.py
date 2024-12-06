"""
Main Module for Telegram Group Media Downloader.

This module serves as the entry point for the program, allowing users to either
load a configuration file or manually input parameters for downloading media
from a specified Telegram group within a date range.

Modules:
    - logging: Configures logging to capture events and errors.
    - asyncio: Manages asynchronous tasks.
    - input: Handles user input, either via configuration files or manual entry.
    - download: Provides the functionality to download media files.

Functions:
    - main(): The main program loop that prompts the user for input and initiates the download process.
"""

import logging
import asyncio
from input import load_config_input, manual_input
from download import download_all_media

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,  # Log level: DEBUG, INFO, WARNING, ERROR, CRITICAL
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("telegram_download.log")
    ]
)


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
                group_name, start_date_obj, end_date_obj, save_path = load_config_input()
                break
            elif choice == 2:
                group_name, start_date_obj, end_date_obj, save_path = manual_input()
                break
            else:
                print("- Error: Invalid option.")
        except ValueError:
            print("- Error: Please enter a valid number.")

    await download_all_media(group_name, start_date_obj, end_date_obj, save_path)

if __name__ == "__main__":
    logging.info("Running Telegram Group Media Downloader")
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logging.critical("Program interrupted by user (Ctrl+C). Exiting.")
        print("\nProgram interrupted by user (Ctrl+C). Exiting.")
