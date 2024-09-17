"""Module for interfacing with FIAT."""

from fiat import FIAT
from fiat.log import CHandler, setup_default_log
from fiat.util import _create_geom_driver_map, _create_grid_driver_map

fiat_start_str = """
###############################################################

        #########    ##          ##      ##############
        ##           ##         ####         ######
        ##           ##         ####           ##
        ##           ##        ##  ##          ##
        ######       ##        ##  ##          ##
        ##           ##       ########         ##
        ##           ##      ##      ##        ##
        ##           ##     ##        ##       ##
        ##           ##    ##          ##      ##

###############################################################

                Fast Impact Assessment Tool
                \u00a9 Deltares

"""


def get_available_geom_exts() -> list:
    """Generate a list of the supported geometry extentions."""
    geom_drivers = _create_geom_driver_map()
    return [("Geometry files", " ".join(["*" + key for key in geom_drivers]))]


def get_available_grid_exts() -> list:
    """Generate a list of supported grid extentions."""
    grid_drivers = _create_grid_driver_map()
    return [("Grid files", " ".join(["*" + key for key in grid_drivers]))]


def run_model(cfg, log_file, log_stream):
    logger = setup_default_log("fiat", level=2, dst=log_file)
    logger._handlers.append(CHandler(level=2, stream=log_stream, name="fiat"))
    for line in fiat_start_str.split("\n"):
        log_stream.write(line + "\n")

    m = FIAT.from_path(file=cfg)
    m.run()
