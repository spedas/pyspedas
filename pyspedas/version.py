"""Print the version number for the current installation."""
import logging
# We don't want to shadow the importlib version() with pyspedas(version)
from importlib.metadata import version as imp_version
from importlib.metadata import PackageNotFoundError

def version():
    """
    Print the pyspedas version number.

    Returns
    -------
    None.

    """
    try:
        ver = imp_version("pyspedas")
    except PackageNotFoundError:
        ver = 'bleeding edge'
    logging.info("pyspedas version: " + ver)
