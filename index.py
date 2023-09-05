from dash import dcc, html, Input, Output, State, Dash, callback
import dash_bootstrap_components as dbc

from app import app
from pages import welcome, start_game, watch_game, setup, play
from iv.game import TheGame
from iv.player import Player

app.layout = html.Div([
    dcc.Location(id = "url"),
    html.Div(id='page-content')
])


@app.callback(Output('page-content', 'children'),
              Input('url', 'pathname'))
def display_page(pathname):
    if pathname == "/":
        return welcome.layout
    elif pathname == '/start_game':
        return start_game.layout
    elif pathname == '/watch_game':
        return watch_game.layout
    elif pathname == '/setup':
        return setup.layout
    elif pathname == '/game':
        return play.layout
    else:
        return '404'

if __name__ == '__main__':
    app.run(debug=True)