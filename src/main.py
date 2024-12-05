"""
Main
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
            print("- Error: Please enter a valid number.\n")

    await download_all_media(group_name, start_date_obj, end_date_obj, save_path)

if __name__ == "__main__":
    asyncio.run(main())