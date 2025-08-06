
import requests
import json
from collections import defaultdict

# 中英文對照表
'''
name_map = {
    "AirTemperature": "氣溫",
    "RelativeHumidity": "相對濕度",
    "WindSpeed": "風速",
    "WindDirection": "風向",
    "Weather": "天氣",
    "Precipitation": "降雨量",
    "AirPressure": "氣壓",
    "PeakGustSpeed": "瞬間最大陣風",
    "DateTime": "時間"
}
# 中文轉英文對照
convert_name = {v : k for k, v in name_map.items()}
'''

def flatten_dict(d, parent_key='', sep='.'):
    items = {}
    for k, v in d.items():
        new_key = f"{parent_key}{sep}{k}" if parent_key else k
        if isinstance(v, dict):
            items.update(flatten_dict(v, new_key, sep))
        else:
            items[new_key] = v
    return items


url = "https://opendata.cwa.gov.tw/api/v1/rest/datastore/O-A0001-001"
api_token = "CWA-8917E0F0-A194-4359-9634-D8AF9CDBB872"

def weather_information(county_name, town_name, show_top_n_data, include_elements):
    params = {
        "Authorization" : api_token,
        "format" : "JSON",
        "TownName" : town_name
    }
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        found_county_town = False
        station = data['records']['Station']
        for station_list in station:
            station_name = station_list['StationName']#觀測站名稱
            datatime = station_list['ObsTime']['DateTime']#測量時間
            geoinfo = station_list['GeoInfo']
            if geoinfo['CountyName'] == county_name and geoinfo['TownName'] == town_name:
                found_county_town = True
                weather_merge = defaultdict(dict)
                weather_element = station_list['WeatherElement']#氣候字典
                for k, v in weather_element.items():
                    if include_elements and k not in include_elements:
                        continue
                    weather_merge['town_name'][k] = v
                
                
                print(f"{county_name}{town_name}現在氣象資料:")
                flat = flatten_dict(weather_merge['town_name'])
                for k, v in flat.items():
                    display_value = "未觀測" if v == "-99" else v
                    print(f"{k}: {display_value}")
                return 
            
        if not found_county_town:                  
                print(f"錯誤: 未找到{town_name}資料")
    except requests.exceptions.HTTPError as http_error:
        print(f"HTTP 錯誤: {http_error}")



if __name__ =="__main__":
    county_name = input(f"請輸入縣市名稱: ").strip()#去除空白與換行
    while not county_name:
        county = input(f"請再次輸入縣市名稱: ").strip()
    town_name = input(f"請輸入鄉鎮市區名稱: ").strip()
    while not town_name:
        town_name = input(f"請再次輸入鄉鎮市區名稱: ").strip()
    do_elements = ["AirTemperature"]#可切換None以測試
    weather_information(county_name, town_name, show_top_n_data=10, include_elements = do_elements)
