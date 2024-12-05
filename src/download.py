"""
Module providing a function of download content from telegram with `telethon`
"""

import os
import logging
from datetime import datetime, timedelta
from telethon.sync import TelegramClient
from dotenv import load_dotenv
from input import choose_download_type

# Load environment variables
load_dotenv()

# Set up Telegram API credentials
api_id = os.getenv('API_ID')
api_hash = os.getenv('API_HASH')
client = TelegramClient('group_media_downloader', api_id, api_hash)


async def download_media(message, save_path):
    """
    Download media in message
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


async def download_media_general(entity, current_date, next_date, day_folder):
    """
    Iterate over messages for the specific date
    General download
    """
    day_count = 0

    async for message in client.iter_messages(entity, offset_date=current_date, reverse=True):
        if message.date.replace(tzinfo=None) < next_date:
            day_count += await download_media(message, save_path=day_folder)
        else:
            break

    return day_count


async def download_media_specific_group_theme(entity, current_date, date_str, next_date, day_folder):
    """
    Iterate over messages for the specific date
    Specific download - group by theme
    """
    day_count = 0

    logging.debug("Create new empty group")
    photo_group = []
    description_message = None

    async for message in client.iter_messages(entity, offset_date=current_date, reverse=True):
        if message.date.replace(tzinfo=None) < next_date:
            if message.media and hasattr(message.media, 'photo'):
                photo_group.append(message)
                logging.debug("--- Add photo to group: %d", message.id)
            elif message.text and not message.media:
                description_message = message
                logging.debug(
                    "--- Found description message of group: %d", message.id)

            if description_message and photo_group:
                logging.debug("Created group: %s", description_message)
                group_folder_name = f"{date_str} {description_message.text}"
                group_folder_path = os.path.join(day_folder, group_folder_name)
                os.makedirs(group_folder_path, exist_ok=True)
                logging.debug("--- Group dir. %s created in %s: %s",
                              group_folder_name, day_folder, group_folder_path)
                
                logging.debug("--- Download photos of group: %s", description_message)
                for photo_message in photo_group:
                    day_count += await download_media(photo_message, save_path=group_folder_path)
                logging.debug("--- End of group: %s", description_message)
                
                logging.debug("Create new empty group")
                photo_group = []
                description_message = None
        else:
            break

    return day_count


async def download_all_media(group_name, start_date_obj, end_date_obj, base_path):
    """
    Download all media in group name in period [start_date, end_date]
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


        choose = choose_download_type()
        total_downloaded = 0
        current_date = start_date_obj

        # Loop period
        while current_date <= end_date_obj:
            date_str = current_date.strftime('%d-%m-%Y')
            day_folder = os.path.join(base_dir, date_str)
            os.makedirs(day_folder, exist_ok=True)
            logging.debug("Day dir. %s created in %s: %s",
                          date_str, base_dir, day_folder)

            logging.info("Downloading media for day: %s", date_str)

            match choose:
                case 1:
                    day_count = await download_media_general(entity, current_date, (current_date + timedelta(days=1)), day_folder)
                case 2:
                    day_count = await download_media_specific_group_theme(entity, current_date, date_str, (current_date + timedelta(days=1)), day_folder)

            logging.info("--- Downloaded %d files for %s.",
                         day_count, date_str)
            if day_count == 0:
                logging.info("No files downloaded for %s. Removing folder %s.", date_str, day_folder)
                os.rmdir(day_folder)
            else:
                total_downloaded += day_count

            current_date += timedelta(days=1)

        print(f"Total media files downloaded: {total_downloaded}")
        logging.info("Total media files downloaded: %d", total_downloaded)

    except Exception as e:
        print(f"Error: {e}")
        logging.error("Error: %s", e)

    finally:
        await client.disconnect()
