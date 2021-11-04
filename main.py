import dash
from dash import dcc
from dash import html
from dash.dependencies import Output, Input
import plotly.express as px
import dash_bootstrap_components as dbc
import pandas as pd
import pandas_datareader.data as web
import datetime

# start=datetime.datetime(2020,7,31)
# end=datetime.datetime(2021,7,31)
# df=web.DataReader(['AMZN','GOOGLE','FB','MSFT','NFLX','TSLA'],
#                   'yahoo', start=start, end=end)
# df=df.stack().reset_index()
# print(df.head(30))
# df.to_csv("stocks.csv", index=False)

df=pd.read_csv('stocks.csv')
print(df)
app=dash.Dash(__name__,external_stylesheets=[dbc.themes.PULSE],
              meta_tags=[{'name': 'viewport',
                          'content': 'width=device-width, initial-scale=1.0'}]
              )
#LAYOUT _____________________________
app.layout=dbc.Container([
    dbc.Row([
    dbc.Col(html.H1("Stock Market Dashboard",
                    className='text-center bg-warning text-white mb-4'),
            width=12)
    ]),
    dbc.Row([
        dbc.Col([
            dcc.Dropdown(id='mydrop', multi=False,
                         value='AMZN',
                         options=[{'label':x,'value':x}
                         for x in sorted(df['Symbols'].unique())]),
            dcc.Graph(id='linefig', figure={})
        ], #width={'size':6, 'offset':0, 'order':1},
            xs=12, sm=12, md=12, lg=6, xl=6
        ),
        dbc.Col([
            dcc.Dropdown(id='mydrop2', multi=True, value=['AMZN', 'FB'],
                         options=[{'label': x, 'value': x}
                                  for x in sorted(df['Symbols'].unique())],
                         ),
            dcc.Graph(id='linefig2', figure={})
        ], #width={'size':6, 'offset':0, 'order':2},
            xs=12, sm=12, md=12, lg=6, xl=6

        )

    ], className="g-0", justify='around'),
    dbc.Row([
        dbc.Col([
            html.P("Select the Stock",
                   style={'textDecoration':'underline'}),
            dcc.Checklist(id='mycheck',
                          value=['FB','TSLA','AMZN'],
                          options=[{'label': x, 'value': x}
                                   for x in sorted(df['Symbols'].unique())],
                          labelClassName='m-3 text-warning'),
            dcc.Graph(id='myhist', figure={})

        ], #width={'size':6}
            xs=12, sm=12, md=12, lg=6, xl=6
            ),

        dbc.Col([
         dbc.Card(
                [
                    dbc.CardBody(
                        html.P(
                            '"I will tell you how to become rich. Close the doors. Be fearful when others are greedy. Be greedy when others are fearful." — Warren Buffett',
                            className="card-text")
                    ),
                    dbc.CardImg(
                        src="https://media.giphy.com/media/JtBZm3Getg3dqxK0zP/giphy-downsized-large.gif",
                        bottom=True),
                ],
                style={"width": "24rem"},
                )
                ], width={'size':6}

        )
    ], align='center')

], fluid=True)

#--------CALLBACKS
@app.callback(
    Output('linefig', 'figure'),
    Input('mydrop', 'value')
)
def update_graph(stock_slctd):
    dff = df[df['Symbols']==stock_slctd]
    figln = px.line(dff, x='Date', y='High')
    return figln


# Line chart - multiple
@app.callback(
    Output('linefig2', 'figure'),
    Input('mydrop2', 'value')
)
def update_graph(stock_slctd):
    dff = df[df['Symbols'].isin(stock_slctd)]
    figln2 = px.line(dff, x='Date', y='Open', color='Symbols')
    return figln2


# Histogram
@app.callback(
    Output('myhist', 'figure'),
    Input('mycheck', 'value')
)
def update_graph(stock_slctd):
    dff = df[df['Symbols'].isin(stock_slctd)]
    dff = dff[dff['Date']=='2021-07-01']
    fighist = px.histogram(dff, x='Symbols', y='Close')
    return fighist

if __name__=='__main__':
    app.run_server(debug=True, port=3000)