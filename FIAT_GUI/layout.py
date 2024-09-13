"""Module containing the layout of the app."""

import dash_bootstrap_components as dbc
from dash import html

FONT_COLOR = "#080C80"

nav_bar = dbc.Navbar(
    [
        dbc.Row(
            [
                dbc.Col(
                    dbc.NavbarBrand(
                        "FIAT GUI",
                        style={"paddingLeft": "1rem", "color": FONT_COLOR, "fontWeight": "bold", "fontSize": "2.5em"},
                    ),
                    width=4,
                ),
                dbc.Col(
                    dbc.Button(
                        "Help",
                        id="help-button",
                        style={
                            "float": "right",
                            "backgroundColor": "white",
                            "borderColor": FONT_COLOR,
                            "color": FONT_COLOR,
                        },
                        outline=True,
                        className="me-1",
                    ),
                    width=4,
                ),
            ],
            justify="between",
            style={
                "width": "100%",
                "display": "flex",
                "alignItems": "center",
            },
        ),
    ],
    color="white",
    dark=True,
    expand="lg",
    style={
        "boxShadow": "0 4px 8px 0 rgba(0, 0, 0, 0.2), 0 6px 20px 0 rgb(0 0 0 / 19%)",
        "padding": "1rem",
        "width": "100%",
        "maxWidth": "100%",
    },
)

output = dbc.Form(
    [
        dbc.Row(
            [
                dbc.Label("Path", html_for="model-output-path", width=2),
                dbc.Col(dbc.Input(id="model-output-path", type="text", placeholder="Enter output path"), width=10),
            ],
            className="mb-3",
        ),
        dbc.Row(
            [
                dbc.Label("Output CSV", html_for="model-output-csv", width=2),
                dbc.Col(
                    dbc.Input(id="model-output-csv", type="text", placeholder="Enter output CSV path (optional)"),
                    width=10,
                ),
            ],
            className="mb-3",
        ),
        dbc.Row(
            [
                dbc.Label("Output geom", html_for="model-output-geom", width=2),
                dbc.Col(
                    dbc.Input(id="model-output-geom", type="text", placeholder="Enter output geom path(s) (optional)"),
                    width=10,
                ),
            ],
            className="mb-3",
        ),
        dbc.Row(
            [
                dbc.Label("Output grid", html_for="model-output-grid", width=2),
                dbc.Col(
                    dbc.Input(id="model-output-grid", type="text", placeholder="Enter output grid path (optional)"),
                    width=10,
                ),
            ],
            className="mb-3",
        ),
    ],
)

hazard = dbc.Form(
    [
        dbc.Row(
            [
                dbc.Label("File", html_for="model-hazard-file", width=2),
                dbc.Col(dbc.Input(id="model-hazard-file", type="text", placeholder="Enter hazard file path"), width=10),
            ],
            className="mb-3",
        ),
        dbc.Row(
            [
                dbc.Label("Elevation reference", html_for="model-hazard-elevation-reference", width=2),
                dbc.Col(
                    dbc.Input(
                        id="model-hazard-elevation-reference",
                        type="text",
                        placeholder="Enter hazard elevation reference path",
                    ),
                    width=10,
                ),
            ],
            className="mb-3",
        ),
        dbc.Row(
            [
                dbc.Label("Risk", html_for="model-hazard-risk", width=2),
                dbc.Col(dbc.Switch(id="model-hazard-risk", value=False)),
            ],
            className="mb-3",
        ),
    ],
)


exposure = dbc.Form(
    [
        dbc.Row(
            [
                dbc.Label("Exposure geom", html_for="model-exposure-geom", width=2),
                dbc.Col(
                    dbc.Input(id="model-exposure-geom", type="text", placeholder="Enter exposure geom path(s)"),
                    width=10,
                ),
            ],
            className="mb-3",
        ),
        dbc.Row(
            [
                dbc.Label("Exposure CSV", html_for="model-exposure-csv", width=2),
                dbc.Col(dbc.Input(id="model-exposure-csv", type="text", placeholder="Enter exposure CSV path")),
            ],
            className="mb-3",
        ),
    ],
)
vulnerability = dbc.Form(
    [
        dbc.Row(
            [
                dbc.Label("Vulnerability file", html_for="model-vulnerability-file", width=2),
                dbc.Col(
                    dbc.Input(id="model-vulnerability-file", type="text", placeholder="Enter vulnerability file path"),
                ),
            ],
            className="mb-3",
        ),
    ],
)

model_config_form = html.Div(
    [
        html.H2("Model configuration", style={"color": FONT_COLOR, "textAlign": "center"}),
        html.Hr(style={"color": FONT_COLOR}),
        html.Div(
            [
                dbc.Accordion(
                    [
                        dbc.AccordionItem(
                            output,
                            title=html.P("Output", style={"fontWeight": "bold", "color": FONT_COLOR}),
                        ),
                        dbc.AccordionItem(
                            hazard,
                            title=html.P("Hazard", style={"fontWeight": "bold", "color": FONT_COLOR}),
                        ),
                        dbc.AccordionItem(
                            exposure,
                            title=html.P("Exposure", style={"fontWeight": "bold", "color": FONT_COLOR}),
                        ),
                        dbc.AccordionItem(
                            vulnerability,
                            title=html.P("Vulnerability", style={"fontWeight": "bold", "color": FONT_COLOR}),
                        ),
                    ],
                ),
            ],
            style={"maxHeight": "60vh", "overflow": "auto"},
        ),
        html.Hr(style={"color": FONT_COLOR}),
        dbc.Row(
            dbc.Col(dbc.Button("Run model", id="model-run-btn", style={"backgroundColor": FONT_COLOR})),
            style={"float": "right"},
            className="mb-3",
        ),
    ],
    style={"padding": "1rem"},
    id="model-config-form",
)

model_run_window = html.Div(
    [
        html.H2("Model run log", style={"color": FONT_COLOR, "textAlign": "center"}),
        html.Hr(style={"color": FONT_COLOR}),
        dbc.Textarea(
            id="model-log",
            readOnly=True,
            style={
                "height": "60vh",
                "margin": "auto",
                "padding": "1rem",
            },
        ),
        dbc.Row(
            dbc.Col(dbc.Button("Back", id="model-back-btn", style={"backgroundColor": FONT_COLOR})),
            style={"float": "left", "paddingTop": "1rem"},
            className="mb-3",
        ),
    ],
    id="model-run-window",
    style={"padding": "1rem", "display": "none"},
)

content_box = dbc.Row(
    [
        dbc.Col(width=2),
        dbc.Col(
            [
                html.Div(
                    [model_config_form, model_run_window],
                    style={
                        "height": "100%",
                        "width": "100%",
                        "boxShadow": "0 4px 8px 0 rgba(0, 0, 0, 0.2), 0 6px 20px 0 rgb(0 0 0 / 19%)",
                        "backgroundColor": "white",
                        "borderRadius": "25px",
                    },
                ),
            ],
            width=8,
        ),
        dbc.Col(width=2),
    ],
    style={"height": "80vh", "width": "100%"},
)

layout = [nav_bar, html.Br(), content_box]
