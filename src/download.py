"""
Module for downloading media content from Telegram groups using `telethon`.

This module provides functions to download media files (such as photos) 
from Telegram groups within a specified date range. Media can be grouped 
by themes or downloaded generally. It supports progress tracking, 
directory creation, and filtering messages based on specified restrictions.
"""

import os
import re
import logging
from datetime import datetime, timedelta
from telethon.sync import TelegramClient
from dotenv import load_dotenv
from input import select_download_mode
from load_files import read_json_config

# Load environment variables
load_dotenv()

# Set up Telegram API credentials
api_id = os.getenv('API_ID')
api_hash = os.getenv('API_HASH')
client = TelegramClient('group_media_downloader', api_id, api_hash)


def __clean_folder_name(folder_name):
    """
    Replace invalid characters in folder names with underscores.

    Args:
        folder_name (str): The original folder name.

    Returns:
        str: The sanitized folder name.
    """
    sanitized_name = re.sub(r'[<>:"/\\|?*]', '_', folder_name)
    return sanitized_name.strip()


def __is_valid_description(message, restrictions):
    """
    Determine if a message qualifies as a description based on restrictions.

    Args:
        message (telethon.tl.custom.Message): The Telegram message object.
        restrictions (list): A list of conditions to identify description messages.

    Returns:
        bool: True if the message qualifies as a description, False otherwise.
    """
    # Have text
    if not message.message:
        return False
    
    # Have prohibit text
    for prohibit in restrictions[0].get('notDescriptionMessage', []):
        if prohibit in message.message:
            return False
    return True

async def __save_media(message, save_path):
    """
    Download media content from a Telegram message.

    Args:
        message (telethon.tl.custom.Message): The Telegram message containing media.
        save_path (str): Directory to save the downloaded media.

    Returns:
        int: 1 if the media was downloaded successfully, 0 otherwise.
    """
    logging.debug("Trying download message: %d, Save path: %s",
                  message.id, save_path)
    try:
        if message.media is not None and hasattr(message.media, 'photo'):
            await client.download_media(message.media, file=save_path)
            logging.debug(
                "--- Downloaded message %d, Save path: %s", message.id, save_path)
            return 1
    except Exception as e:
        logging.error(
            "Error downloading media from message ID %d: %s", message.id, e)
    return 0


async def __process_general_download(entity, current_date, next_date, day_folder):
    """
    Download all media from a Telegram group for a specific date.

    Args:
        entity: The Telegram entity (group or channel) to download from.
        current_date (datetime): The start date of the download range.
        next_date (datetime): The end date (exclusive) of the download range.
        day_folder (str): Directory to save the downloaded media for the day.

    Returns:
        int: Total number of media files downloaded for the day.
    """
    day_count = 0

    async for message in client.iter_messages(entity, offset_date=current_date, reverse=True):
        if message.date.replace(tzinfo=None) < next_date:
            logging.debug("Message: id: %s, date: %s, message: %s, media: %s", message.id, message.date, message.message, message.media)
            day_count += await __save_media(message, save_path=day_folder)
        else:
            break

    return day_count

async def __process_theme_grouped_download(entity, current_date, date_str, next_date, day_folder, restrictions):
    """
    Download media grouped by themes for a specific date.

    Args:
        entity: The Telegram entity (group or channel) to download from.
        current_date (datetime): The start date of the download range.
        date_str (str): The formatted date string for folder naming.
        next_date (datetime): The end date (exclusive) of the download range.
        day_folder (str): Directory to save the grouped media for the day.
        restrictions (list): Criteria for grouping and filtering messages.

    Returns:
        int: Total number of media files downloaded for the day.
    """
    day_count = 0

    logging.debug("Create new empty group")
    photo_group = []
    description_message : str = None

    async for message in client.iter_messages(entity, offset_date=current_date, reverse=True):
        # Process messages only current date
        if message.date.replace(tzinfo=None) < next_date:
            logging.debug("Message: id: %s, date: %s, message: %s, media: %s", message.id, message.date, message.message, message.media)
            # Filter messages
            if message.media and hasattr(message.media, 'photo'):
                if not message.message:
                    photo_group.append(message)
                    logging.debug("--- Add photo to group: %d", message.id)
                elif __is_valid_description(message, restrictions):
                    photo_group.append(message)
                    logging.debug("--- Add photo to group: %d", message.id)
                    description_message = message.message
                    logging.debug(
                            "--- Found description message of group: %d", message.id)
            elif __is_valid_description(message, restrictions) and photo_group:
                description_message = message.message
                logging.debug(
                    "--- Found description message of group: %d", message.id)

            if description_message is not None and photo_group:
                logging.debug("Created group: %s", description_message)
                group_folder_name = f"{date_str} {
                    __clean_folder_name(description_message)}"
                group_folder_path = os.path.join(day_folder, group_folder_name)
                os.makedirs(group_folder_path, exist_ok=True)
                logging.debug("--- Group dir. %s created in %s: %s",
                              group_folder_name, day_folder, group_folder_path)

                logging.debug("--- Download photos of group: %s",
                              description_message)
                for photo_message in photo_group:
                    day_count += await __save_media(photo_message, save_path=group_folder_path)
                logging.debug("--- End of group: %s", description_message)

                logging.debug("Create new empty group")
                photo_group = []
                description_message = None
        else:
            break

    return day_count


