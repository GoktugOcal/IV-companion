import dash
from dash import Dash
import dash_bootstrap_components as dbc
import os
import flask
from flask import session

from dash_extensions.enrich import DashProxy, NoOutputTransform, TriggerTransform


server = flask.Flask(__name__)
server.secret_key = os.urandom(12).hex()
app = DashProxy(__name__,
    server = server,
    # url_base_pathname="/goktug/",
    suppress_callback_exceptions=True,
    external_stylesheets=[dbc.themes.FLATLY],
    transforms = [
        NoOutputTransform()
    ]
    )
app.title = "Isgal Vakti"

# server = app.server
