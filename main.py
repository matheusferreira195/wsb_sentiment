
import dash
import datetime
from dash.dependencies import Output, Input
import dash_core_components as dcc
import dash_html_components as html
import plotly
import plotly.graph_objs as go
from collections import deque
from apps.wsb import wsb_comment_sentiment, create_wsb_client, wsb_get_comments
from apps.gme_data import gme_stock_price
from database import Db
import threading

wsb = create_wsb_client()

app = dash.Dash(__name__)
app.layout = html.Div(
    html.Div([
        html.H4('WSB Daily Discussion SA'),
        html.Div(id='live-update-text'),
        dcc.Graph(id='live-graph', animate=True),
        dcc.Interval(
            id='graph-update',
            interval=60*1000
        ),
    ]),
    html.Div([
        html.H4('GME Stock Price'),
        html.Div(id='gme-stock-price'),
        dcc.Graph(id='gme-stock-graph', animate=True),
        dcc.Interval(
            id='gme-update',
            interval=60*1000
        )
    ])
)

db_wsb = Db()

thread_wsb = threading.Thread(target=wsb_comment_sentiment, args=(wsb, db_wsb))
thread_wsb.start()

X_gme = deque(maxlen=20)
Y_gme = deque(maxlen=20)
db = Db()

@app.callback(Output('gme-stock-graph', 'figure'),
              [Input('gme-update', 'n_intervals')])
def update_gme():
    gme_stock_price(X_gme,Y_gme)

    data = plotly.graph_objs.Scatter(
            x=list(X_gme),
            y=list(Y_gme),
            name='Scatter',
            mode= 'lines+markers'
            )

    return {'data': [data],'layout' : go.Layout(xaxis=dict(range=[min(X_gme),max(X_gme)]),
                                                yaxis=dict(range=[min(Y_gme),max(Y_gme)]),)}


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
