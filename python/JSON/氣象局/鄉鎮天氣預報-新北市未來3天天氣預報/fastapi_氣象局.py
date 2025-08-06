from fastapi import FastAPI, Query
from fastapi.responses import RedirectResponse  # 若要轉址
from typing import Optional, List
from collections import defaultdict
import requests


app = FastAPI(
    title="氣象資料 API",
    description="提供縣市、行政區氣象預報查詢服務",
    version="1.0.0"
)

# 直接回傳訊息
@app.get("/", tags=["Root"])
async def read_root():
    return {"message": "歡迎使用氣象資料 API，請至 /docs 查看文件"}

# 或者直接導向 swagger UI
@app.get("/home", include_in_schema=False)
async def redirect_to_docs():
    return RedirectResponse(url="/docs")


# 中英對照
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

def translate_name(be_translated_name):
    return name_map.get(be_translated_name, be_translated_name)

@app.get("/weather")
def get_weather(
    city_name: str = Query(..., description="城市名稱，如 新北市"),
    district_name: str = Query(..., description="鄉鎮名稱，如 深坑區"),
    show_top_n: int = Query(3, description="顯示筆數"),
    include_elements: Optional[List[str]] = Query(None, description="只顯示指定資料元素")
):
    url = "https://opendata.cwa.gov.tw/api/v1/rest/datastore/F-D0047-069"
    api_token = "CWA-8917E0F0-A194-4359-9634-D8AF9CDBB872"
    params = {
        "Authorization": api_token,
        "format": "JSON",
        "LocationName": district_name
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()

        result = []

        for city in data['records']['Locations']:
            if city['LocationsName'] == city_name:
                for district in city['Location']:
                    if district['LocationName'] == district_name:
                        weather_elements = district['WeatherElement']
                        weather_merged = defaultdict(dict)

                        for elem in weather_elements:
                            elem_name = elem['ElementName']
                            for time_list in elem['Time'][:show_top_n]:
                                time = time_list.get('DataTime') or time_list.get('StartTime')
                                for kv in time_list['ElementValue']:
                                    for k, v in kv.items():
                                        if include_elements and k not in include_elements:
                                            continue
                                        weather_merged[time][k] = v

                        for time in sorted(weather_merged.keys())[:show_top_n]:
                            entry = {"時間": time}
                            for k, v in weather_merged[time].items():
                                entry[translate_name(k)] = v
                            result.append(entry)

                        return {"地區": f"{city_name} {district_name}", "資料": result}

        return {"錯誤": f"找不到 {city_name} {district_name} 的天氣資料"}

    except requests.exceptions.RequestException as e:
        return {"錯誤": str(e)}
