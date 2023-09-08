import os
import json

from dash import dcc, html, Input, Output, State, Dash
from dash_extensions.enrich import DashProxy, NoOutputTransform, TriggerTransform, Trigger
import dash_bootstrap_components as dbc
from flask import session
from app import app

from iv.game import TheGame, game_decoder
from iv.player import Player, player_decoder

start_card = dbc.Card(
    dbc.CardBody(
        [
            html.H1("Start a game", className="card-title"),
            html.P("Brace yourself, brave adventurers, for this game demands cunning, courage, and a heart unyielding to challenges. Do you dare to embark on this epic journey of conquest?"),
            html.Hr(),
            dbc.Row([
                dbc.Col(
                    dbc.Button(id="create", children="Create a game", color="danger" ,className="btn-lg col-12"),
                    width = 6,
                    className = "text-center"
                ),
                dbc.Col(
                    dbc.Button(id="load", children="Load a game", color="success", className="btn-lg col-12"),
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
            [
                start_card,
                html.Div(id="config"),
                html.Div(id="load-container")
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
    Output('load-container', 'children'),
    Input('load', 'n_clicks'),
    prevent_initial_call=True
)
def load_game_container(n_clicks):

    options = [
        {
            "label" : item + " | saved at: " + json.load(open(os.path.join(os.path.abspath("."),"games",item,"game.json")))["latest_save_time"],
            "value": os.path.join(os.path.abspath("."),"games",item,"game.json")
        }
        for item in os.listdir("./games/") if os.path.isdir(os.path.join(os.path.abspath("."),"games",item))
        ]
    
    load_container = dbc.Card(
        dbc.CardBody(
            [
                dbc.Row(
                    dbc.Col(
                        [
                            dbc.Label("Choose one game to load"),
                            dbc.RadioItems(
                                options=options,
                                id="load-games-input",
                            ),
                        ],
                        width=12
                    )
                ),
                html.Hr(id="load-hr"),
                dbc.Button(id="load-game", children="Load Selected Game", href="/game", color="success", className="d-grid gap-2 mx-auto"),
            ]
        ),
        style = {
            "margin-top" : "20px"
        }
    )

    return load_container

@app.callback(
    Output('load-hr', 'children'),
    Input('load-game', 'n_clicks'),
    State('load-games-input', 'value'),
    prevent_initial_call=True
)
def load_game(n_clicks, path):
    session["game"] = json.load(open(path))
    return None

#################################
######### Create a Game #########
#################################
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
                    dbc.Alert(
                        id="alert-create",
                        is_open=False,
                        duration=4000,
                    ),
                ]
            ),
            html.Div(id = "game-details"),
            
        ],
        style = {
            "margin-top" : "30px"
        }
    )
    
    return res

@app.callback(
    Output('game-details', 'children'),
    Output('game-name-inp', 'disabled '),
    Output('alert-create', 'is_open'),
    Output('alert-create', 'children'),
    Input('submit-game-btn', 'n_clicks'),
    State('game-name-inp', 'value'),
    prevent_initial_call=True
    )
def game_name_set(n_clicks, game_name):

    try:

        game = TheGame(name = game_name)
        session["game"] = game.serialize()
        print(json.dumps(session["game"], indent=2))

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
                html.Div(id="players-container", style={"margin-top" : "10px"}),
                html.Hr(),
                html.Div(
                    [   
                        html.P("Gain from mines per round"),
                        dbc.InputGroup(
                            [
                                dbc.Input(id="coal-gain-inp", type="number", placeholder="Mine Gain"),
                                dbc.Button("Submit", id="coal-btn", n_clicks=0),
                            ]
                        ),
                        dbc.FormText(id="gain-mess", children = "Gain has not set.")
                    ]
                ),
                html.Div(
                    [
                        html.P("Gain from factories per round"),
                        dbc.InputGroup(
                            [
                                dbc.Input(id="factory-gain-inp", type="number", placeholder="Factory Gain"),
                                dbc.Button("Submit", id="factory-btn", n_clicks=0),
                            ]
                        ),
                        dbc.FormText(id="factory-mess", children = "Gain has not set."),
                    ]
                ),
                html.Div(
                    [
                        html.P("Gain from central per round"),
                        dbc.InputGroup(
                            [
                                dbc.Input(id="central-gain-inp", type="number", placeholder="Central Gain"),
                                dbc.Button("Submit", id="central-btn", n_clicks=0),
                            ]
                        ),
                        dbc.FormText(id="central-mess", children = "Gain has not set."),
                    ]
                ),
                html.Div(
                    [
                        html.P("Gain from capital per round"),
                        dbc.InputGroup(
                            [
                                dbc.Input(id="capital-gain-inp", type="number", placeholder="Capital Gain"),
                                dbc.Button("Submit", id="capital-btn", n_clicks=0),
                            ]
                        ),
                        dbc.FormText(id="capital-mess", children = "Gain has not set."),
                    ]
                ),
                html.Div(
                    [
                        html.P("Gain from empire per round"),
                        dbc.InputGroup(
                            [
                                dbc.Input(id="empire-gain-inp", type="number", placeholder="Empire Gain"),
                                dbc.Button("Submit", id="empire-btn", n_clicks=0),
                            ]
                        ),
                        dbc.FormText(id="empire-mess", children = "Gain has not set."),
                    ]
                ),
                html.Hr(),
                dbc.Button(id="start-game", children="Start Game", color="danger", href="/game", disabled=True, className="d-grid gap-2 mx-auto"),
            ],
            style = {"margin-top" : "30px"}
        )

        return res, True, True, "Your game has been created. Please configure it now."
    except:
        return None, False, True, "An error occured. Try again."

