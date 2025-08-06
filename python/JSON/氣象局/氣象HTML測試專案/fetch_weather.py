# src/fetch_weather.py
import requests
import json
import os
from collections import defaultdict

name_map = {
    "Temperature": "溫度",
    "ApparentTemperature": "體感溫度",
    "Weather": "天氣現象"
}

def translate_name(key):
    return name_map.get(key, key)

def parse_time(t):
    return t.get("DataTime") or f"{t['StartTime']} ~ {t['EndTime']}"

def get_weather(city_name, district_name, show_top_ndata=6, include_elements=None):
    url = "https://opendata.cwa.gov.tw/api/v1/rest/datastore/F-D0047-069"
    api_token = "CWA-8917E0F0-A194-4359-9634-D8AF9CDBB872"
    params = {
        "Authorization": api_token,
        "format": "JSON",
        "locationName": district_name
    }

    response = requests.get(url, params=params)
    response.raise_for_status()
    data = response.json()

    for city in data['records']['Locations']:
        if city['LocationsName'] != city_name:
            continue
        for district in city['Location']:
            if district['LocationName'] != district_name:
                continue

            weather_merged = defaultdict(dict)
            for elem in district['WeatherElement']:
                elem_name = elem['ElementName']
                if include_elements and elem_name not in include_elements:
                    continue
                for t in elem['Time'][:show_top_ndata]:
                    time_key = parse_time(t)
                    if t.get("ElementValue") and len(t["ElementValue"]) > 0:
                        for k, v in t["ElementValue"][0].items():
                            weather_merged[time_key][elem_name] = v

            # 整理為 list 格式
            weather_list = []
            for time in sorted(weather_merged.keys()):
                row = {"時間": time}
                for k, v in weather_merged[time].items():
                    row[translate_name(k)] = v
                weather_list.append(row)

            return {
                "city": city_name,
                "district": district_name,
                "weather_data": weather_list
            }

if __name__ == "__main__":
    result = get_weather("新北市", "深坑區")

    # 建立 ../data 資料夾（如果不存在）
    os.makedirs("data", exist_ok=True)

    with open("data/weather_data.json", "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)

    print("✅ 天氣資料已存入 data/weather_data.json")
