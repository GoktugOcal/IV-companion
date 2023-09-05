import dash
from dash import Dash
import dash_bootstrap_components as dbc
import os
import flask
from flask import session


server = flask.Flask(__name__)
server.secret_key = os.urandom(12).hex()
app = Dash(__name__,
    server = server,
    # url_base_pathname="/goktug/",
    suppress_callback_exceptions=True,
    external_stylesheets=[dbc.themes.BOOTSTRAP]
    )

# server = app.server