@app.callback(
    Output('players-container', 'children'),
    Output('submit-player-inp', 'value'),
    Input('submit-player-btn', 'n_clicks'),
    State('submit-player-inp', 'value'),
    prevent_initial_call=True
    )
def game_name_set(n_clicks, player_name):

    game = game_decoder(session["game"])
    game.add_player(player_name)

    table = dbc.Table.from_dataframe(game.get_players_dataframe(), striped=True, bordered=True, hover=True)
    
    session["game"] = game.serialize()

    return [table], ""


@app.callback(
    Output('gain-mess', 'children'),
    Input('coal-btn', 'n_clicks'),
    State('coal-gain-inp', 'value'),
    prevent_initial_call=True
    )
def coal_btn(n_clicks, gain):

    game = game_decoder(session["game"])
    game.set_coal_gain(gain)
    session["game"] = game.serialize()

    return f"Coal gain has been set to {gain}"


@app.callback(
    Output('factory-mess', 'children'),
    Input('factory-btn', 'n_clicks'),
    State('factory-gain-inp', 'value'),
    prevent_initial_call=True
    )
def factory_btn(n_clicks, gain):

    game = game_decoder(session["game"])
    game.set_factory_gain(gain)
    session["game"] = game.serialize()

    return f"Factory gain has been set to {gain}"

@app.callback(
    Output('central-mess', 'children'),
    Input('central-btn', 'n_clicks'),
    State('central-gain-inp', 'value'),
    prevent_initial_call=True
    )
def central_btn(n_clicks, gain):

    game = game_decoder(session["game"])
    game.set_central_gain(gain)
    session["game"] = game.serialize()

    return f"Central gain has been set to {gain}"

@app.callback(
    Output('capital-mess', 'children'),
    Input('capital-btn', 'n_clicks'),
    State('capital-gain-inp', 'value'),
    prevent_initial_call=True
    )
def empire_btn(n_clicks, gain):

    game = game_decoder(session["game"])
    game.set_capital_gain(gain)
    session["game"] = game.serialize()

    return f"Capital gain has been set to {gain}"

@app.callback(
    Output('empire-mess', 'children'),
    Input('empire-btn', 'n_clicks'),
    State('empire-gain-inp', 'value'),
    prevent_initial_call=True
    )
def empire_btn(n_clicks, gain):

    game = game_decoder(session["game"])
    game.set_empire_gain(gain)
    session["game"] = game.serialize()

    return f"Empire gain has been set to {gain}"


@app.callback(
    Output('start-game','disabled'),
    [
        Input('submit-player-btn', 'n_clicks'),
        Input('coal-btn', 'n_clicks'),
        Input('factory-btn', 'n_clicks')
    ]
    )
def game_start(player_clicks, coal_clicks, factory_clicks):

    game = game_decoder(session["game"])

    print("Can game start:", game.can_game_start())

    if game.can_game_start():
        return False
    else:
        return True

@app.callback(
    Input("start-game", "n_clicks")
)
def start(n_clicks):
    game = game_decoder(session["game"])
    game.add_bot("The Game")
    game.start_game()
    session["game"] = game.serialize()
    return None