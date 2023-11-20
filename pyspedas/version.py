"""Print the version number for the current installation."""
import logging


def version():
    """
    Print the pyspedas version number.

    Returns
    -------
    None.

    """
    from importlib_metadata import version
    ver = version("pyspedas")
    logging.info("pyspedas version: " + ver)
