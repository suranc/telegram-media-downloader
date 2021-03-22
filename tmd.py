#!/usr/local/bin/python3

from telethon.sync import TelegramClient, events
from tqdm import  tqdm
import os
import sys
import argparse
 
parser = argparse.ArgumentParser(description='Telegram Media Downloader.  Allows for downloads of all media from a given channel.')
parser.add_argument('channel',
                    help='Name of the Telegram channel to be downloaded, the channel-name part from t.co/channel-name')
parser.add_argument('--start', dest='start', metavar='Video.mp4',
                    help='Filename to start on')
parser.add_argument('--end', dest='end', metavar='Video.mp4',
                    help='Filename to end on')
parser.add_argument('--api_id', dest='api_id', metavar='8675309',
                    help='App ID for your Telegram client, one can be obtained from https://my.telegram.org, under API Development.  Overrides the TELEGRAM_API_ID environment variable')
parser.add_argument('--api_hash', dest='api_hash', metavar='f20b326c0172cdfce9108394fa8ab9f7',
                    help='App Hash for your Telegram client, one can be obtained from https://my.telegram.org, under API Development.  Overrides the TELEGRAM_API_HASH environment variable')

args = parser.parse_args()

channel = args.channel
start_filename = None
end_filename = None
started = True


if (args.start != None):
    start_filename = args.start
    started = False
    print("Starting at " + start_filename)

if (args.end != None):
    end_filename = args.end
    print("Ending at " + end_filename)

# Need an api_id and api_hash, and a download.session file in the working directory (a new one will be created through MFA if one does)
# The api_id and api_hash can be gotten from https://my.telegram.org, under API Development.
api_id = args.api_id or os.getenv('TELEGRAM_API_ID')
api_hash = args.api_hash or os.getenv('TELEGRAM_API_HASH')
if ((not api_id) or (not api_hash)):
    print ("Error:  api_id and api_hash must be passed with --api_id and --api_hash, or in the environment variables TELEGRAM_API_ID and TELEGRAM_API_HASH")
    sys.exit(1)

# Create a telegram client with the given api_id and api_hash
# Will reuse an existing download.session in working directory, otherwise will begin an interactive mfa flow
client = TelegramClient('download', api_id, api_hash)

async def main(started):
    me = await client.get_me()
    
    # Loop through each message in channel
    async for message in client.iter_messages(channel):
        # Only act on messages with media
        if (hasattr(message, 'media')):
            if (message.media):
                # If there's a start filename, wait for that and set started=True when found
                if (not started):
                    if (hasattr(message.media, 'document')):
                        for attribute in message.media.document.attributes:
                            if (hasattr(attribute, 'file_name') and (attribute.file_name == start_filename)):
                                print("Reached start file "+start_filename)
                                started = True
                                break
                        if (not started):
                            continue
                    else:
                        print ("Haven't found " + start_filename + " yet id=" + str(message.id))
                        continue

                # If end filename is set, check for it and quit if we're at it
                if ((end_filename != None) and (attribute.file_name == end_filename)):
                    print("Reached end file "+end_filename)
                    sys.exit(0)
                else:
                    path = await message.download_media()
                    print('File saved to', path)  # printed after download is done

with client:
    client.loop.run_until_complete(main(started))