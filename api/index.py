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

import openai
import os
openai.api_key = os.environ["OPENAI_API_KEY"]
model_engine = "text-davinci-003"
output_length = 500

app = Flask(__name__)

line_bot_api = LineBotApi('YOUR_CHANNEL_ACCESS_TOKEN')
webhook_handler = WebhookHandler('YOUR_CHANNEL_SECRET')

@app.route("/")
def home():
    return "小羅伯特活著"

@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        webhook_handler.handle(body, signature)
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'


@webhook_handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    response = openai.Completion.create(
        engine=model_engine,
        prompt=event.message.text,
        max_tokens=output_length,
    )
    output_text = response.choices[0].text.strip()
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=output_text))


if __name__ == "__main__":
    app.run()