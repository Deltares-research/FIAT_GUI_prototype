"""Script for serving the app locally."""

import webbrowser
from threading import Timer

from waitress import serve

from FIAT_GUI.app import server


def open_browser() -> None:
    """Open browser to localhost."""
    webbrowser.open_new("http://127.0.0.1:8080/")


if __name__ == "__main__":
    Timer(1, open_browser).start()
    serve(server)
