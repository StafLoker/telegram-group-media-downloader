import os
import asyncio
from telethon.sync import TelegramClient
from telethon.tl.types import DocumentAttributeVideo
from dotenv import load_dotenv
from pathlib import Path

# Load environment variables
load_dotenv()

# Set up Telegram API credentials
api_id = os.getenv('API_ID')
api_hash = os.getenv('API_HASH')
client = TelegramClient('group_media_downloader', api_id, api_hash)


# Function to download media
async def download_media(message, save_path):
    try:
        if message.media is not None:
            # Check for image, video, or GIF
            if hasattr(message.media, 'photo') or (
                    hasattr(message.media, 'document') and isinstance(message.media.document.attributes[0], DocumentAttributeVideo)
            ) or (
                    hasattr(message.media, 'document') and message.media.document.mime_type.split("/")[0] == 'image'
                    and message.media.document.mime_type.split("/")[1] == 'gif'
            ):
                file = await client.download_media(message.media, file=save_path)
                return 1
    except Exception as e:
        print(f"Error downloading media: {e}")
    return 0


# Main function to download all media files
async def download_all_media(group_name, start_date, end_date, base_path):
    try:
        await client.start()

        # Get group entity
        entity = await client.get_entity(group_name)

        # Create base directory
        today = datetime.now().strftime('%d-%m-%Y')
        folder_name = f"download-group-{group_name}-{today}-s-{start_date}-f-{end_date}"
        base_dir = os.path.join(base_path, folder_name)
        os.makedirs(base_dir, exist_ok=True)

        start_date_obj = datetime.strptime(start_date, '%d-%m-%Y')
        end_date_obj = datetime.strptime(end_date, '%d-%m-%Y')

        total_downloaded = 0

        # Loop over dates
        current_date = start_date_obj
        while current_date <= end_date_obj:
            date_str = current_date.strftime('%d-%m-%Y')
            day_folder = os.path.join(base_dir, date_str)
            os.makedirs(day_folder, exist_ok=True)

            # Iterate over messages for the specific date
            async for message in client.iter_messages(entity, offset_date=current_date + timedelta(days=1), reverse=True):
                if message.date.date() == current_date.date():
                    total_downloaded += await download_media(message, save_path=day_folder)

            current_date += timedelta(days=1)

        print(f"Total images downloaded: {total_downloaded}")

    except Exception as e:
        print(f"Error: {e}")

    finally:
        await client.disconnect()