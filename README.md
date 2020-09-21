# TwitterBot
Bot to upload pics/comments to a twitter account. Pics and comments are taken from user-provided pools (.csv).

## Prerequisites
1. You'll need a Twitter dev account, and create a new application with write permissions with which your bot will interface. There should be multiple tutorials online. Ex) https://www.labnol.org/how-to-create-a-twitter-app-for-bots-4703
2. Install pandas (pip install pandas)
3. Install the Python Twitter API: https://github.com/bear/python-twitter

## Running the Bot
Look at the environment varialbes at the top of Bot.py.
You'll need to set these up according to the Twitter application credentials, which directory contains the pictures to post (.jpg format), and the locations of the post-tracking .csvs.

### Twitter Access Env Variables
See https://github.com/bear/python-twitter, particularly the API section about get_access_token.py.
   TWITTER_BOT_API_KEY: Twitter application API key
   TWITTER_BOT_API_SECRET_KEY: Twitter application API secret key
   TWITTER_BOT_ACCESS_TOKEN_KEY: Twitter application token key
   TWITTER_BOT_ACCESS_TOKEN_SECRET: Twitter application token secret

### File-System Env Variables
   TWITTER_BOT_PIC_DIR: Directory from which .jpg images will be collected for posting.
   TWITTER_BOT_PIC_DATA_PATH: File path for the .csv containing metadata about pics. It should have 'FileName', 'Count', and 'LastUsedDatetime' fields. See Bot.py for details.
   TWITTER_BOT_TEXT_FILE_PATH: File path for the .csv containing metadata about text. It should have 'Text', 'Count', and 'LastUsedDDatetime' fields. See Bot.py for details.

## Periodic Posts
Use a task scheduler (e.g. Windows's built-in Task Scheduler) to set up a recurring call to Bot.py.
