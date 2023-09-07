from dash import dcc, html, Input, Output, State, Dash, register_page
import dash_bootstrap_components as dbc
from flask import session
from app import app

from iv.game import TheGame
from iv.player import Player

register_page(__name__, name="Welcome")

welcome_card = dbc.Card(
    dbc.CardBody(
        [
            html.H1("Welcome to İŞGAL VAKTİ", className="card-title"),
            html.P("Around our table, an intricate realm takes shape as we forge our own world. Through battles and alliances, we compete for supremacy, capturing coal mines and factories to amass wealth. Yet, amid this empire-building, a bustling market tempts us with powerful artifacts and map-enhancing cosmetics. In this enduring saga, we shape our destinies, seeking victory not only in territory but in the artistry of our conquests, a tapestry of strategy and friendship illuminated by a flickering candle's soft glow."),
            dbc.Row([
                dbc.Col(
                    dbc.Button(id="play", children="Play the game", color="danger", href="/start_game", className="btn-lg d-grid gap-2"),
                    width = 6,
                    className = "text-center "
                ),
                dbc.Col(
                    dbc.Button(id="watch", children="Watch a game", color="primary", href="/watch_game", className="btn-lg d-grid gap-2"),
                    width = 6,
                    className = "text-center"
                )
            ])
            
        ],
        className = "text-center"
    )
)

layout = html.Div([
    dbc.Row([
        dbc.Col(className="col-1 col-lg-4"),
        dbc.Col(welcome_card, className="col-10 col-lg-4"),
        dbc.Col(className="col-1 col-lg-4")
    ],
    style={
        "padding-top" : "10vh"
    })
])

@app.callback(
    Output('play', 'children'),
    Input('play', 'n_clicks'),
    prevent_initial_call=True
)
def play_clicked(n_clicks):

    session["type"] = "play"
    print(session["type"])

    return None

@app.callback(
    Output('watch', 'children'),
    Input('watch', 'n_clicks'),
    prevent_initial_call=True
)
def watch_clicked(n_clicks):

    session["type"] = "watch"
    print(session["type"])

    return None