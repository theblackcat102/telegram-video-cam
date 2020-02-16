import requests
from settings import telegram_api_key

if __name__ == "__main__":
    if ":" in telegram_api_key:
        res = requests.post('https://api.telegram.org/bot{}/getUpdates'.format(telegram_api_key))
        payload =  res.json()
        for r in payload['result']:
            if 'message' in r:
                print(r['message']['from']['id'])
