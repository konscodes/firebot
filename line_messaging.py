'''Line messenger app module.
- connect to Line API
- send a push message'''
import os

from linebot.v3.messaging import (
    ApiClient,
    Configuration,
    MessagingApi,
)
from linebot.v3.messaging.models.push_message_request import PushMessageRequest

access_token = os.environ['LINE_CHANNEL_ACCESS_TOKEN']
configuration = Configuration(access_token)


def send_push(group_id: str, message: str):
    print('[Line] Sending push')
    with ApiClient(configuration) as api_client:
        api_instance = MessagingApi(api_client)
        push_request = PushMessageRequest(to=group_id,
                                          messages=[{
                                              "type": "text",
                                              "text": message
                                          }])
        try:
            api_response = api_instance.push_message(push_request)
            print('The response of MessagingApi -> push_message:\n',
                  api_response)
        except Exception as e:
            print("Exception when calling MessagingApi -> push_message: %s\n" %
                  e)
