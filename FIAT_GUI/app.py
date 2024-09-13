from FIAT_GUI.layout import layout
from dash import Dash

app = Dash()

app.layout = layout

if __name__ == "__main__":
    app.run_server(debug=True)
