# Flask Web API 應用程式
# 提供 GET 和 POST 方法來處理應用程式資訊的讀取和儲存

from flask import Flask, render_template, request, jsonify, json

# 建立 Flask 應用程式實例
app = Flask(__name__)

# 路由：顯示主頁面
@app.route('/data')
def webapi():
    """
    顯示 data.html 頁面
    這個頁面包含了 AJAX 操作的使用者界面
    """
    return render_template('data.html')

# 路由：處理 GET 請求 - 讀取應用程式資訊
@app.route('/data/message', methods=['GET'])
def getDataMessage():
    """
    處理 GET 請求，從 JSON 檔案讀取應用程式資訊
    回傳格式：JSON 物件包含 appInfo
    """
    if request.method == "GET":
        # 開啟並讀取 JSON 檔案
        with open('static/data/message.json', 'r') as f:
            data = json.load(f)  # 將 JSON 檔案內容載入為 Python 字典
            print("讀取的資料: ", data)  # 在終端機顯示讀取的資料
        f.close()  # 關閉檔案
        return jsonify(data)  # 將資料轉換為 JSON 格式回傳給前端
    else:
        return "error"  # 如果不是 GET 請求則回傳錯誤

# 路由：處理 POST 請求 - 儲存應用程式資訊
@app.route('/data/message', methods=['POST'])
def setDataMessage():
    """
    處理 POST 請求，將前端傳送的表單資料儲存到 JSON 檔案
    接收表單欄位：app_id, app_name, app_version, app_author, app_remark
    """
    if request.method == "POST":
        # 建立資料結構，將表單資料組織成 JSON 格式
        data = {
            'appInfo': {
                'id': int(request.form['app_id']),        # 將字串轉換為整數
                'name': request.form['app_name'],         # 應用程式名稱
                'version': request.form['app_version'],   # 版本號
                'author': request.form['app_author'],     # 作者
                'remark': request.form['app_remark']      # 備註
            }
        }
        print("資料類型:", type(data))  # 顯示資料類型（用於除錯）
        
        # 將資料寫入 JSON 檔案，使用 indent=4 讓格式更易讀
        with open('static/data/input.json', 'w') as f:
            json.dump(data, f, indent=4)  # 以 4 個空格縮排的格式儲存
        f.close()  # 關閉檔案
        
        return jsonify(result='OK')  # 回傳成功訊息給前端
    else:
        return "error"  # 如果不是 POST 請求則回傳錯誤

# 主程式入口點
if __name__ == '__main__':
    # 啟動 Flask 開發伺服器
    # 預設在 http://127.0.0.1:5000 執行
    app.run()