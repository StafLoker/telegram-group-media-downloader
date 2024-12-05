# Virtual Environment Management

## Prerequisites

On Linux:
`sudo apt install python3-venv`

## Create Virtual Environment

`python3 -m venv .venv/telegram-group-media-downloader-env`

## Activate the Virtual Environment
`source .venv/telegram-group-media-downloader-env/bin/activate`

## Save and Load Dependencies with `requirements.txt`

### Save
`pip freeze > .venv/requirements.txt`

### Load
`pip install -r .venv/requirements.txt`

## Deactivate the Virtual Environment

`deactivate`

## Delete a Virtual Environment

`rm -rf .venv/telegram-group-media-downloader-env`