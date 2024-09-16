"""Module for interfacing with FIAT."""

from fiat.util import _create_geom_driver_map, _create_grid_driver_map
from fiat import FIAT


def get_available_geom_exts() -> list:
    """Generate a list of the supported geometry extentions."""
    geom_drivers = _create_geom_driver_map()
    return [("Geometry files", " ".join(["*" + key for key in geom_drivers]))]


def get_available_grid_exts() -> list:
    """Generate a list of supported grid extentions."""
    grid_drivers = _create_grid_driver_map()
    return [("Grid files", " ".join(["*" + key for key in grid_drivers]))]


def run_model(cfg):
    m = FIAT.from_path(file=cfg)
    m.run()
