from flask import Flask, request
from pyngrok import ngrok    # 本機環境不需要
from pyngrok import conf
import json

app = Flask(__name__)

# 本機環境不需要下面這三行
port = "5000"               
config = conf.PyngrokConfig(ngrok_path=r"C:\ProgramData\chocolatey\bin\ngrok.exe")  # ← 改成你的 ngrok 路徑
public_url = ngrok.connect(port, pyngrok_config=config).public_url
print(f" * ngrok tunnel \"{public_url}\" -> \"http://127.0.0.1:{port}\" ")

@app.route("/", methods=['POST'])
def linebot():
    body = request.get_data(as_text=True)
    json_data = json.loads(body)
    print(json_data)               # 印出 json_data
    return 'OK'
if __name__ == "__main__":
  app.run()