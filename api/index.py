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

line_bot_api = LineBotApi('F3iWzws3ypon002uN+swy+EBDOsVnjl79FXkhKkd4Ev7ZfBGixANYB9kSuSNLX/GhbiPirq/w8AD2Bo8O4Ctp/Bq3EXGluy0DseZR4+zCF9jsgoqsjEYVhsCSfpLZ3HEA+5UcrajxljyahU/audoKgdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('c1e3f01970d9f2828273807a3b9cab6e')


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


if __name__ == "__main__":
    app.run()