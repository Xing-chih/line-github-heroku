import os
import json

from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
    FlexSendMessage, CarouselContainer, BubbleContainer
)


app = Flask(__name__)

line_bot_api = LineBotApi(os.environ['CHANNEL_ACCESS_TOKEN'])
handler = WebhookHandler(os.environ['CHANNEL_SECRET'])


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
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    if event.message.text == 'show me':
        with open('test.json', 'r') as f:

            bubble_flex_send_message = FlexSendMessage(
                alt_text="hello", contents=json.load(f))

        line_bot_api.reply_message(
            event.reply_token,
            bubble_flex_send_message
        )

    elif event.message.text == 'oh':
        flex_message = FlexSendMessage(
            alt_text='hello',
            contents={
                'type': 'bubble',
                'direction': 'ltr',
                'hero': {
                    'type': 'image',
                    'url': 'https://example.com/cafe.jpg',
                    'size': 'full',
                    'aspectRatio': '20:13',
                    'aspectMode': 'cover',
                    'action': {'type': 'uri', 'uri': 'http://example.com', 'label': 'label'}
                }
            }
        )
        line_bot_api.reply_message(
            event.reply_token,
            flex_message
        )

    else:
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=event.message.text))


# if __name__ == "__main__":
#     app.run()

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=os.environ['PORT'])
