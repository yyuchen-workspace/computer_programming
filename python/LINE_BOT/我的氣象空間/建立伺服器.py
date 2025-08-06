from flask import Flask, request, abort
import json
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage

app = Flask(__name__)

ACCESS_TOKEN = 'FtP6i/TQvFzlMQmh1LKkAFtdvvHV9bFxowTsp1K5psjAS99LLX7WJgikwVYyedBMKDXorGISc8SpOyOZzANH2qrciAvNOlMGw6xWKEuA/Cokn0Lo6Lxm4j30ath4tdLwCVwRqi3KtfoIePTFZxU1igdB04t89/1O/w1cDnyilFU='#你的 access token
CHANNEL_SECRET = 'a36a6d1dc8213a829542824680b85339' #你的 secret

line_bot_api = LineBotApi(ACCESS_TOKEN)
handler = WebhookHandler(CHANNEL_SECRET)

@app.route("/", methods=['POST'])
def callback():
    body = request.get_data(as_text=True)
    signature = request.headers.get('X-Line-Signature', '')
    try:
        handler.handle(body, signature)
        data = json.loads(body)
        event = data['events'][0]

        if event['type'] == 'message' and event['message']['type'] == 'text':
            msg = event['message']['text']
            print("使用者傳來：", msg)
            reply = f"{msg}"
        else:
            reply = '你傳的不是文字喔～'

        line_bot_api.reply_message(
            event['replyToken'],
            TextSendMessage(text=reply)
        )
    except InvalidSignatureError:
        abort(400)
    except Exception as e:
        print("錯誤：", e)
        print("原始內容：", body)
        return 'ERROR', 500

    return 'OK'

if __name__ == "__main__":
    app.run(port=5000)
