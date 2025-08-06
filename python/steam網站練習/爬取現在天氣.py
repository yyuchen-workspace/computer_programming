import requests
url = '你的氣象觀測資料 JSON 網址'
data = requests.get(url)
data_json = data.json()
location = data_json['cwaopendata']['dataset']['Station']

weather = {}   # 新增一個 weather 字典

for i in location:
    name = i['StationName']            # 測站地點
    city = i['GeoInfo']['CountyName']  # 城市
    area = i['GeoInfo']['TownName']    # 行政區
    temp = i['WeatherElement']['AirTemperature']     # 氣溫
    humd = i['WeatherElement']['RelativeHumidity']   # 相對濕度
    msg = f'{temp} 度，相對濕度 {humd}%'  # 組合成天氣描述
    try:
        weather[city][name]=msg   # 記錄地區和描述
    except:
        weather[city] = {}        # 如果每個縣市不是字典，建立第二層字典
        weather[city][name]=msg   # 記錄地區和描述

show = ''
for i in weather:
    show = show + i + ','                       # 列出可輸入的縣市名稱
show = show.strip(',')                          # 移除結尾逗號
a = input(f'請輸入下方其中一個縣市\n( {show} )\n')  # 讓使用者輸入縣市名稱

show = ''
for i in weather[a]:
    show = show + i + ','                       # 列出可輸入的地點名稱
show = show.strip(',')                          # 移除結尾逗號
b = input(f'請輸入{a}的其中一個地點\n( {show} )\n') # 讓使用者輸入觀測地點名稱
print(f'{a}{b}，{weather[a][b]}。')              # 顯示結果