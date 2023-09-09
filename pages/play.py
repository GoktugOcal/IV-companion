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

NUM_COLS = ["money", "mines", "factories", "price", "navy"]

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





round_list = dbc.ListGroup(
    id = "player-list",
    horizontal=True,
    className="mb-2",
)

next_round_button = dbc.Button(id="next-player", children="Next Player!", color="success", className="btn-md d-grid gap-2 btn-block", style={"margin-top" : "5px", "margin-bottom" : "5px", "margin-left": "auto"})
buy_button = dbc.Button(id="buy-button", children="Buy!", color="success", className="col-12", style={"margin-top" : "5px", "margin-bottom" : "5px"})



# Attack Buttons
attack_button = dbc.Button(id="attack-button", children="Attack ⚔️", color="danger", className="col-4", style={"margin-top" : "5px", "margin-bottom" : "5px"})
final_attack_button = dbc.Button(id="final-attack-button", children="Attack ⚔️", color="danger", className="btn-md d-grid gap-2 btn-block")
attack_win = dbc.Button(id="attack-win-btn", children="Win 🏆", color="success", className="col-12")
attack_lose = dbc.Button(id = "attack-lose-btn", children="Lose 😭", className="col-12")
# Transfer Buttons
transfer_button = dbc.Button(id="transfer-button", children="Transfer 💸", color="success", className="col-4", style={"margin-top" : "5px", "margin-bottom" : "5px"})
send_button = dbc.Button(id="send-button", children="Send 💸", className="btn-md d-grid gap-2 btn-block")
# Three Big Buttons
three_big_button = dbc.Button(id="three-button", children="Three Big 🍆", color="info", className="col-4", style={"margin-top" : "5px", "margin-bottom" : "5px"})


#Alerts
saved_alert = dbc.Alert("Saved.", id="saved-alert", is_open=False, dismissable=True)
welcome_alert = dbc.Alert("Welcome!", is_open=True, style = {"margin-top" : "10px"})

round_list_container = dbc.Row([dbc.Col(round_list), dbc.Col(next_round_button)])

button_group = dbc.ButtonGroup(
    [
        three_big_button,
        attack_button,
        transfer_button
    ],
    className = "col-12"
)

#######################################################################
############################## Collapses ##############################
#######################################################################

win_lose_collapse = dbc.Collapse(
    children = [
        dbc.Row(
            [
                dbc.Col(attack_win, width=6),
                dbc.Col(attack_lose, width=6),
            ],
        )
    ],
    id = "win-lose-collapse",
    is_open = False,
    style = {"margin-top" : "5px"}
)
attack_collapse = dbc.Collapse(
    children = [
        dbc.InputGroup([
            dbc.Select(id="attack-target-select"),
            final_attack_button
        ]),
        win_lose_collapse
    ],
    id="attack-collapse",
    is_open=False
    # dimension="width"
)


transfer_collape = dbc.Collapse(
    children = [
        dbc.Row(
            [
                dbc.InputGroup([
                    dbc.Select(id="transfer-target-select", placeholder="Select Target"),
                    dbc.Input(id="transfer-amount", placeholder="Transfer Amount", type="number"),
                    send_button
                ]),
            ]
        )
    ],
    id = "transfer-collapse",
    is_open = False
)

start_img = html.Img(src="./assets/img/iv_start.jpg", style={'width':'100%', "margin-bottom":"20px"})
market_img = html.Img(src="./assets/img/iv_market.jpg", style={'width':'100%', "margin-bottom":"20px"})


#######################################################################
################################ Rows #################################
#######################################################################

attack_row = html.Div(
    [
        dbc.Row(
            [
                dbc.Col(attack_button, className="col-4 col-lg-4"),
                dbc.Col(attack_collapse, className="col-8 col-lg-8")
            ],
            className="mx-auto"
        ),
        win_lose_collapse
    ]
)

transfer_row = html.Div(
    [
        dbc.Row(
            [
                dbc.Col(transfer_button, className="col-4 col-lg-4"),
                dbc.Col(transfer_collape, className="col-8 col-lg-8")
            ]
        ),
        win_lose_collapse
    ]
)

