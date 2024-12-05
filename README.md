# Telegram Download Media Group

This Python script downloads media files (images, videos, and GIFs) from a specific Telegram group or channel for a specified date range and organizes the files into directories by date.

## Features

- Downloads media files from a Telegram group or channel.
- Organizes files into folders by date.
- User input for group name, date range, and save location.
- Creates a structured directory for downloaded files.

## Requirements

Install the following Python packages:

- `telethon`
- `asyncio`
- `dotenv`

So you can create a virtual environment if you wish (a .venv) or install globally (not advised)

Install them with pip:

```bash
pip install telethon python-dotenv
```
## Run

```bash
python src/main.py
```

# References

- [GitHub: telegram-download-media](https://github.com/marcelohcortez/telegram-download-media)