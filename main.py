
import dash
import datetime
from dash.dependencies import Output, Input
import dash_core_components as dcc
import dash_html_components as html
import plotly
import plotly.graph_objs as go
from collections import deque
from apps.wsb import wsb_comment_sentiment, create_wsb_client
from apps.gme_data import gme_stock_price

wsb = create_wsb_client()

app = dash.Dash(__name__)
app.layout = html.Div(
    [
        html.H4('WSB Daily Discussion SA'),
        html.Div(id='live-update-text'),
        dcc.Graph(id='live-graph', animate=True),
        dcc.Interval(
            id='graph-update',
            interval=1*1000
        ),
    ]
)

X = deque(maxlen=20)
Y = deque(maxlen=20)

@app.callback(Output('live-graph', 'figure'),
              [Input('graph-update', 'n_intervals')])
def update_graph_scatter(input_data):

    wsb_comment_sentiment(wsb, X, Y)

    data = plotly.graph_objs.Scatter(
            x=list(X),
            y=list(Y),
            name='Scatter',
            mode= 'lines+markers'
            )

    return {'data': [data],'layout' : go.Layout(xaxis=dict(range=[min(X),max(X)]),
                                                yaxis=dict(range=[-1,1]),)}

if __name__ == '__main__':
    app.run_server(host='0.0.0.0', port=8080 ,debug=True)
