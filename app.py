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
import os

app = Flask(__name__)
app.debug = False

YOUR_CHANNEL_ACCESS_TOKEN = os.environ["kDji1+bU35yIn5K2O4hx6UhpjlgxAtBdOVgeSCyK62+g9aYXSV2FzSbziBpnrr5vbQBNhNS4/a2juuzs0/Qit4aN7Djwk6TNpWhL4HBBOHIXXDAXqOUpXZaZxTp6TAD73LWON6auA4gvBlMYRkJw+gdB04t89/1O/w1cDnyilFU="]
YOUR_CHANNEL_SECRET = os.environ["c0aa75db34d80d9149c60a2576c6f61"]

line_bot_api = LineBotApi(YOUR_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(YOUR_CHANNEL_SECRET)

@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']

    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text))

if __name__ == "__main__":
    port = int(os.getenv("PORT"))
    app.run(host="0.0.0.0", port=port)