
import dash
import datetime
from dash.dependencies import Output, Input
import dash_core_components as dcc
from dash_core_components.Graph import Graph
import dash_table
import dash_html_components as html
import plotly
import plotly.graph_objs as go
from collections import deque
from apps.wsb import wsb_comment_sentiment, create_wsb_client, wsb_get_comments, get_comments_table
from apps.gme_data import gme_stock_price
from database import Db
import threading
import pandas as pd

wsb = create_wsb_client()

df = pd.DataFrame(columns=[
    'body',
    'polarity',
    'subjectivity',
    'created_at'
])

app = dash.Dash(__name__)
app.layout = html.Div(children=[
    html.Div(children=[
        html.Div([
            html.H3('WSB Daily Discussion SA'),
            html.Div(id='live-update-text'),
            dcc.Graph(id='live-graph', animate=True),
            dcc.Interval(
                id='graph-update',
                interval=60*1000
            ),
        ],  style={'width': '50%', 'display': 'inline-block'}),
        html.Div([
            html.H3('Comentários'),
            html.Div(id='comments-table-live'),
            dash_table.DataTable(
                id='comments-table',
                columns=[
                    {
                        "name":i, "id":i
                    }
                    for i in df.columns
                ],
                data=df.to_dict('records'),
                style_data={'whiteSpace': 'normal', 'height': 'auto'},
                style_cell={'maxWidth': '500px', 'fontSize':9, 'textAlign':'left'},
                style_table={'height':500,'overflowY':'scroll'}
            ),
            dcc.Interval(
                id='table-update',
                interval=60*1000
            )
        ], style={'width': '50%', 'display': 'inline-block'})
    ]),
    html.Div(children=[
        html.H4('GME Stock Price'),
        html.Div(id='gme-stock-price'),
        dcc.Graph(id='gme-stock-graph', animate=True),
        dcc.Interval(
            id='gme-update',
            interval=60*1000
        )
    ])]
)

db_wsb = Db()

thread_wsb = threading.Thread(target=wsb_comment_sentiment, args=(wsb, db_wsb))
thread_wsb.start()


db = Db()

@app.callback(Output('comments-table', 'data'),
              [Input('table-update', 'n_intervals')])
def update_comments_table(input_data):

    df = get_comments_table(db)
    return df.to_dict(orient='records')


@app.callback(Output('gme-stock-graph', 'figure'),
              [Input('gme-update', 'n_intervals')])
def update_gme(input_data):
    stock_df = gme_stock_price()

    data = plotly.graph_objs.Candlestick(
        x=stock_df['Datetime'],
        open=stock_df['Open'],
        high=stock_df['High'],
        low=stock_df['Low'],
        close=stock_df['Close'],
        name='Scatter'
    )

    return {'data': [data],'layout' : go.Layout(xaxis=dict(range=[min(stock_df['Datetime']),max(stock_df['Datetime'])]))}

X_wsb = deque(maxlen=20)
Y_wsb = deque(maxlen=20)
@app.callback(Output('live-graph', 'figure'),
              [Input('graph-update', 'n_intervals')])

def update_graph_scatter(input_data):

    wsb_get_comments(db, X_wsb,Y_wsb)

    data = plotly.graph_objs.Scatter(
            x=list(X_wsb),
            y=list(Y_wsb),
            name='Scatter',
            mode= 'lines+markers'
            )

    return {'data': [data],'layout' : go.Layout(xaxis=dict(range=[min(X_wsb),max(X_wsb)]),
                                                yaxis=dict(range=[min(Y_wsb),max(Y_wsb)]),)}

if __name__ == '__main__':
    app.run_server(host='0.0.0.0', port=8080 ,debug=True)
