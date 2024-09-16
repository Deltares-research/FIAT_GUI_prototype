"""Module containing the callbacks of the app."""

from __future__ import annotations

import io
import logging
from pathlib import Path

import subprocess
from dash import Input, Output, State, callback, callback_context
from dash.exceptions import PreventUpdate

from FIAT_GUI.fiat_api import get_available_geom_exts, get_available_grid_exts
from FIAT_GUI.utils import create_fiat_toml, file_dialog

logger = logging.getLogger()
log_capture_string = io.StringIO()
ch = logging.StreamHandler(log_capture_string)
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
ch.setFormatter(formatter)
logger.addHandler(ch)


@callback(
    Output("user-agreement-modal", "is_open"),
    Input("user-agreement-btn", "n_clicks"),
    State("user-agreement-modal", "is_open"),
)
def toggle_user_agreement(n_clicks, is_open):
    if n_clicks:
        return not is_open
    return is_open


@callback(
    Output("model-config-form", "style"),
    Output("model-run-window", "style"),
    Input("next-btn", "n_clicks"),
    Input("model-back-btn", "n_clicks"),
    State("model-config-form", "style"),
    State("model-run-window", "style"),
)
def toggle_content(next_btn, back_btn, config_form_style: dict, run_window_style: dict) -> list[dict, dict]:
    changed_id = [p["prop_id"] for p in callback_context.triggered][0]
    if "next-btn" in changed_id:
        config_form_style.update({"display": "none"})
        run_window_style.update({"display": "block"})
    elif "model-back-btn" in changed_id:
        config_form_style.update({"display": "block"})
        run_window_style.update({"display": "none"})

    return config_form_style, run_window_style


def handle_file_dialog(
    btn_id: str,
    *,
    file_type: str | None = None,
    is_file: bool = True,
    multiple: bool = False,
    title: str | None = None,
):
    changed_id = [p["prop_id"] for p in callback_context.triggered][0]
    if btn_id in changed_id:
        if file_type == "CSV":
            file_types = [("CSV", "*.csv")]
        elif file_type == "geom":
            file_types = get_available_geom_exts()
        elif file_type == "grid":
            file_types = get_available_grid_exts()
        else:
            file_types = None
        return file_dialog(title=title, file_types=file_types, is_file=is_file, multiple=multiple)
    raise PreventUpdate


@callback(Output("model-output-path", "value"), Input("output-filedialog-btn", "n_clicks"))
def model_output_path_fd(fd_btn):
    return handle_file_dialog(
        "output-filedialog-btn",
        file_type=None,
        is_file=False,
        multiple=False,
        title="Please select a folder for the model output files",
    )


@callback(Output("model-hazard-file", "value"), Input("hazard-file-filedialog-btn", "n_clicks"))
def model_hazard_file_fd(fd_btn):
    return handle_file_dialog(
        "hazard-file-filedialog-btn",
        file_type="grid",
        is_file=True,
        multiple=False,
        title="Please select the hazard file(s)",
    )


@callback(Output("model-exposure-geom", "value"), Input("exposure-geom-filedialog-btn", "n_clicks"))
def model_exposure_geom_fd(fd_btn):
    return handle_file_dialog(
        "exposure-geom-filedialog-btn",
        file_type="geom",
        is_file=True,
        multiple=True,
        title="Select the exposure geometry file(s)",
    )


@callback(Output("model-exposure-csv", "value"), Input("exposure-csv-filedialog-btn", "n_clicks"))
def model_exposure_csv_fd(fd_btn):
    return handle_file_dialog(
        "exposure-csv-filedialog-btn",
        file_type="CSV",
        is_file=True,
        multiple=False,
        title="Select the exposure CSV file",
    )


@callback(Output("model-vulnerability-file", "value"), Input("vulnerability-file-filedialog-btn", "n_clicks"))
def model_vulnerability_file_fd(fd_btn):
    return handle_file_dialog(
        "vulnerability-file-filedialog-btn",
        file_type="CSV",
        is_file=True,
        multiple=False,
        title="Select the vulnerability CSV file",
    )


@callback(
    Output("model-log-interval", "disabled"),
    Input("next-btn", "n_clicks"),
    State("model-output-path", "value"),
    State("model-output-csv", "value"),
    State("model-output-geom", "value"),
    State("model-output-grid", "value"),
    State("model-hazard-file", "value"),
    State("model-hazard-elevation-reference", "value"),
    State("model-hazard-risk", "value"),
    State("model-exposure-geom", "value"),
    State("model-exposure-csv", "value"),
    State("model-vulnerability-file", "value"),
)
def create_toml(
    next_btn,
    ouput_path,
    output_csv,
    output_geom,
    output_grid,
    hazard_file,
    hazard_elev_ref,
    hazard_risk,
    exposure_geom,
    exposure_csv,
    vulnerability_file,
):
    changed_id = [p["prop_id"] for p in callback_context.triggered][0]
    if "next-btn" in changed_id:
        create_fiat_toml(
            ouput_path=ouput_path,
            output_csv=output_csv,
            output_geom=output_geom,
            output_grid=output_grid,
            hazard_file=hazard_file,
            hazard_elev_ref=hazard_elev_ref,
            hazard_risk=hazard_risk,
            exposure_geom=exposure_geom,
            exposure_csv=exposure_csv,
            vulnerability_file=vulnerability_file,
        )
        return False
    raise PreventUpdate


@callback(
    Output("model-log", "value"),
    Output("js-log", "run"),
    Input("model-log-interval", "n_intervals"),
    Input("model-run-btn", "n_clicks"),
    State("model-log-interval", "disabled"),
    State("model-log", "value"),
)
def stream_model_log(n_intervals, run_btn, model_log_disabled, model_log):
    if n_intervals and not model_log_disabled:
        js = """
        var textarea = document.getElementById('model-log');
        textarea.scrollTop = textarea.scrollHeight;
        """

        return log_capture_string.getvalue(), js

    raise PreventUpdate


@callback(
    Output("model-run-alert", "is_open"),
    Input("model-run-btn", "n_clicks"),
    State("model-output-path", "value"),
)
def run_model(n_clicks, output_path):
    changed_id = [p["prop_id"] for p in callback_context.triggered][0]
    if "model-run-btn" in changed_id:
        model_config_path = output_path + "/model_config.toml"
        subprocess.run(["fiat", "run", model_config_path, "-v"], shell=True)
        return True
    raise PreventUpdate
