import requests
import json

api_token = "CWA-45D530C8-20F2-48F6-9F45-5E27789BF627"
location = "深坑區"

url = f"https://opendata.cwa.gov.tw/api/v1/rest/datastore/F-D0047-069"
params = {
    "Authorization": api_token,
    "format": "JSON",
    "locationName": location
}

response = requests.get(url, params=params)

if response.status_code == 200:
    data = response.json()
    try:
        location_data = data["records"]["locations"][0]["location"][0]
        print(f"📍 深坑區預報：")
        for element in location_data["weatherElement"]:
            print(f"\n🌟 {element['description']}")
            for t in element["time"][:3]:  # 只顯示前3筆
                start = t["startTime"]
                end = t["endTime"]
                value = t["elementValue"][0]["value"]
                print(f"🕒 {start} ~ {end}：{value}")
    except Exception as e:
        print("⚠️ 資料格式錯誤或地點不存在", e)
else:
    print("❌ API 請求失敗", response.status_code)