button_functions = html.Div(
    [
        button_group,
        attack_collapse,
        transfer_collape
    ]
)


player_table = dash_table.DataTable(id = "the-table", style_table={'overflowX': 'scroll'})

style_data_conditional=[
        {
            'if': {'row_index': 'odd'},
            'backgroundColor': 'rgb(220, 220, 220)',
        }
    ]

##############################
##############################
##############################

button = dbc.Row(
    [
        dbc.Col(dbc.Button("Block button", color="primary", className = "col-12"), width = 6),
        dbc.Col(dbc.Button("Block button", color="secondary", className = "col-12"), width = 6),
    ],
    className="mx-auto",
)

layout = html.Div([
    dbc.Container([

        html.Div(id='dummy-div'),  # Dummy input
        html.Div(id='alert-container', children=[welcome_alert]),
        dbc.Row(
            [
                dbc.Col([start_img, round_list_container, player_table, html.Hr(), saved_alert, button_functions, html.Hr()], className="col-12 col-lg-7"),
                dbc.Col([html.Div()], className="col-12 col-lg-1"),
                dbc.Col([market_img, buy_button, dash_table.DataTable(id = "market-table", row_selectable='single', style_data={'textAlign': 'left'}, style_data_conditional=style_data_conditional)], className="col-12 col-lg-4")
            ]
        ),
        modal_1

    ])
    
])

##############################
##############################
##############################



####################################################################
########################## CALLBACKS ###############################
@app.callback(
    Output("the-table", "columns"),
    Output("the-table", "data"),
    Output("the-table", "style_data_conditional"),
    Input("dummy-div","children")
)
def table_update(dummy):
    game = game_decoder(session["game"])
    game.show_players()
    df = game.get_players_dataframe()[json.load(open("./data/col_order.json"))]

    cols = []
    for col in df.columns:
        if "pid" not in col:
            if col in NUM_COLS: cols.append({'name':col, 'id':col, 'editable': True, 'type' : 'numeric'})
            else: cols.append({'name':col, 'id':col, 'editable': True})
        else:
            cols.append({'name':col, 'id':col, 'editable':False, 'type': 'numeric'})

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

    return cols, data, style_data_conditional

@app.callback(
    Output("market-table", "columns"),
    Output("market-table", "data"),
    Input("dummy-div","children")
)
def market_update(dummy):
    game = game_decoder(session["game"])
    df = pd.DataFrame.from_records(game.serialize()["market"]["items"])[["id", "name", "price"]]
    cols = [{'name':col, 'id':col} for col in df]
    data = df.to_dict(orient='records')
    return cols, data

# @app.callback(
#     Output("player-list", "children"),
#     Input("dummy-div","children")
# )
# def list_update(dummy):
#     game = game_decoder(session["game"])
#     list_grp = [dbc.ListGroupItem(player.name, active=True) if game.round_player_pid == player.pid else dbc.ListGroupItem(player.name) for player in game.players.values()]
#     return list_grp

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

    return None

