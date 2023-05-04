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
openai.api_key = "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"
model_engine = "text-davinci-003"
output_length = 500

app = Flask(__name__)

line_bot_api = LineBotApi('F3iWzws3ypon002uN+swy+EBDOsVnjl79FXkhKkd4Ev7ZfBGixANYB9kSuSNLX/GhbiPirq/w8AD2Bo8O4Ctp/Bq3EXGluy0DseZR4+zCF9jsgoqsjEYVhsCSfpLZ3HEA+5UcrajxljyahU/audoKgdB04t89/1O/w1cDnyilFU=')
webhook_handler = WebhookHandler('c1e3f01970d9f2828273807a3b9cab6e')

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