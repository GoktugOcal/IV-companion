from dash import dcc, html, Input, Output, State, Dash
import dash_bootstrap_components as dbc
from flask import session
from app import app

from iv.game import TheGame
from iv.player import Player

start_card = dbc.Card(
    dbc.CardBody(
        [
            html.H1("Start a game", className="card-title"),
            dbc.Row([
                dbc.Col(
                    dbc.Button(id="create", children="Create", color="danger" ,className="d-grid gap-2 mx-auto"),
                    width = 6,
                    className = "text-center"
                ),
                dbc.Col(
                    dbc.Button(id="load", children="Load", color="primary", className="d-grid gap-2 mx-auto"),
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
        dbc.Col(
            [html.Div(
                [
                    start_card
                ],
            ),
            html.Div(id="config")
            ],
            className="col-10 col-lg-4"
        ),
        dbc.Col(className="col-1 col-lg-4")
    ],
    style={
        "padding-top" : "10vh"
    })

])


@app.callback(
    Output('config', 'children'),
    Input('create', 'n_clicks'),
    prevent_initial_call=True
    )
def create_game(n_clicks):

    res = html.Div(
        [
            html.H3("Configure the game."),
            html.P("Enter the game name"),
            dbc.InputGroup(
                [
                    dbc.Input(id="game-name-inp", placeholder="Game Name"),
                    dbc.Button("Submit", id="submit-game-btn", n_clicks=0),
                ]
            ),
            html.Div(id = "game-details")
        ],
        style = {
            "margin-top" : "30px"
        }
    )
    
    return res

@app.callback(
    Output('game-details', 'children'),
    Output('game-name-inp', 'disabled '),
    Input('submit-game-btn', 'n_clicks'),
    State('game-name-inp', 'value'),
    prevent_initial_call=True
    )
def game_name_set(n_clicks, game_name):

    print(game_name)
    game = TheGame(name = game_name)
    session["game"] = game

    res = html.Div(
        [
            html.H3("Game details."),
            html.P("Submit players"),
            dbc.InputGroup(
                [
                    dbc.Input(id="submit-player-inp", placeholder="Player's Name"),
                    dbc.Button("Submit", id="submit-player-btn", n_clicks=0),
                ]
            ),
            html.Div(id="players-container")
        ],
        style = {"margin-top" : "30px"}
    )

    return res, True

@app.callback(
    Output('players-container', 'children'),
    Input('submit-player-btn', 'n_clicks'),
    State('submit-player-inp', 'value'),
    prevent_initial_call=True
    )
def game_name_set(n_clicks, player_name):
    

    session["game"].add_player(player_name)
    session["game"].show_players()
    
    return None