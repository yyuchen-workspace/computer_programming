import requests
import json

DO_DIS = "深坑區"
url = "https://opendata.cwa.gov.tw/api/v1/rest/datastore/O-A0001-001?Authorization=CWA-8917E0F0-A194-4359-9634-D8AF9CDBB872"

response = requests.get(url)
response.raise_for_status()
data = response.json()

stations = data['records']['Station']

found = False
for station in stations:
    geo = station.get("GeoInfo", {})
    if geo.get("TownName") == DO_DIS:
        found = True
        name = station.get("StationName", "未知測站")
        time = station.get("ObsTime", {}).get("DateTime", "無資料")
        elements = station.get("WeatherElement", {})

        print(f"觀測站：{name}")
        print(f"時間：{time}")
        print(f"地點：{geo.get('CountyName')} {geo.get('TownName')}")
        print(f"  • 氣溫：{elements.get('AirTemperature')}°C")
        print(f"  • 濕度：{elements.get('RelativeHumidity')}%")
        print(f"  • 降雨量：{elements.get('Now', {}).get('Precipitation')} mm")
        print(f"  • 風速：{elements.get('WindSpeed')} m/s")
        print(f"  • 風向：{elements.get('WindDirection')}°")

if not found:
    print(f"No data of {DO_DIS}")