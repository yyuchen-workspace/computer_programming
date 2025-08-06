#%%
# 1️⃣ Plotly 畫圖版本（氣溫與濕度折線圖）
import requests
import json
import plotly.graph_objects as go
from collections import defaultdict

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

def get_weather_data(city_name, district_name, show_top_ndata=10):
    url = "https://opendata.cwa.gov.tw/api/v1/rest/datastore/F-D0047-069"
    api_token = "CWA-8917E0F0-A194-4359-9634-D8AF9CDBB872"
    params = {
        "Authorization" : api_token,
        "format": "JSON",
        "locationName" : district_name
    }

    response = requests.get(url, params=params)
    response.raise_for_status()
    data = response.json()

    cities = data['records']['Locations']
    for city in cities:
        if city['LocationsName'] == city_name:
            for district in city['Location']:
                if district['LocationName'] == district_name:
                    weather_elements = district['WeatherElement']
                    weather_merged = defaultdict(dict)

                    for elem in weather_elements:
                        elem_name = elem['ElementName']
                        for time_list in elem['Time'][:show_top_ndata]:
                            time = time_list.get('DataTime') or time_list.get('StartTime')
                            element_value = time_list['ElementValue']
                            if element_value:
                                for k, v in element_value[0].items():
                                    weather_merged[time][k] = v
                    return weather_merged
    return {}

#%%
# 取得資料並畫圖
weather = get_weather_data("新北市", "深坑區", show_top_ndata=10)

times = sorted(weather.keys())
temps = [float(weather[t].get("Temperature", 'nan')) for t in times]
humds = [float(weather[t].get("RelativeHumidity", 'nan')) for t in times]

fig = go.Figure()
fig.add_trace(go.Scatter(x=times, y=temps, mode='lines+markers', name='溫度'))
fig.add_trace(go.Scatter(x=times, y=humds, mode='lines+markers', name='相對濕度'))
fig.update_layout(title='新北市深坑區氣溫與相對濕度變化',
                  xaxis_title='時間',
                  yaxis_title='數值',
                  template='plotly_white')
fig.show()

#%%
# 2️⃣ Dash 網頁互動版本
import dash
from dash import html, dcc, Input, Output

app = dash.Dash(__name__)
app.layout = html.Div([
    html.H2("新北市深坑區未來天氣圖表"),
    dcc.Slider(id='count-slider', min=3, max=10, step=1, value=6,
               marks={i: str(i) for i in range(3, 11)}),
    dcc.Graph(id='weather-graph')
])

@app.callback(
    Output('weather-graph', 'figure'),
    Input('count-slider', 'value')
)
def update_chart(top_n):
    weather = get_weather_data("新北市", "深坑區", show_top_ndata=top_n)
    times = sorted(weather.keys())
    temps = [float(weather[t].get("Temperature", 'nan')) for t in times]
    humds = [float(weather[t].get("RelativeHumidity", 'nan')) for t in times]

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=times, y=temps, mode='lines+markers', name='溫度'))
    fig.add_trace(go.Scatter(x=times, y=humds, mode='lines+markers', name='相對濕度'))
    fig.update_layout(title='溫度與相對濕度變化', xaxis_title='時間', yaxis_title='數值', template='plotly_white')
    return fig

if __name__ == '__main__':
    app.run_server(debug=True)
