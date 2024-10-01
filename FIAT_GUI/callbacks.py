"""Module containing the callbacks of the app."""

from __future__ import annotations

import io
from pathlib import Path

import dash_bootstrap_components as dbc
from dash import MATCH, Input, Output, State, callback, callback_context, ALL
from dash.exceptions import PreventUpdate

from FIAT_GUI.fiat_api import get_available_geom_exts, get_available_grid_exts, run_model
from FIAT_GUI.layout import file_dialog_btn
from FIAT_GUI.utils import _validate_path_callback, create_fiat_toml, file_dialog

LOG_STRING = io.StringIO()


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


@callback(
    Output("hazard-multiple-input", "style"),
    Output("hazard-single-input", "style"),
    Input("model-hazard-risk", "value"),
    State("hazard-multiple-input", "style"),
    State("hazard-single-input", "style"),
)
def toggle_multiple_hazard_input(switch_on, multi_hazard_style, single_hazard_style):
    single_hazard_style.update({"display": "block"})
    multi_hazard_style.update({"display": "none"})
    if switch_on:
        single_hazard_style.update({"display": "none"})
        multi_hazard_style.update({"display": "block"})
        return multi_hazard_style, single_hazard_style
    return multi_hazard_style, single_hazard_style


@callback(
    Output("hazard-multiple-input", "children"),
    Input("add-hazard-btn", "n_clicks"),
    State("hazard-multiple-input", "children"),
)
def add_hazard_input(n_clicks, multiple_hazard_children):
    changed_id = [p["prop_id"] for p in callback_context.triggered][0]
    if "add-hazard-btn" in changed_id:
        id = len(multiple_hazard_children)
        multiple_hazard_children.insert(
            -1,
            dbc.Row(
                [
                    dbc.Label(f"Hazard file {id}", width=2),
                    dbc.Col(
                        [
                            dbc.Input(
                                type="text",
                                placeholder="Enter hazard file path",
                                id={"type": "multiple-hazard-file-input", "index": id},
                            ),
                            dbc.FormText(
                                "Add a valid path to the hazard file",
                                style={"display": "none", "color": "red"},
                                id={"type": "multiple-hazard-file-input-formtext", "index": id},
                            ),
                        ],
                        width=6,
                    ),
                    dbc.Col(
                        file_dialog_btn(btn_id={"type": "multiple-hazard-file-input-dialog", "index": id}),
                        width=1,
                    ),
                    dbc.Label("Return period", width=2),
                    dbc.Col(dbc.Input(id={"type": "hazard-return-period", "index": id}, type="number")),
                ],
                className="mb-3",
            ),
        )
    return multiple_hazard_children


@callback(
    Output({"type": "multiple-hazard-file-input", "index": MATCH}, "value"),
    Input({"type": "multiple-hazard-file-input-dialog", "index": MATCH}, "n_clicks"),
)
def handle_file_dialog_multiple_hazard(n_clicks):
    if n_clicks:
        return file_dialog(title="Please select the hazard file", file_types=get_available_grid_exts(), is_file=True)
    raise PreventUpdate


@callback(
    Output({"type": "multiple-hazard-file-input", "index": MATCH}, "valid"),
    Output({"type": "multiple-hazard-file-input", "index": MATCH}, "invalid"),
    Output({"type": "multiple-hazard-file-input-formtext", "index": MATCH}, "style"),
    Input({"type": "multiple-hazard-file-input", "index": MATCH}, "value"),
    State({"type": "multiple-hazard-file-input-formtext", "index": MATCH}, "style"),
)
def multiple_hazard_formtext(path, formtext_style):
    return _validate_path_callback(path, formtext_style)


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
        title="Please select the hazard file",
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
    Output("model-output-path", "valid"),
    Output("model-output-path", "invalid"),
    Output("model-output-path-formtext", "style"),
    Input("model-output-path", "value"),
    State("model-output-path-formtext", "style"),
)
def validate_model_output_path(path, formtext_style):
    return _validate_path_callback(path, formtext_style)


@callback(
    Output("model-hazard-file", "valid"),
    Output("model-hazard-file", "invalid"),
    Output("model-hazard-file-formtext", "style"),
    Input("model-hazard-file", "value"),
    State("model-hazard-file-formtext", "style"),
)
def validate_hazard_file_path(path, formtext_style):
    return _validate_path_callback(path, formtext_style)


@callback(
    Output("model-exposure-geom", "valid"),
    Output("model-exposure-geom", "invalid"),
    Output("model-exposure-geom-formtext", "style"),
    Input("model-exposure-geom", "value"),
    State("model-exposure-geom-formtext", "style"),
)
def validate_exposure_geom_path(path, formtext_style):
    return _validate_path_callback(path, formtext_style)


