'''Updated handler module to avoid using Line SDK
- listen for requests on Webhook url
- validate the signature
- handle events

TODO: implement validation process and test
'''
import json
import os

from flask import Flask, abort, request

app = Flask(__name__)

LINE_CHANNEL_SECRET = os.environ['LINE_CHANNEL_SECRET']


@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    if not validate_signature(LINE_CHANNEL_SECRET, signature):
        abort(400, 'Invalid signature')

    # handle webhook body for JoinEvent
    try:
        events = json.loads(body)['events']
        for event in events:
            if event['type'] == 'join':
                handle_join_event(event)
    except Exception as e:
        app.logger.error('Error handling events: ' + str(e))
        abort(500, 'Internal Server Error')

    return 'OK'


def validate_signature(channel_secret, signature):
    # Implement signature validation logic here
    # You can refer to Line API documentation for the validation process
    # https://developers.line.biz/en/docs/messaging-api/reference/#signature-validation
    return True  # For demonstration purposes, assuming the signature is always valid


def handle_join_event(event):
    group_id = event['source']['groupId']
    print('Group ID:', group_id)


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
