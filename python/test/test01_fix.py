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
        location_data = data["records"]["Locations"]["Location"]
        print(f"📍 深坑區預報：")
        for location in location_data: #結構循環查找
            district = location['LocationName'] #地區
            if district == "深坑區":
                weather = location['WeatherElement'] #天氣結構開始
                time = weather['Time'] #時間結構
            for i in time[:3]:  # 只顯示前3筆
                data_time = time['DataTime'] #時間
                Temperature = time['ElementValue']['Temperature'] #氣溫
                print(f"時間: {data_time}\n溫度: {Temperature}")
                
                
    except Exception as e:
        print("⚠️ 資料格式錯誤或地點不存在", e)
else:
    print("❌ API 請求失敗", response.status_code)
