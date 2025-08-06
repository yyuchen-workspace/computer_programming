import requests
import json
from collections import defaultdict


'''暫存中英對照表
name_map = {
    "Temperature": "溫度",
    "DewPoint": "露點溫度",
    "RelativeHumidity": "相對濕度",
    "ApparentTemperature": "體感溫度",
    "ComfortIndex": "舒適度",
    "ComfortIndexDescription": "舒適度描述",
    "WindSpeed": "風速",
    "BeaufortScale": "蒲福風級",
    "ProbabilityOfPrecipitation": "降雨機率",
    "Weather": "天氣現象",
    "WeatherDescription": "天氣描述",
    "WindDirection": "風向",
    "WeatherCode": "天氣代碼"
}
'''


url = f"https://opendata.cwa.gov.tw/api/v1/rest/datastore/F-D0047-069"
api_token = "CWA-8917E0F0-A194-4359-9634-D8AF9CDBB872"
def get_weather(city_name, district_name, show_top_ndata=10):
    params = {
        "Authorization" : api_token,
        "format": "JSON",
        "LocationName" : district_name
    }
    
    
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()

        print("臺灣各縣市鄉鎮未來3天天氣預報")
        cities = data['records']['Locations']
        found_city = False
        found_district = False

        for city in cities:
            if city['LocationsName'] == city_name:
                found_city = True
                for district in city['Location']:
                    if district['LocationName'] == district_name:
                        found_district = True
                        print(f"\n📍 {city_name} {district_name}")

                        weather_elements = district['WeatherElement']
                        weather_merged = defaultdict(dict)

                        for elem in weather_elements:
                            elem_name = elem['ElementName']#內容名字
                            for time_list in elem['Time']:#時間結構
                                # 自動偵測是 DataTime 或 StartTime
                                time = time_list.get('DataTime') or time_list.get('StartTime')
                                element_value = time_list['ElementValue']
                                if element_value:
                                    weather_merged[time][elem_name] = element_value[0]

                        # 印出前 N 筆資料
                        for time in sorted(weather_merged.keys())[:show_top_ndata]:#如...{weather_merge{"Datatime"{"ElementName":{"temperature":"34"}}}}
                            print(f"\n🕒 時間:{time}")
                            for cname, temperature in weather_merged[time].items():
                                  for k, v in temperature.items():
                                      print(f"{cname}({k}): {v}")
            return               
                             
        #if not found_district:
        print(f"⚠️ 找不到 {district} 的天氣資料。")

    except requests.exceptions.HTTPError as http_err:
        print("❌ HTTP 錯誤：", http_err)
    except requests.exceptions.RequestException as req_err:
        print("❌ 其他請求錯誤（例如網路錯誤）", req_err)
    except KeyError as ke:
        print("❌ 回傳資料格式錯誤，缺少欄位：", ke)
    except Exception as e:
        print("❌ 其他非 requests 錯誤：", e)   

if __name__ == "__main__":
    get_weather("新北市", "深坑區", show_top_ndata=10)