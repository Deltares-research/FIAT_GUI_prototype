"""Module containing the callbacks of the app."""

from __future__ import annotations

from dash import Input, Output, State, callback, callback_context


@callback(
    Output("model-config-form", "style"),
    Output("model-run-window", "style"),
    Input("model-run-btn", "n_clicks"),
    Input("model-back-btn", "n_clicks"),
    State("model-config-form", "style"),
    State("model-run-window", "style"),
)
def toggle_content(run_btn, back_btn, config_form_style: dict, run_window_style: dict) -> list[dict, dict]:
    changed_id = [p["prop_id"] for p in callback_context.triggered][0]
    if "model-run-btn" in changed_id:
        config_form_style.update({"display": "none"})
        run_window_style.update({"display": "block"})
    elif "model-back-btn" in changed_id:
        config_form_style.update({"display": "block"})
        run_window_style.update({"display": "none"})

    return config_form_style, run_window_style
