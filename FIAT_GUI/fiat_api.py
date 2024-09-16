from fiat.util import _create_geom_driver_map, _create_grid_driver_map


def get_available_geom_exts():
    geom_drivers = _create_geom_driver_map()
    return [("Geometry files", " ".join(["*" + key for key in geom_drivers.keys()]))]


def get_available_grid_exts():
    grid_drivers = _create_grid_driver_map()
    return [("Grid files", " ".join(["*" + key for key in grid_drivers.keys()]))]
