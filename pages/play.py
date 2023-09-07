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

NUM_COLS = ["money", "mines", "factories", "price"]

# def refresh(game: TheGame):

#     # table = dbc.Table.from_dataframe(game.get_players_dataframe(), striped=True, bordered=True, hover=True)
#     df = game.get_players_dataframe()
#     table = dash_table.DataTable(
#         id = "theTable",
#         columns = [{'name':col, 'id':col, 'editable': True} if col != "pid" else {'name':col, 'id':col, 'editable':False, 'type': 'numeric'} for col in df.columns],
#         data = df.to_dict(orient='records'),
#         # editable=True
#     )

#     market_df = df.from_dict(game_decoder(session["game"]).market)

#     market_table = dash_table.DataTable(
#         id="market-table",
#         columns = [{'name':col, 'id':col} for col in market_df],
#         data = market_df.to_dict(orient='records'),
#         row_selectable='single'
#     )

#     return html.Div([
#         table,
#         dbc.Alert("Saved.", id="saved-alert", is_open=False, dismissable=True),
#         market_table
#     ])


modal_1 = dbc.Modal(
    [
        dbc.ModalHeader(dbc.ModalTitle("Attack"), close_button=True),
        dbc.ModalBody(id="modal-body"),
    ],
    id="modal-1",
    centered=True,
    is_open=False,
)

# modal_1 = dbc.Modal(
#     [
#         dbc.ModalHeader(dbc.ModalTitle("Attack"), close_button=True),
#         dbc.ModalBody(id="modal-body"),
#     ],
#     id="modal-1",
#     centered=True,
#     is_open=False,
# )

# attack_collapse  =dbc.Collapse(
#     dbc.Card(dbc.CardBody(id="attack-card")),
#     id="attack-collapse",
#     is_open=False,
# )



round_list = dbc.ListGroup(
    id = "player-list",
    horizontal=True,
    className="mb-2",
)

next_round_button = dbc.Button(id="next-player", children="Next Player!", color="success", className="btn-md d-grid gap-2 btn-block", style={"margin-top" : "5px", "margin-bottom" : "5px", "margin-left": "auto"})
buy_button = dbc.Button(id="buy-button", children="Buy!", className="btn-md d-grid gap-2 btn-block", style={"margin-top" : "5px", "margin-bottom" : "5px"})
three_big_button = dbc.Button(id="three-button", children="Play Three Big!!", className="btn-md d-grid gap-2 btn-block", style={"margin-top" : "5px", "margin-bottom" : "5px"})

# Attack Buttons
attack_button = dbc.Button(id="attack-button", children="Attack ⚔️", className="btn-md d-grid gap-2 btn-block", style={"margin-top" : "5px", "margin-bottom" : "5px"})
final_attack_button = dbc.Button(id="final-attack-button", children="Attack ⚔️", color="danger", className="btn-md d-grid gap-2 btn-block", style={"margin-top" : "5px", "margin-bottom" : "5px"})
attack_win = dbc.Button(id="attack-win-btn", children="Win 🏆", color="success", className="btn-md d-grid gap-2 btn-block", style={"margin-top" : "5px", "margin-bottom" : "5px"})
attack_lose = dbc.Button(id = "attack-lose-btn", children="Lose 😭", className="btn-md d-grid gap-2 btn-block", style={"margin-top" : "5px", "margin-bottom" : "5px"})

transfer_button = dbc.Button(id="transfer-button", children="Transfer Money 💸", className="btn-md d-grid gap-2 btn-block", style={"margin-top" : "5px", "margin-bottom" : "5px"})

saved_alert = dbc.Alert("Saved.", id="saved-alert", is_open=False, dismissable=True)
welcome_alert = dbc.Alert("Welcome!", is_open=True)

round_list_container = dbc.Row([dbc.Col(round_list), dbc.Col(next_round_button)])

layout = html.Div([
    html.Div(id='dummy-div'),  # Dummy input
    html.Div(id='alert-container', children=[welcome_alert]),
    dbc.Row(
        [
            dbc.Col([round_list_container, dash_table.DataTable(id = "the-table"), saved_alert, three_big_button, attack_button], className="col-12 col-lg-7"),
            dbc.Col([html.Div()], className="col-12 col-lg-1"),
            dbc.Col([buy_button, dash_table.DataTable(id = "market-table", row_selectable='single')], className="col-12 col-lg-4")
        ]
    ),
    modal_1
])

