mport dash
from dash import dcc, html, dash_table
from dash.dependencies import Input, Output
import pandas as pd
import datetime

from market_scanner import scan_market
from portfolio_analyzer import analyze_portfolio

app = dash.Dash(__name__)
server = app.server

LANG = "fa"

TEXT = {
    "fa": {
        "title": "🤖 ربات هوشمند تحلیل بورس",
        "market_tab": "📊 سیگنال کل بازار",
        "portfolio_tab": "📁 پرتفوی من (Excel)",
        "upload": "آپلود فایل اکسل",
        "updated": "آخرین بروزرسانی"
    },
    "en": {
        "title": "🤖 Smart Stock Market Analyzer",
        "market_tab": "📊 Market Signals",
        "portfolio_tab": "📁 My Portfolio (Excel)",
        "upload": "Upload Excel File",
        "updated": "Last Update"
    }
}

app.layout = html.Div([
    html.H2(TEXT[LANG]["title"]),

    dcc.Tabs([
        dcc.Tab(label=TEXT[LANG]["market_tab"], children=[
            dcc.Interval(id="market-interval", interval=30*60*1000, n_intervals=0),
            html.Div(id="market-output")
        ]),

        dcc.Tab(label=TEXT[LANG]["portfolio_tab"], children=[
            dcc.Upload(
                id="upload-excel",
                children=html.Button(TEXT[LANG]["upload"]),
                multiple=False
            ),
            html.Div(id="portfolio-output")
        ])
    ])
])

@app.callback(
    Output("market-output", "children"),
    Input("market-interval", "n_intervals")
)
def update_market(n):
    df = scan_market()
    return dash_table.DataTable(
        data=df.to_dict("records"),
        columns=[{"name": i, "id": i} for i in df.columns],
        style_data_conditional=[
            {
                "if": {"filter_query": '{Signal} = "BUY"'},
                "backgroundColor": "#d4f8d4"
            },
            {
                "if": {"filter_query": '{Signal} = "SELL"'},
                "backgroundColor": "#f8d4d4"
            }
        ]
    )

@app.callback(
    Output("portfolio-output", "children"),
    Input("upload-excel", "contents")
)
def update_portfolio(contents):
    if contents is None:
        return ""
    df = analyze_portfolio(contents)
    return dash_table.DataTable(
        data=df.to_dict("records"),
        columns=[{"name": i, "id": i} for i in df.columns]
    )

if __name__ == "__main__":
    app.run_server(host="0.0.0.0", port=8050)
