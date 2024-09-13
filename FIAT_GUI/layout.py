import dash_bootstrap_components as dbc


nav_bar = dbc.Navbar(
    [
        dbc.Row(
            [
                dbc.Col(
                    dbc.NavbarBrand("HydroMT Dashboard", style={"paddingLeft": "1rem"}),
                    width=4,
                ),
                dbc.Col(
                    dbc.Button(
                        "Help",
                        id="help-button",
                        style={
                            "float": "right",
                            "backgroundColor": "#080C80",
                            "borderColor": "white",
                            "color": "white",
                        },
                        outline=True,
                        className="me-1",
                    ),
                    width=4,
                ),
            ],
            justify="between",
            style={"width": "100%"},
        ),
    ],
    color="#080C80",
    # fluid=True,
    # links_left=True,
    dark=True,
    expand="lg",
    style={
        "boxShadow": "0 4px 8px 0 rgba(0, 0, 0, 0.2), 0 6px 20px 0 rgb(0 0 0 / 19%)",
        "padding": "1rem",
        "width": "100%",
        "maxWidth": "100%",
    },
)

layout = [nav_bar]
