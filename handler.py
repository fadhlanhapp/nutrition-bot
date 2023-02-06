import json
import os
import sys
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), "./vendored"))

import requests

TOKEN = os.environ['TELEGRAM_TOKEN']
BASE_URL = "https://api.telegram.org/bot{}".format(TOKEN)


def hello(event, context):
    try:
        data = json.loads(event["body"])
        message = str(data["message"]["text"]).split(" ")
        chat_id = data["message"]["chat"]["id"]
        first_name = data["message"]["chat"]["first_name"]

        command = message[0]
        response = "no command found!"

        if command == "/start":
            response = ' '.join(message[1:])
        elif command == "/check":
            URL = "https://trackapi.nutritionix.com/v2/natural/nutrients"
            search = ' '.join(message[1:])
            DATA = {'query':search}
            app_id = os.environ['APP_ID_NUTRITIONIX']
            app_keys = os.environ['APP_KEYS_NUTRITIONIX']
            HEADER = {'x-app-id':app_id, 'x-app-key': app_keys}

            r = requests.post(url = URL, data = DATA, headers = HEADER)

            result = r.json()
            response = "masuk"
            # result['foods'][0]['nf_calories']

        data = {"text": response.encode("utf8"), "chat_id": chat_id}
        url = BASE_URL + "/sendMessage"
        requests.post(url, data)

    except Exception as e:
        print(e)

    return {"statusCode": 200}