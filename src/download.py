import os
import logging
from datetime import datetime, timedelta
from telethon.sync import TelegramClient
from telethon.tl.types import DocumentAttributeVideo
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Set up Telegram API credentials
api_id = os.getenv('API_ID')
api_hash = os.getenv('API_HASH')
client = TelegramClient('group_media_downloader', api_id, api_hash)

async def get_group_entity(group_name):
    """
    Get the Telegram group entity using the group's name or ID.
    If it fails to find the group directly, it will search through the user's dialogs.
    """
    try:
        # Try to get the group entity directly
        return await client.get_entity(group_name)
    except ValueError:
        logging.warning(f"Group '{group_name}' not found directly. Searching through dialogs.")
        async for dialog in client.iter_dialogs():
            if dialog.name == group_name:
                logging.info(f"Found group '{group_name}' in user dialogs.")
                return dialog.entity
        raise ValueError(f"Group '{group_name}' not found in dialogs.")

async def download_media(message, save_path):
    try:
        if message.media:
            if hasattr(message.media, 'photo'):  # Check for photos
                file = await client.download_media(message.media, file=save_path)
                return 1
            elif hasattr(message.media, 'document'):  # Check for documents
                mime_type = message.media.document.mime_type
                if mime_type.startswith('image/') or mime_type == 'video/mp4':  # Images or MP4 videos
                    file = await client.download_media(message.media, file=save_path)
                    return 1
    except Exception as e:
        print(f"Error downloading media from message ID {message.id}: {e}")
        logging.error(f"Error downloading media from message ID {message.id}: {e}")
    return 0


async def download_all_media(group_name, start_date_obj, end_date_obj, base_path):
    try:
        await client.start()

        # Get group entity
        entity = await get_group_entity(group_name)

        # Create base directory
        today = datetime.now().strftime('%d-%m-%Y')
        folder_name = f"download-group-{group_name}-{today}-s-{start_date_obj.strftime('%d-%m-%Y')}-e-{end_date_obj.strftime('%d-%m-%Y')}"
        base_dir = os.path.join(base_path, folder_name)
        os.makedirs(base_dir, exist_ok=True)

        total_downloaded = 0

        # Loop over dates
        current_date = start_date_obj
        while current_date <= end_date_obj:
            date_str = current_date.strftime('%d-%m-%Y')
            day_folder = os.path.join(base_dir, date_str)
            os.makedirs(day_folder, exist_ok=True)

            logging.debug(f"Downloading media for {date_str}...")
            day_count = 0

            # Iterate over messages for the specific date
            async for message in client.iter_messages(entity, offset_date=current_date + timedelta(days=1), reverse=True):
                if message.date.date() == current_date.date():
                    day_count += await download_media(message, save_path=day_folder)

            logging.debug(f"Downloaded {day_count} files for {date_str}.")
            total_downloaded += day_count
            current_date += timedelta(days=1)

        print(f"Total media files downloaded: {total_downloaded}")
        logging.info(f"Total media files downloaded: {total_downloaded}")

    except Exception as e:
        print(f"Error: {e}")
        logging.error(f"Error: {e}")

    finally:
        await client.disconnect()
        