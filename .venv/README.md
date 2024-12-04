# Virtual Environment Management

## Prerequisites

On Linux:
`sudo apt install python3-venv`

## Create Virtual Environment

`python3 -m venv telegram-download-media-group-env`

## Activate the Virtual Environment
- Assuming you are already in the project root
`source .venv/telegram-download-media-group-env/bin/activate`

## Save and Load Dependencies with `requirements.txt`

### Save
`pip freeze > requirements.txt`

### Load
`pip install -r requirements.txt`

## Deactivate the Virtual Environment

`deactivate`

## Delete a Virtual Environment

`rm -rf telegram-download-media-group-env`


# Libraries

- `pip install python-telegram-bot`