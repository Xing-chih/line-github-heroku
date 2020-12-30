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
        with open('test.json', 'r', encoding='utf-8') as f:
            bubble_container = BubbleContainer.new_from_json_dict(json.load(f))

        bubble_flex_send_message = FlexSendMessage(
            alt_text="hello", contents=bubble_container)

        line_bot_api.reply_message(
            event.reply_token,
            bubble_flex_send_message
        )

    else:
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=event.message.text))


# if __name__ == "__main__":
#     app.run()

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=os.environ['PORT'])
