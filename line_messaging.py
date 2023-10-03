'''Line messenger app module.
- connect to Line API
- send a push message

ISSUE: PushMessageRequest does not parse the text message correctly
'''
import json
import os

from linebot.v3.messaging import (
    ApiClient,
    Configuration,
    MessagingApi,
)
from linebot.v3.messaging.models.push_message_request import PushMessageRequest

configuration = Configuration(
    access_token=os.environ['LINE_CHANNEL_ACCESS_TOKEN'])


def send_push(group_id: str, message: str):
    with ApiClient(configuration) as api_client:
        api_instance = MessagingApi(api_client)
        messages = [{"type": "text", "text": message}]
        push_request = PushMessageRequest(to=group_id, messages=messages)
        try:
            # Check the raw payload before sending
            request_payload = json.dumps(push_request.to_dict(), indent=2)
            print('Raw API Request Payload:\n', request_payload)

            api_response = api_instance.push_message(push_request)
            print('The response of MessagingApi -> push_message:\n',
                  api_response)
        except Exception as e:
            print("Exception when calling MessagingApi -> push_message: %s\n" %
                  e)


if __name__ == '__main__':
    send_push(group_id='Cd8838ffe33ac87f0595ac2be8ce6579f', message='Test')
