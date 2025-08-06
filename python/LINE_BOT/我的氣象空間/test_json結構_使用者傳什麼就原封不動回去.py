from flask import Flask, request, abort
import requests, json, os
from pyngrok import conf, ngrok 
from dotenv import load_dotenv


load_dotenv()   # 這行會自動把 .env 裡的變數載入到 os.environ


app = Flask(__name__)


# 把你的 channel access token 放到環境變數
LINE_TOKEN = os.getenv("LINE_CHANNEL_ACCESS_TOKEN")
if not LINE_TOKEN:
    raise ValueError("請先在 .env 裡設定 LINE_CHANNEL_ACCESS_TOKEN")


# === ngrok 設定 (自動開啟 tunnel) ===
port = "5000"
# 如果你已經把 ngrok 加到 PATH，就不需要設定 ngrok_path
config = conf.PyngrokConfig(ngrok_path=r"C:\ProgramData\chocolatey\bin\ngrok.exe")
public_url = ngrok.connect(port, pyngrok_config=config).public_url
print(f" * ngrok tunnel \"{public_url}\" -> \"http://127.0.0.1:{port}\"")


@app.route("/", methods=["POST"])
def linebot():
    body      = request.get_data(as_text=True)
    json_data = json.loads(body)

    # 1. 取出第一個 event
    event = json_data["events"][0]

    # 2. 確保這是一則文字訊息
    if event["type"] == "message" and event["message"]["type"] == "text":
        user_text   = event["message"]["text"]       # 使用者傳的文字
        reply_token = event["replyToken"]            # 用來回覆的 token

        # 3. 組 reply payload
        payload = {
            "replyToken": reply_token,
            "messages": [
                {
                    "type": "text",
                    "text": f"：{user_text}"
                }
            ]
        }
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {LINE_TOKEN}"
        }

        # 4. 呼叫 LINE 回覆訊息
        resp = requests.post(
            "https://api.line.me/v2/bot/message/reply",
            headers=headers,
            data=json.dumps(payload)
        )

        if resp.status_code != 200:
            print("Reply failed:", resp.status_code, resp.text)

    return "OK"

if __name__ == "__main__":
    # ngrok 已經把外網導到這裡
    app.run(host="0.0.0.0", port=5000)