@app.callback(
    Output("the-table", "columns"),
    Output("the-table", "data"),
    Input("dummy-div","children")
)
def table_update(dummy):
    game = game_decoder(session["game"])
    df = game.get_players_dataframe()

    cols = []
    for col in df.columns:
        if "pid" not in col:
            if col in NUM_COLS: cols.append({'name':col, 'id':col, 'editable': True, 'type' : 'numeric'})
            else: cols.append({'name':col, 'id':col, 'editable': True})
        else:
            cols.append({'name':col, 'id':col, 'editable':False, 'type': 'numeric'})

    data = df.to_dict(orient='records')
    return cols, data

@app.callback(
    Output("market-table", "columns"),
    Output("market-table", "data"),
    Input("dummy-div","children")
)
def market_update(dummy):
    game = game_decoder(session["game"])
    df = pd.DataFrame(game.market)
    cols = [{'name':col, 'id':col} for col in df]
    data = df.to_dict(orient='records')
    return cols, data

@app.callback(
    Output("player-list", "children"),
    Input("dummy-div","children")
)
def list_update(dummy):
    game = game_decoder(session["game"])
    list_grp = [dbc.ListGroupItem(player.name, active=True) if game.round_player_pid == player.pid else dbc.ListGroupItem(player.name) for player in game.players.values()]
    return list_grp

@app.callback(
    Output("dummy-div","children", allow_duplicate=True),
    Input("next-player", "n_clicks"),
    prevent_initial_call=True
)
def next_player(n_clicks):
    print("next triggered.")
    game = game_decoder(session["game"])
    game.go_to_next_player()
    session["game"] = game.serialize()

    return "Update"

@app.callback(
    Output("alert-container","children", allow_duplicate=True),
    Output("dummy-div","children", allow_duplicate=True),
    Input("three-button","n_clicks"),
    prevent_initial_call=True
)
def three_big(n_clicks):

    game = game_decoder(session["game"])

    if game.round_player.three_big_used:
        return dbc.Alert("Three Big is used. Can not use it right now.", color='danger'), "Three Big"
    else:
        game.round_player.three_big(game,"Win")
        session["game"] = game.serialize()
        return dbc.Alert("Three Big is used successfully"), "Three Big"

@app.callback(
    Output("alert-container","children", allow_duplicate=True),
    Output("modal-1","is_open"),
    Output("modal-body","children", allow_duplicate=True),
    Input("attack-button","n_clicks"),
    State("modal-1","is_open"),
    prevent_initial_call=True
)
def attack(n_clicks, is_open):
    game = game_decoder(session["game"])

    body = [
        dbc.InputGroup([
            dbc.InputGroupText("Target 🎯"),
            dbc.Select(
                id="attack-target-select",
                options=[{"label": v.name, "value": k} for k, v in game.players.items()],
            )
        ]),
        final_attack_button
    ]

    return dbc.Alert("Attacking", color='danger'), not is_open, body

@app.callback(
    Output("modal-body","children", allow_duplicate=True),
    Input("final-attack-button","n_clicks"),
    prevent_initial_call=True
)
def attack_final(n_clicks):
    game = game_decoder(session["game"])

    body = [
        dbc.Row(
            [
                dbc.Col(attack_win),
                dbc.Col(attack_lose)
            ]
        )
    ]

    return body



@app.callback(
    Output("alert-container","children", allow_duplicate=True),
    Input("attack-modal-button","n_clicks"),
    prevent_initial_call=True
)
def attack(n_clicks):
    return dbc.Alert("Attacking", color='danger'), Tr







@app.callback(
    Output('saved-alert', 'is_open'),
    [
        Input('the-table', 'data'),
        Input('the-table', 'columns')
    ],
    prevent_initial_call=True
)
def update_game_from_table(rows, columns):

    df = pd.DataFrame(rows, columns=[c['name'] for c in columns])
    game = game_decoder(session["game"])

    for item in df.to_dict(orient="records"):
        player = game.get_player_by_pid(item["pid"])
        for k in item.keys():
            setattr(player, k, item[k])
    
    session["game"] = game.serialize()

    return True


@app.callback(
    Input('market-table', 'selected_rows'),
    prevent_initial_call=True
)
def market_select(ids):
    print(ids)