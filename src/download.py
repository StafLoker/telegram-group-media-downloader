import os
import logging
from datetime import datetime, timedelta
from telethon.sync import TelegramClient
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Set up Telegram API credentials
api_id = os.getenv('API_ID')
api_hash = os.getenv('API_HASH')
client = TelegramClient('group_media_downloader', api_id, api_hash)

async def download_media(message, save_path):
    logging.debug(f"Trying download message: {message.id}, Save path: {save_path}")
    try:
        if message.media is not None and hasattr(message.media, 'photo'):
            await client.download_media(message.media, file=save_path)
            logging.debug(f"Downloaded message (photo): {message.id}, Save path: {save_path}")
            return 1
    except Exception as e:
        logging.error(f"Error downloading media from message ID {message.id}: {e}")
    return 0


async def download_all_media(group_name, start_date_obj, end_date_obj, base_path):
    try:
        await client.start()

        # Get group entity
        entity = await client.get_entity(group_name)
        logging.info(f"Entity to download {entity.id}, {entity.title}")

        # Create base directory
        name_dir = f"download-group-{group_name}-{datetime.now().strftime('%d-%m-%Y')}-s-{start_date_obj.strftime('%d-%m-%Y')}-e-{end_date_obj.strftime('%d-%m-%Y')}"
        base_dir = os.path.join(base_path, name_dir)
        os.makedirs(base_dir, exist_ok=True)
        logging.debug(f"Dir. {name_dir} created in {base_path}: {base_dir}")

        total_downloaded = 0

        # Loop over dates
        current_date = start_date_obj
        next_date = current_date + timedelta(days=1)
        while current_date <= end_date_obj:
            date_str = current_date.strftime('%d-%m-%Y')
            day_folder = os.path.join(base_dir, date_str)
            os.makedirs(day_folder, exist_ok=True)
            logging.debug(f"Dir. {date_str} created in {base_dir}: {day_folder}")

            logging.info(f"Downloading media for {date_str}")
            day_count = 0

            # Iterate over messages for the specific date
            async for message in client.iter_messages(entity, offset_date=current_date, reverse=True):
                if message.date.replace(tzinfo=None) < next_date:
                    day_count += await download_media(message, save_path=day_folder)
                else:
                    break

            logging.info(f"--- Downloaded {day_count} files for {date_str}.")
            total_downloaded += day_count
            current_date += timedelta(days=1)
            next_date += timedelta(days=1)

        print(f"Total media files downloaded: {total_downloaded}")
        logging.info(f"Total media files downloaded: {total_downloaded}")

    except Exception as e:
        print(f"Error: {e}")
        logging.error(f"Error: {e}")

    finally:
        await client.disconnect()
        