@callback(
    Output("model-exposure-csv", "valid"),
    Output("model-exposure-csv", "invalid"),
    Output("model-exposure-csv-formtext", "style"),
    Input("model-exposure-csv", "value"),
    State("model-exposure-csv-formtext", "style"),
)
def validate_exposure_csv_path(path, formtext_style):
    return _validate_path_callback(path, formtext_style)


@callback(
    Output("model-vulnerability-file", "valid"),
    Output("model-vulnerability-file", "invalid"),
    Output("model-vulnerability-file-formtext", "style"),
    Input("model-vulnerability-file", "value"),
    State("model-vulnerability-file-formtext", "style"),
)
def validate_vulnerability_file(path, formtext_style):
    return _validate_path_callback(path, formtext_style)


@callback(
    Output("next-btn", "disabled"),
    Input("model-output-path", "value"),
    # Input("model-hazard-file", "value"),
    Input("model-hazard-elevation-reference", "value"),
    Input("model-exposure-geom", "value"),
    Input("model-exposure-geom-crs", "value"),
    Input("model-exposure-csv", "value"),
    Input("model-vulnerability-file", "value"),
)
def enable_next_btn(*args: tuple[str]):
    return not all(args)


@callback(
    Output("model-log-interval", "disabled"),
    Input("next-btn", "n_clicks"),
    Input("model-back-btn", "n_clicks"),
    State("model-output-path", "value"),
    State("model-output-csv", "value"),
    State("model-output-geom", "value"),
    State("model-output-grid", "value"),
    State("model-hazard-file", "value"),
    State("model-hazard-elevation-reference", "value"),
    State("model-hazard-risk", "value"),
    State("model-exposure-geom", "value"),
    State("model-exposure-geom-crs", "value"),
    State("model-exposure-csv", "value"),
    State("model-vulnerability-file", "value"),
    State({"type": "multiple-hazard-file-input", "index": ALL}, "value"),
    State({"type": "hazard-return-period", "index": ALL}, "value"),
)
def create_toml(  # noqa: PLR0913
    next_btn,
    back_btn,
    ouput_path,
    output_csv,
    output_geom,
    output_grid,
    hazard_file,
    hazard_elev_ref,
    hazard_risk,
    exposure_geom,
    exposure_geom_crs,
    exposure_csv,
    vulnerability_file,
    multiple_hazard_files,
    return_periods,
):
    changed_id = [p["prop_id"] for p in callback_context.triggered][0]
    if "next-btn" in changed_id:
        if hazard_risk:
            for hazard_fp, rp in zip(multiple_hazard_files, return_periods):
                config_file = f"return_period_{rp}.toml"
                create_fiat_toml(
                    ouput_path=ouput_path,
                    output_csv=output_csv,
                    output_geom=output_geom,
                    output_grid=output_grid,
                    hazard_file=hazard_fp,
                    hazard_elev_ref=hazard_elev_ref,
                    exposure_geom=exposure_geom,
                    exposure_geom_crs=exposure_geom_crs,
                    exposure_csv=exposure_csv,
                    vulnerability_file=vulnerability_file,
                    config_file_name=config_file,
                )

        create_fiat_toml(
            ouput_path=ouput_path,
            output_csv=output_csv,
            output_geom=output_geom,
            output_grid=output_grid,
            hazard_file=hazard_file,
            hazard_elev_ref=hazard_elev_ref,
            exposure_geom=exposure_geom,
            exposure_geom_crs=exposure_geom_crs,
            exposure_csv=exposure_csv,
            vulnerability_file=vulnerability_file,
        )
        return False
    if "model-back-btn" in changed_id:
        return True
    raise PreventUpdate


@callback(
    Output("model-log", "value"),
    Output("js-log", "run"),
    Input("model-log-interval", "n_intervals"),
    Input("model-run-btn", "n_clicks"),
    State("model-log-interval", "disabled"),
    State("model-log", "value"),
    State("model-output-path", "value"),
)
def stream_model_log(n_intervals, run_btn, model_log_disabled, model_log, output_path):
    if n_intervals and not model_log_disabled:
        js = """
        var textarea = document.getElementById('model-log');
        textarea.scrollTop = textarea.scrollHeight;
        """
        if value := LOG_STRING.getvalue():
            model_log = value
        return model_log, js

    raise PreventUpdate


@callback(
    Output("model-run-alert", "is_open"),
    Input("model-run-btn", "n_clicks"),
    State("model-output-path", "value"),
)
def start_model(n_clicks, output_path):
    changed_id = [p["prop_id"] for p in callback_context.triggered][0]
    if "model-run-btn" in changed_id:
        model_config_path = Path(output_path) / "model_config.toml"
        # run model
        run_model(model_config_path, log_stream=LOG_STRING, log_file=output_path)
        return True
    raise PreventUpdate
