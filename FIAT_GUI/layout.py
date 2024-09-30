"""Module containing the layout of the app."""

import dash_bootstrap_components as dbc
import visdcc
from dash import dcc, html

FONT_COLOR = "#080C80"


user_agreement_modal = html.Div(
    [
        dbc.Modal(
            [
                dbc.ModalHeader(dbc.ModalTitle("User agreement"), close_button=False),
                dbc.ModalBody(
                    [
                        html.P(
                            """Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nam augue sapien, scelerisque ac
                             nibh quis, interdum aliquet neque. Aenean vel metus venenatis libero tristique iaculis sit
                             amet at nunc. Fusce nec augue luctus, sollicitudin nulla et, placerat risus. Duis posuere
                              quam ornare ante consectetur, et convallis velit bibendum. Nunc ligula enim, vestibulum
                               finibus metus vel, porttitor varius augue. Ut et luctus ligula, vitae scelerisque erat.
                                Cras at molestie orci. Fusce cursus nunc facilisis, aliquet arcu vitae, vulputate
                                odio.""",
                        ),
                        html.P(
                            """Pellentesque eu euismod diam. Pellentesque vitae gravida ante. Integer maximus sit amet
                            diam ac tempus. Donec vitae tincidunt ante. Aenean blandit tincidunt ornare. Mauris a massa
                            gravida, lobortis metus at, mollis purus. Nam sit amet felis urna. In hac habitasse platea
                            dictumst. Fusce pulvinar tempor enim, lobortis sollicitudin augue pulvinar ut. Nunc lobortis
                            hendrerit dui, ac volutpat sapien tristique ac. Aenean massa magna, viverra sit amet
                            scelerisque eget, pharetra sed arcu. Nunc vitae mollis risus. Morbi non porta tortor.""",
                        ),
                    ],
                ),
                dbc.ModalFooter(dbc.Button("I agree", style={"backgroundColor": FONT_COLOR}, id="user-agreement-btn")),
            ],
            is_open=True,
            backdrop="static",
            id="user-agreement-modal",
        ),
    ],
)

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


def file_dialog_btn(btn_id: str) -> dbc.Button:
    return dbc.Button(
        [
            html.I(className="bi bi-folder2"),
        ],
        id=btn_id,
        style={"backgroundColor": "white", "borderColor": "black", "color": "black"},
    )


