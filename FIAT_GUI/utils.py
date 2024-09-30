"""util functions for FIAT GUI."""

from __future__ import annotations

import tkinter as tk
from pathlib import Path
from tkinter import filedialog

import toml


def file_dialog(title: str, file_types, *, is_file: bool = True, multiple: bool = False) -> str | None:
    root = tk.Tk()
    # Force dialog to stay on top of all other open windows - this is the closest
    #  we can get to a browser popup.
    root.attributes("-topmost", True)
    # Remove window and task bar
    root.withdraw()
    if is_file and multiple:
        path = filedialog.askopenfilenames(title=title, filetypes=file_types)
    elif is_file:
        path = filedialog.askopenfilename(title=title, filetypes=file_types)
    else:
        path = filedialog.askdirectory(title=title)
    root.destroy()
    return path if path else None


def create_fiat_toml(
    *,
    ouput_path: str,
    output_csv: str,
    output_geom: str,
    output_grid: str,
    hazard_file: str,
    hazard_elev_ref: str,
    hazard_risk: bool,
    exposure_geom: str,
    exposure_geom_crs: str,
    exposure_csv: str,
    vulnerability_file: str,
) -> Path:
    model_config = {}
    if output_geom:
        output_geom = _seperate_input_names(output_geom)
    if output_grid:
        output_grid = _seperate_input_names(output_grid)
    model_config["output"] = {"path": ouput_path, "csv": {"name": output_csv}, "geom": output_geom, "grid": output_grid}
    model_config["hazard"] = {"file": hazard_file, "elevation_reference": hazard_elev_ref, "risk": hazard_risk}
    if exposure_geom:
        exposure_geom = _seperate_input_names(exposure_geom, key="file", crs=exposure_geom_crs)
    model_config["exposure"] = {"geom": exposure_geom, "csv": {"file": exposure_csv}}
    model_config["vulnerability"] = {"file": vulnerability_file}

    toml_file = Path(ouput_path) / "model_config.toml"

    with toml_file.open(mode="w") as f:
        toml.dump(model_config, f)
    return toml_file


def _seperate_input_names(_input: list, key: str = "name", crs=None) -> dict:
    if not isinstance(_input, list):
        _input = [_input]

    _dict = {f"{key}{x+1}": name for x, name in enumerate(_input)}
    if crs:
        _dict["crs"] = crs
    return _dict


def _validate_path_callback(path: str | None | list, formtext_style: dict) -> tuple[bool, bool, dict]:
    formtext_style.update({"display": "none"})
    if path:
        if isinstance(path, list):
            if all(Path(p).exists() for p in path):
                return True, False, formtext_style
        elif Path(path).exists():
            return True, False, formtext_style
        formtext_style.update({"display": "block"})
        return (
            False,
            True,
            formtext_style,
        )

    return False, False, formtext_style
