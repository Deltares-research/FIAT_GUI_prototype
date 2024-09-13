"""The app."""

import dash_bootstrap_components as dbc
from dash import Dash

from FIAT_GUI.callbacks import *  # noqa: F403
from FIAT_GUI.layout import layout

app = Dash(
    "FIAT GUI",
    title="FIAT GUI",
    external_stylesheets=[
        dbc.themes.BOOTSTRAP,
        dbc.icons.BOOTSTRAP,
    ],
)

app.layout = layout

if __name__ == "__main__":
    app.run_server(debug=True)
