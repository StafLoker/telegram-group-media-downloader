import logging
import asyncio
from input import load_config_input, manual_input

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
                await load_config_input()
                break
            elif choice == 2:
                await manual_input()
                break
            else:
                print("- Error: Invalid option.")
        except ValueError:
            print("- Error: Please enter a valid number.\n")

if __name__ == "__main__":
    asyncio.run(main())