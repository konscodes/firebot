'''Line messenger app module.
- connect to Line API
- send a push message'''
import os

from flask import Flask, abort, request
from linebot.v3 import WebhookHandler
from linebot.v3.exceptions import InvalidSignatureError

from linebot.v3.webhooks import (
    JoinEvent, 
    GroupSource
)

app = Flask(__name__)

channel_secret = os.environ['LINE_CHANNEL_SECRET']
handler = WebhookHandler(channel_secret)

@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        app.logger.info(
            'Invalid signature. Please check your channel access token/channel secret.'
            )
        abort(400)

    return 'OK'


@handler.add(JoinEvent)
def handle_group_joined(event):
    print(event)
    if isinstance(event.source, GroupSource):
        print('GroupID', event.source.group_id)


if __name__ == "__main__":
    app.run(host='0.0.0.0')