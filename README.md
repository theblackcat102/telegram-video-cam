# telegram-video-cam

A quick and easy way to create your personal movement detection recorder and sent it to your telegram bot

# Setup

## Setup environment

You will need python packages in requirements.txt with a machine with camera. ie: raspberry pi with camera

To test if your video is working you can execute test_vid.py 


## Obtain telegram api key

You need to create a telegram bot, please follow the instruction [here](https://core.telegram.org/bots) to create your own bot


## Obtain your chat id


After creating chat bot, you need to chat with your chat bot by sending a few messages.

Create a .env with the following fields

```
TELEGRAM_API_KEY="TELEGRAM API KEY"
```

Execute get_tg_user_id.py to find your chat id

## Fill .env fields

After obtaining your telegram API key from telegram, you need to create .env with the following fields

```
ROTATE_ANGLE=0
COUNT_DOWN_FRAME=100
USER_ID="YOUR CHAT ID"
TELEGRAM_API_KEY="TELEGRAM API KEY"
VIDEO_WIDTH="480"
TRIGGER_AREA="200"
```


## Run

execute main.py and see your results