async def download_media_from_group(group_name, start_date_obj, end_date_obj, base_path):
    """
    Download all media from a Telegram group within a specified date range.

    Args:
        group_name (str): Name of the Telegram group or channel.
        start_date_obj (datetime): Start date for media download.
        end_date_obj (datetime): End date for media download.
        base_path (str): Directory where media files will be saved.

    Returns:
        None
    """
    try:
        await client.start()

        # Get group entity
        entity = await client.get_entity(group_name)
        logging.info("Entity to download %d, %s", entity.id, entity.title)

        # Create base directory
        name_dir = f"download-group-{group_name}-{datetime.now().strftime('%d-%m-%Y')}-s-{
            start_date_obj.strftime('%d-%m-%Y')}-e-{end_date_obj.strftime('%d-%m-%Y')}"
        base_dir = os.path.join(base_path, name_dir)
        os.makedirs(base_dir, exist_ok=True)
        logging.debug("Base dir. %s created in %s: %s",
                      name_dir, base_path, base_dir)

        # Choose type
        choose = select_download_mode()
        total_downloaded = 0
        current_date = start_date_obj

        # Load restrictions
        restrictions = read_json_config("data/restrictions.json", "restrictions")
        if restrictions is None:
            print("- Error: No restrictions available.")
            if choose == 2:
                return None

        # Progress bar init
        total_days = (end_date_obj - start_date_obj).days + 1
        completed_days = 0
        print("\nDownloading...", end=" ")

        # Loop period
        while current_date <= end_date_obj:
            month_str = current_date.strftime('%m-%Y')
            month_folder = os.path.join(base_dir, month_str)
            if not os.path.exists(month_folder):
                os.makedirs(month_folder)
                logging.debug("Month dir. %s created in %s: %s",
                              month_str, base_dir, month_folder)

            date_str = current_date.strftime('%d-%m-%Y')
            day_folder = os.path.join(month_folder, date_str)
            os.makedirs(day_folder, exist_ok=True)
            logging.debug("Day dir. %s created in %s: %s",
                          date_str, month_folder, day_folder)

            logging.info("Downloading media for day: %s", date_str)

            match choose:
                case 1:
                    day_count = await __process_general_download(entity, current_date, (current_date + timedelta(days=1)), day_folder)
                case 2:
                    day_count = await __process_theme_grouped_download(entity, current_date, date_str, (current_date + timedelta(days=1)), day_folder, restrictions)

            logging.info("--- Downloaded %d files for %s.",
                         day_count, date_str)
            if day_count == 0:
                logging.info(
                    "No files downloaded for %s. Removing folder %s.", date_str, day_folder)
                os.rmdir(day_folder)

            total_downloaded += day_count
            current_date += timedelta(days=1)

            # Progress bar print
            completed_days += 1
            progress_percentage = int((completed_days / total_days) * 100)
            bar = f"[{'#' * (progress_percentage // 2)}{'-' * (50 - (progress_percentage // 2))}] {progress_percentage}%"
            print(f"\r{"Downloading..." if progress_percentage < 100 else "Downloaded:"} {bar}", end='')

        print(f"\n\nTotal media files downloaded: {total_downloaded}")
        logging.info("Total media files downloaded: %d", total_downloaded)

    except Exception as e:
        print(f"Error: {e}")
        logging.error("Error: %s", e)

    finally:
        await client.disconnect()