output = dbc.Form(
    [
        dbc.Row(
            [
                dbc.Label("Path", html_for="model-output-path", width=2),
                dbc.Col(
                    [
                        dbc.Input(id="model-output-path", type="text", placeholder="Enter output path"),
                        dbc.FormText(
                            "Add a valid path to the output directory",
                            style={"display": "none", "color": "red"},
                            id="model-output-path-formtext",
                        ),
                    ],
                    width=9,
                ),
                dbc.Col(file_dialog_btn(btn_id="output-filedialog-btn")),
            ],
            className="mb-3",
        ),
        dbc.Row(
            [
                dbc.Label("Output CSV", html_for="model-output-csv", width=2),
                dbc.Col(
                    dbc.Input(
                        id="model-output-csv",
                        type="text",
                        placeholder="Enter name of output CSV file (optional)",
                    ),
                    width=9,
                ),
            ],
            className="mb-3",
        ),
        dbc.Row(
            [
                dbc.Label("Output geom", html_for="model-output-geom", width=2),
                dbc.Col(
                    dbc.Input(
                        id="model-output-geom",
                        type="text",
                        placeholder="Enter name(s) of output geometry (optional)",
                    ),
                    width=9,
                ),
            ],
            className="mb-3",
        ),
        dbc.Row(
            [
                dbc.Label("Output grid", html_for="model-output-grid", width=2),
                dbc.Col(
                    dbc.Input(id="model-output-grid", type="text", placeholder="Enter name of output grid (optional)"),
                    width=9,
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
                dbc.Label("Risk", html_for="model-hazard-risk", width=2),
                dbc.Col(dbc.Switch(id="model-hazard-risk", value=False)),
            ],
            className="mb-3",
        ),
        html.Div(
            [
                dbc.Row(
                    [
                        dbc.Label("Hazard file 1", width=2),
                        dbc.Col(dbc.Input(type="text", placeholder="Enter hazard file path"), width=6),
                        dbc.Col(file_dialog_btn("btn-id"), width=1),
                        dbc.Label("Return period", width=2),
                        dbc.Col(dbc.Input(type="number")),
                    ],
                    className="mb-3",
                ),
                dbc.Row(dbc.Col(dbc.Button("add another hazard"), width=3), justify="center", className="mb-3"),
            ],
            id="hazard-multiple-input",
            style={"display": "none"},
        ),
        html.Div(
            [
                dbc.Row(
                    [
                        dbc.Label("File", html_for="model-hazard-file", width=2),
                        dbc.Col(
                            [
                                dbc.Input(id="model-hazard-file", type="text", placeholder="Enter hazard file path"),
                                dbc.FormText(
                                    "Add a valid path to the hazard file",
                                    style={"display": "none", "color": "red"},
                                    id="model-hazard-file-formtext",
                                ),
                            ],
                            width=9,
                        ),
                        dbc.Col(file_dialog_btn(btn_id="hazard-file-filedialog-btn")),
                    ],
                    className="mb-3",
                ),
                dbc.Row(
                    [
                        dbc.Label("Elevation reference", html_for="model-hazard-elevation-reference", width=2),
                        dbc.Col(
                            dbc.Select(
                                options=[{"label": "DEM", "value": "DEM"}, {"label": "datum", "value": "datum"}],
                                id="model-hazard-elevation-reference",
                            ),
                            width=9,
                        ),
                    ],
                    className="mb-3",
                ),
            ],
            id="hazard-single-input",
            style={"display": "block"},
        ),
    ],
)


exposure = dbc.Form(
    [
        dbc.Row(
            [
                dbc.Label("Exposure geom", html_for="model-exposure-geom", width=2),
                dbc.Col(
                    [
                        dbc.Input(id="model-exposure-geom", type="text", placeholder="Enter exposure geom path(s)"),
                        dbc.FormText(
                            "Add a valid path to the exposure geometry file",
                            style={"display": "none", "color": "red"},
                            id="model-exposure-geom-formtext",
                        ),
                    ],
                    width=9,
                ),
                dbc.Col(file_dialog_btn(btn_id="exposure-geom-filedialog-btn")),
            ],
            className="mb-3",
        ),
        dbc.Row(
            [
                dbc.Label("Exposure geom CRS", width=2),
                dbc.Col(
                    dbc.Input(id="model-exposure-geom-crs", placeholder="Add geom CRS in EPSG", type="text"), width=9
                ),
            ],
            className="mb-3",
        ),
        dbc.Row(
            [
                dbc.Label("Exposure CSV", html_for="model-exposure-csv", width=2),
                dbc.Col(
                    [
                        dbc.Input(id="model-exposure-csv", type="text", placeholder="Enter exposure CSV path"),
                        dbc.FormText(
                            "Add a valid path to the model exposure csv file",
                            style={"display": "none", "color": "red"},
                            id="model-exposure-csv-formtext",
                        ),
                    ],
                    width=9,
                ),
                dbc.Col(file_dialog_btn(btn_id="exposure-csv-filedialog-btn")),
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
                    [
                        dbc.Input(
                            id="model-vulnerability-file", type="text", placeholder="Enter vulnerability file path"
                        ),
                        dbc.FormText(
                            "Add a valid path to vulnerability file",
                            style={"display": "none", "color": "red"},
                            id="model-vulnerability-file-formtext",
                        ),
                    ],
                    width=9,
                ),
                dbc.Col(file_dialog_btn(btn_id="vulnerability-file-filedialog-btn")),
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
            dbc.Col(dbc.Button("Next", id="next-btn", style={"backgroundColor": FONT_COLOR})),
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
            size="lg",
            style={
                "height": "60vh",
                "margin": "auto",
                "padding": "1rem",
                "fontFamily": "Courier New, monospace",
            },
        ),
        dbc.Row(
            [
                dbc.Col(
                    dbc.Button("Back", id="model-back-btn", style={"backgroundColor": FONT_COLOR, "float": "left"}),
                    width=3,
                ),
                dbc.Col(
                    dbc.Button(
                        "Run model", id="model-run-btn", style={"backgroundColor": FONT_COLOR, "float": "right"}
                    ),
                    width=3,
                ),
            ],
            style={"paddingTop": "1rem"},
            className="mb-3",
            justify="around",
        ),
        dbc.Alert("model run started", id="model-run-alert", duration=5000),
        dcc.Interval(id="model-log-interval", disabled=True),
        visdcc.Run_js(id="js-log", run=""),
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

layout = [user_agreement_modal, nav_bar, html.Br(), content_box]
