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
    try:
        data = response.json()

        # 檢查是否包含 'records' 和 'locations'
        if "records" not in data or not data["records"]:
            print("⚠️ 無法找到資料，可能是因為地點不正確或資料格式問題。")
        else:
            locations = data["records"].get("locations", [])
            if not locations:
                print("⚠️ 找不到對應的地點資料。")
            else:
                location_data = locations[0].get("location", [])
                if not location_data:
                    print("⚠️ 找不到指定地點的天氣資料。")
                else:
                    # 顯示預報資訊
                    print(f"📍 {location} 預報：")
                    for element in location_data[0].get("weatherElement", []):
                        print(f"\n🌟 {element.get('description', '無法取得描述')}")
                        for t in element.get("time", [])[:3]:  # 只顯示前3筆
                            start = t.get("startTime", "未知")
                            end = t.get("endTime", "未知")
                            value = t.get("elementValue", [{}])[0].get("value", "未知")
                            print(f"🕒 {start} ~ {end}：{value}")
    except (json.JSONDecodeError, KeyError, TypeError) as e:
        print(f"⚠️ 資料處理錯誤：{e}")
else:
    print("❌ API 請求失敗", response.status_code)
