# Telegram Media Downloader

A simple utiliy that will download all of the media files in a given Telegram channel.

## Usage

`./tmd.py [-h] [--start Video.mp4] [--end Video.mp4] [--app_id 8675309] [--app_hash f20b326c0172cdfce9108394fa8ab9f7] channel`

The `app_id` and `app_hash` can also be set in environment variables, with `TELEGRAM_APP_ID` and `TELEGRAM_APP_HASH` respectively.  To use this you'll need to create a telegram application, following the instructions here: https://docs.telethon.dev/en/latest/basic/signing-in.html

## Setup

To run locally, install the required Python modules with `pip install -r requirements.txt`

Alternatively, you can run the latest build from a docker container like `docker run -it -v $PWD:/save -w /save -u 1000 -e TELEGRAM_APP_ID=8675309 -e TELEGRAM_APP_HASH=f20b326c0172cdfce9108394fa8ab9f7 ghcr.io/suranc/tmd Telegram-Channel --start start-video.mp4`
