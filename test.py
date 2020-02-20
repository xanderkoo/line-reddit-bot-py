from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)

app = Flask(__name__)

line_bot_api = LineBotApi('SADT02d0iaUexaWwgg4XPZD/BvHLpAE9A0jfzqgcmCQQNsLAH9EwoDhQo8IgOQAhqGtk+44QYYvzUET4X7kEwjGxgKiJ1NStjDrH6tkuFJTOTp0N9LGaBcFDxIq3KG/IGw5qY6pSXecn9V5C7caugQdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('965755332759aab0bdb7591d49546997')


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
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text))
    print('Hello')


if __name__ == "__main__":
    app.run()
