# Telegram Group Media Downloader

This Python script downloads media files (images) from a specific Telegram group or channel for a specified date range and organizes the files into directories by date.

## Features

- Downloads media files from a Telegram group or channel.
- Organizes files into folders by date.
- User input for group name, date range, and save location.
- Creates a structured directory for downloaded files.
- Permit to use configs

## Requirements

### Install the following Python packages:

- `telethon`
- `dotenv`

So you can create a virtual environment if you wish (a .venv) or install globally (not advised)

Install them with pip:

```bash
pip install telethon python-dotenv
```

### Obtaining api_id & api_hash 

- [Telegram docs](https://core.telegram.org/api/obtaining_api_id)

Created api_id & api_hash save to `.env` like:
```
API_ID = number
API_HASH = 'text'
```

## Run

```bash
python src/main.py
```

# References

- [GitHub: telegram-download-media](https://github.com/marcelohcortez/telegram-download-media)