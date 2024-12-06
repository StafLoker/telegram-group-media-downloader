# Telegram Group Media Downloader

This Python script downloads media files (images) from a specific Telegram group or channel for a specified date range and organizes the files into directories by date.

## Features

- Downloads media files from a Telegram group or channel.
- Organizes files into folders by date.
- User input for group name, date range, and save location.
- Creates a structured directory for downloaded files.
- Allows configuration via config files.
- 2 download modes

## Download Modes

- **General download**: Downloads all media from the group.

Result:
```
└── download-group-family-group-05-12-2024-s-01-07-2024-e-30-11-2024/
    └── 07-2024
        └── 02-07-2024/
            └── image1.jpg
            └── image2.png
        └── 03-07-2024/
            └── image3.jpg
```
- **Grouped download**: Groups media files into themes (categories) based on content type (`theme = [photo, photo, ...[description]`), allowing better organization.

Result:
```
└── download-group-family-group-05-12-2024-s-01-07-2024-e-30-11-2024/
    └── 07-2024
        └── 02-07-2024/
            └── theme1
                └── image1.jpg
                └── image2.png
            └── theme2
                └── image3.jpg
                └── image4.png
        └── 03-07-2024/
            └── theme3
                └── image5.jpg
```

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
## Logs
# [dev, prod]
LOGGER_CONFIG = 'prod'

## API
API_ID = number
API_HASH = 'text'
```

## Run

```bash
python src/main.py
```

# References

- [GitHub: telegram-download-media](https://github.com/marcelohcortez/telegram-download-media)