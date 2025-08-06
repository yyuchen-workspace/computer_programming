import json
import dash
from dash import html, dcc, Input, Output
import plotly.express as px

with open("data/weather_data.json", encoding="utf-8") as f:
    data = json.load(f)
df = data["weather_data"]

app = dash.Dash(__name__)
app.layout = html.Div([
    html.H2(f"{data['city']} {data['district']} 天氣圖表"),
    dcc.Dropdown(
        id="column-selector",
        options=[{"label": col, "value": col} for col in df[0] if col != "時間"],
        value="溫度"
    ),
    dcc.Graph(id="weather-graph")
])

@app.callback(
    Output("weather-graph", "figure"),
    Input("column-selector", "value")
)
def update_chart(col):
    fig = px.line(df, x="時間", y=col, title=f"{col} 趨勢圖")
    fig.update_layout(template="plotly_white", xaxis_title="時間", yaxis_title=col)
    return fig

if __name__ == "__main__":
    app.run(debug=True)
