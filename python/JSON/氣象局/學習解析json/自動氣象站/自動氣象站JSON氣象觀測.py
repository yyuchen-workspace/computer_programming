import requests
import json

# 正確資料來源
url = "https://opendata.cwa.gov.tw/fileapi/v1/opendataapi/O-A0001-001?Authorization=CWA-8917E0F0-A194-4359-9634-D8AF9CDBB872&format=JSON"

try:
    response = requests.get(url)
    response.raise_for_status()
    data = response.json()

    stations = data["cwaopendata"]["dataset"]["Station"]
    print("八里區氣象:")    
    found = False
    DO_LOCATION = "八里區"
    for station in stations:
        geo = station["GeoInfo"]   
       
        if geo['TownName'] == DO_LOCATION:
            found = True
            name = station["StationName"]
            time = station["ObsTime"]["DateTime"]
            elements = station["WeatherElement"]

            print(f"\n觀測站：{name}")
            print(f"時間：{time}")
            print(f"地點：{geo['CountyName']} {geo['TownName']}")
            print(f"  • 氣溫：{elements.get('AirTemperature')}°C")
            print(f"  • 濕度：{elements.get('RelativeHumidity')}%")
            print(f"  • 降雨量：{elements.get('Now', {}).get('Precipitation')} mm")
            print(f"  • 風速：{elements.get('WindSpeed')} m/s")
            print(f"  • 風向：{elements.get('WindDirection')}°") 

except Exception as e:
    print(f"錯誤發生：{e}")

if not found:
    print("未找到該區資料")