@app.callback(
    Output("dummy-div","children", allow_duplicate=True),
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

    return None
####################################################################
####################################################################



####################################################################
########################## THREE BIG ###############################
@app.callback(
    Output("alert-container","children", allow_duplicate=True),
    Output("dummy-div","children", allow_duplicate=True),
    Input("three-button","n_clicks"),
    prevent_initial_call=True
)
def three_big(n_clicks):

    game = game_decoder(session["game"])

    if game.round_player.three_big_used:
        return dbc.Alert("Three Big is used. Can not use it right now.", color='danger'), None
    else:
        game.round_player.three_big(game,"Win")
        session["game"] = game.serialize()
        return dbc.Alert("Three Big is used successfully"), None
####################################################################
####################################################################



#################################################################
########################## ATTACK ###############################
@app.callback(
    Output("alert-container","children", allow_duplicate=True),
    Output("attack-collapse","is_open"),
    Output("attack-target-select","options", allow_duplicate=True),
    Input("attack-button","n_clicks"),
    State("attack-collapse","is_open"),
    prevent_initial_call=True
)
def attack(n_clicks, is_open):
    game = game_decoder(session["game"])

    options=[{"label": v.name, "value": int(k)} for k, v in game.players.items() if game.round_player_pid != int(k)]
    bot_options = [{"label": v.name, "value": int(k)} for k, v in game.bots.items()]
    options = options + bot_options
    return dbc.Alert("Attacking", color='danger'), not is_open, options

@app.callback(
    Output("win-lose-collapse","is_open"),
    Input("final-attack-button","n_clicks"),
    prevent_initial_call=True
)
def attack_final(n_clicks):
    return True


@app.callback(
    Output("alert-container","children", allow_duplicate=True),
    Output("attack-collapse","is_open", allow_duplicate=True),
    Output("win-lose-collapse","is_open", allow_duplicate=True),
    [Input("attack-win-btn", "n_clicks"),
    Input("attack-lose-btn", "n_clicks")],
    State("attack-target-select", "value"),
    prevent_initial_call=True
)
def win_lose(win_clicks, lose_clicks, target):
    game = game_decoder(session["game"])
    target_player = {**game.players, **game.bots}[int(target)]

    trigger = callback_context.triggered[0]
    button_name = trigger["prop_id"].split(".")[0]

    if button_name == "attack-win-btn":
        game.round_player.attack(game, target_player, "WIN")
    
    elif button_name == "attack-lose-btn":
        game.round_player.attack(game, target_player, "LOSE")

    session["game"] = game.serialize()


    return dbc.Alert("Status", color='danger'), False, False
##############################################################
##############################################################



################################################################
########################## MONEY ###############################
@app.callback(
    Output("alert-container","children", allow_duplicate=True),
    Output("transfer-collapse","is_open", allow_duplicate=True),
    Output("transfer-target-select","options", allow_duplicate=True),
    Input("transfer-button","n_clicks"),
    State("transfer-collapse","is_open"),
    prevent_initial_call=True
)
def transfer(n_clicks, is_open):
    game = game_decoder(session["game"])

    options=[{"label": v.name, "value": int(k)} for k, v in game.players.items() if game.round_player_pid != int(k)]
    bot_options = [{"label": v.name, "value": int(k)} for k, v in game.bots.items()]
    options = options + bot_options
    return dbc.Alert("Transfering Money", color='success'), not is_open, options

@app.callback(
    Output("alert-container","children", allow_duplicate=True),
    Output("transfer-collapse","is_open", allow_duplicate=True),
    Output("dummy-div","children", allow_duplicate=True),
    Input("send-button","n_clicks"),
    State("transfer-target-select", "value"),
    State("transfer-amount", "value"),
    prevent_initial_call=True
)
def send_money(n_clicks, target, amount):
    game = game_decoder(session["game"])
    target_player = {**game.players, **game.bots}[int(target)]

    try:
        game.round_player.transfer(game, target_player, int(amount))
        session["game"] = game.serialize()
        return dbc.Alert("Successfully transferred", color='success'), False, None
    except Exception as e:
        return dbc.Alert(str(e), color='warning'), False, None
##############################################################
##############################################################



##############################################################
########################## BUY ###############################
@app.callback(
    Output("alert-container","children", allow_duplicate=True),
    Output('market-table', 'selected_rows'),
    Output("dummy-div","children", allow_duplicate=True),
    Input('buy-button','n_clicks'),
    State('market-table', 'selected_rows'),
    prevent_initial_call=True
)
def market_select(n_clicks, ids):
    game = game_decoder(session["game"])

    try:
        item_id = list(game.market.items.values())[ids[0]].id
        game.buy(game.round_player, item_id)
        # game.round_player.buy(game, ids[0])
        session["game"] = game.serialize()
        return dbc.Alert("Successfully bought", color='success'), [], None
    except Exception as e:
        return dbc.Alert(str(e), color='warning'), [], None
##############################################################
##############################################################


