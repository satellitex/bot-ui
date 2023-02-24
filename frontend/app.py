# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

import os

import pandas as pd
import plotly.graph_objs as go
from dash import Dash, dcc, html
from dotenv import load_dotenv
from plotly.subplots import make_subplots

load_dotenv(override=True)

app = Dash(__name__)

# assume you have a "long-form" data frame
# see https://plotly.com/python/px-arguments/ for more options


"""
# 高速取引 bot のヴィジュアライズ
以下データ構造
```
timestamp:
残高: USD 建て
残高: USD 建て(売指値ベース)
BTC price: BTC の価格
ポジション: BTC, USD
ポジション: BTC_free, BTC_locked, USD_free, USD_lcoked
```
"""

csv_path = os.getenv("UI_CSV_PATH")
if csv_path is None:
    csv_path = "data/log/csv/kosoku_binance_BTCUSDT_5m_pl.csv"

df = pd.read_csv(csv_path)
df["unusd_pos"] = df["balance"] - df["usd_pos"]


def serve_layout():
    df = pd.read_csv(csv_path)
    df["unusd_pos"] = df["balance"] - df["usd_pos"]

    fig = make_subplots(
        specs=[[{"secondary_y": True}]], subplot_titles=["BTCUSDT5m 高速bot の損益"]
    )
    # 1. 残高推移
    fig.add_trace(go.Scatter(x=df["timestamp"], y=df["balance"], name="balance"))
    # 2. 理論残高推移
    fig.add_trace(go.Scatter(x=df["timestamp"], y=df["ideal_balance"], name="ideal"))
    # 3. USD の残高
    fig.add_trace(go.Scatter(x=df["timestamp"], y=df["usd_pos"], name="usd pos($)"))
    # 4. BTC になってる USD の残高(ドル建て) (1) = (3) + (4)
    fig.add_trace(go.Scatter(x=df["timestamp"], y=df["unusd_pos"], name="btc pos($)"))
    # 5. BTC の価格
    fig.add_trace(
        go.Scatter(
            x=df["timestamp"],
            y=df["btc_price"],
            name="btc price",
            line=dict(color="orange"),
        ),
        secondary_y=True,
    )

    return html.Div(
        children=[
            html.H1(children="Bot Rewards Graph"),
            html.Div(
                children="""
            Dash: A web application framework for kosoku bot balances.
        """
            ),
            dcc.Graph(
                id="example-graph",
                figure=fig,
            ),
        ]
    )


app.layout = serve_layout

if __name__ == "__main__":
    app.run_server(host='0.0.0.0', debug=True)
