import requests
import json

api_token = "CWA-8917E0F0-A194-4359-9634-D8AF9CDBB872"
location = "深坑區"

url = f"https://opendata.cwa.gov.tw/api/v1/rest/datastore/F-D0047-069"
params = {
    "Authorization": api_token,
    "format": "JSON",
    "LocationName": location
}

response = requests.get(url, params=params)

if response.status_code == 200:
    data = response.json()
    try:
        location_data = data['records']['Locations']
        for city in location_data:
            for district in city['Location']:
                district_name = district['LocationName']
                print(f"📍 {district_name}預報：")
                for weather_element in district["WeatherElement"]:
                    element_name = weather_element['ElementName']
                    for time_list in weather_element['Time'][:3]:
                        time1 = time_list.get('DataTime') or time_list.get('StartTime')
                        if time_list.get('EndTime'):
                            time2 = time_list.get('EndTime')
                        else:
                            time2 = None

                        element_value = time_list['ElementValue'][0]
                        # 自動抓唯一的 value
                        value = list(element_value.values())[0]

                        if time2:
                            print(f"🕒 {time1} ~ {time2}：{element_name} ➜ {value}")
                        else:
                            print(f"🕒 {time1}：{element_name} ➜ {value}")

                        

                
    except Exception as e:
        print("⚠️ 資料格式錯誤或地點不存在", e)
else:
    print("❌ API 請求失敗", response.status_code)