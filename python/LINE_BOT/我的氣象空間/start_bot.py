from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.models import MessageEvent, TextMessage, TextSendMessage
from linebot.exceptions import InvalidSignatureError
from pyngrok import ngrok
from pyngrok import conf
import json
import os

# ===== 修改為你的 LINE 資訊 =====
ACCESS_TOKEN = 'FtP6i/TQvFzlMQmh1LKkAFtdvvHV9bFxowTsp1K5psjAS99LLX7WJgikwVYyedBMKDXorGISc8SpOyOZzANH2qrciAvNOlMGw6xWKEuA/Cokn0Lo6Lxm4j30ath4tdLwCVwRqi3KtfoIePTFZxU1igdB04t89/1O/w1cDnyilFU='
CHANNEL_SECRET = 'a36a6d1dc8213a829542824680b85339'
# =================================

# 建立 Flask App
app = Flask(__name__)

line_bot_api = LineBotApi(ACCESS_TOKEN)
handler = WebhookHandler(CHANNEL_SECRET)

@app.route("/webhook", methods=['POST'])
def callback():
    body = request.get_data(as_text=True)
    signature = request.headers.get('X-Line-Signature', '')

    try:
        handler.handle(body, signature)
        data = json.loads(body)
        event = data['events'][0]

        if event['type'] == 'message' and event['message']['type'] == 'text':
            msg = event['message']['text']
            reply = f"你說了：{msg}"
        else:
            reply = '你傳的不是文字喔～'

        line_bot_api.reply_message(
            event['replyToken'],
            TextSendMessage(text=reply)
        )
    except InvalidSignatureError:
        abort(400)
    except Exception as e:
        print("⚠️ 錯誤:", e)
        print("📦 原始資料:", body)
        return 'ERROR', 500

    return 'OK'

if __name__ == "__main__":
    port = 5000

    # 啟用 ngrok 隧道
    config = conf.PyngrokConfig(ngrok_path=r"C:\ProgramData\chocolatey\bin\ngrok.exe")  # ← 改成你的 ngrok 路徑
    public_url = ngrok.connect(port, pyngrok_config=config).public_url
    print("✅ ngrok 公開網址：", public_url)
    print("📌 請將此網址貼到 LINE Webhook 設定：", public_url + "/webhook")

    # 啟動 Flask
    app.run(port=port)
