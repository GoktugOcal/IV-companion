import os
import json
import pandas as pd

from dash import dcc, html, Input, Output, State, Dash, callback_context, dash_table, callback
from dash_extensions.enrich import DashProxy, NoOutputTransform, TriggerTransform, Trigger
import dash_bootstrap_components as dbc
from flask import session
from app import app

from iv.game import TheGame, game_decoder
from iv.player import Player, player_decoder


start_img = html.Img(src="./assets/img/iv_start.jpg", style={'width':'100%', "margin-bottom":"20px"})
market_img = html.Img(src="./assets/img/iv_market.jpg", style={'width':'100%', "margin-bottom":"20px"})


layout = dbc.Container([
    dbc.Row(
        [
            dbc.Button(id="refresh", children="Refresh", className="col-11 mx-auto", style={"margin-bottom":"10px"}),
            html.Hr(),
            html.Div(id="watch-dummy"),
            html.Div(id="watch-container")
        ]
        ),
    ],
    className="col-12 col-lg-4",
    style={
        "padding-top" : "10vh"
    })

@app.callback(
    Output('watch-container', 'children', allow_duplicate=True),
    Input('watch-dummy', 'id'),
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
                                id="watch-games-input",
                            ),
                        ],
                        width=12
                    )
                ),
                html.Hr(id="load-hr"),
                dbc.Button(id="watch-game", children="Load Selected Game", color="success", className="d-grid gap-2 mx-auto"),
            ]
        ),
        style = {
            "margin-top" : "20px"
        }
    )

    return load_container


@app.callback(
    Output('watch-container', 'children', allow_duplicate=True),
    Input('watch-game', 'n_clicks'),
    State('watch-games-input', 'value'),
    prevent_initial_call = True
)
def load_game(n_clicks, path):
    session["game"] = json.load(open(path))
    session["path"] = path
    game = game_decoder(session["game"])


    return html.Div(
        [   
            start_img,
            html.H1("Player Table"),
            render_player_table(game),
            html.Hr(),
            market_img,
            html.H2("Market"),
            render_market_table(game),
        ]
    )

@app.callback(
    Output('watch-container', 'children', allow_duplicate=True),
    Input('refresh', 'n_clicks'),
    prevent_initial_call = True
)
def refresh(n_clicks):
    session["game"] = json.load(open(session["path"]))
    game = game_decoder(session["game"])

    return html.Div(
        [   
            start_img,
            html.H1("Player Table"),
            render_player_table(game),
            html.Hr(),
            market_img,
            html.H2("Market"),
            render_market_table(game),
        ]
    )

def render_player_table(game):

    df = game.get_players_dataframe()[json.load(open("./data/col_order.json"))]
    cols = [{'name':col, 'id':col} for col in df]
    data = df.to_dict(orient='records')

    style_data_conditional=[
        {
            'if': {
                'filter_query': '{{pid}} = {}'.format(game.round_player_pid),
            },
            'backgroundColor': '#FF4136',
            'color': 'white'
        },
    ]

    return dash_table.DataTable(
        data=data,
        columns=cols,
        style_table={'overflowX': 'scroll'},
        style_data_conditional=style_data_conditional)

def render_market_table(game):

    df = pd.DataFrame.from_records(game.serialize()["market"]["items"])[["id", "name", "price", "requirement"]]
    cols = [{'name':col, 'id':col} for col in df]
    data = df.to_dict(orient='records')
    return dash_table.DataTable(
        data=data,
        columns=cols)