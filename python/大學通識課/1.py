import requests
import json

api_token = "CWA-45D530C8-20F2-48F6-9F45-5E27789BF627"
location = "深坑區"

url = "https://opendata.cwa.gov.tw/api/v1/rest/datastore/F-D0047-069"
params = {
    "Authorization": api_token,
    "format": "JSON",
    "locationName": location
}

response = requests.get(url, params=params)

if response.status_code == 200:
    data = response.json()
    # 打印出 API 返回的完整資料
    print(json.dumps(data, indent=4, ensure_ascii=False))  # 格式化打印 JSON
else:
    print("❌ API 請求失敗", response.status_code)


