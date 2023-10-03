'''Updated push message module to avoid using Line SDK
- create a payload
- send push
- handle response
'''
import json
import os

import requests


def send_push(group_id: str, message: str):
    print('[Line] Sending push')
    print(message)

    url = 'https://api.line.me/v2/bot/message/push'
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {os.environ["LINE_CHANNEL_ACCESS_TOKEN"]}'
    }
    messages = [{"type": "text", "text": message}]
    payload = {"to": group_id, "messages": messages}

    try:
        response = requests.post(url,
                                 headers=headers,
                                 data=json.dumps(payload))
        print('API Response:\n', response.json())
    except Exception as e:
        print("Exception when calling Line API: %s\n" % e)


if __name__ == '__main__':
    send_push(group_id='Cd8838ffe33ac87f0595ac2be8ce6579f', message='Test')
