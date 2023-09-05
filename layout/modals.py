import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd

login_modal = dbc.Modal(
    [
        dbc.ModalHeader(dbc.ModalTitle("Header"), close_button=True),
        dbc.ModalBody("This modal is vertically centered"),
        dbc.ModalFooter(
            dbc.Button(
                "Close",
                id="close-centered",
                className="ms-auto",
                n_clicks=0,
            )
        ),
    ],
    id="modal-centered",
    centered=True,
    is_open=False,
)
