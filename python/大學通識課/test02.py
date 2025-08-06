import requests

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
        location_data = data["records"]["locations"][0]["location"][0]
        print(f"📍 {location}天氣預報：")

        for element in location_data["weatherElement"]:
            name = elemesnt["elementName"]
            if name == "WeatherDescription":
                print(f"\n🌟 天氣概況（未來3時段）")
                for t in element["time"][:3]:
                    start = t["startTime"]
                    end = t["endTime"]
                    desc = t["elementValue"][0]["value"]
                    print(f"🕒 {start} ~ {end}：{desc}")

            elif name == "Temperature":
                print(f"\n🌡️ 溫度預報（未來3時段）")
                for t in element["time"][:3]:
                    time = t.get("dataTime", "N/A")
                    temp = t["elementValue"][0]["value"]
                    print(f"🕒 {time}：{temp}°C")

    except (KeyError, IndexError, TypeError) as e:
        print("⚠️ 資料格式錯誤或地點不存在", e)
else:
    print("❌ API 請求失敗", response.status_code)
