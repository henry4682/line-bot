from flask import Flask
app = Flask(__name__)

from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage

import os 
from dotenv import load_dotenv

load_dotenv()

# print(os.environ.get('line_api'))
line_bot_api = LineBotApi(os.environ.get('line_api'))
handler = WebhookHandler(os.environ.get('handler'))

@app.route('/')
@app.route('/index')
def index():
    return 'Hello World'

@app.route('/callback', methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def handler_message(event):
    line_bot_api.reply_message(event.reply_token, TextSendMessage(text=event.message.text))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)

