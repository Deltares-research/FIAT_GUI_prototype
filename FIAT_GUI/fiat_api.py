"""Module for interfacing with FIAT."""

from io import StringIO
from pathlib import Path

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


def run_model(output: str, log_file: str, log_stream: StringIO) -> None:
    """Run FIAT model and adds a log stream to run process."""
    logger = setup_default_log("fiat", level=2, dst=log_file)
    logger._handlers.append(CHandler(level=2, stream=log_stream, name="fiat"))  # noqa: SLF001
    for line in fiat_start_str.split("\n"):
        log_stream.write(line + "\n")

    config_path = Path(output) / "config"
    cfgs = config_path.glob("*.toml")
    for cfg in cfgs:
        m = FIAT.from_path(file=cfg)
        m.run()
