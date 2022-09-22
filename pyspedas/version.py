"""Print the version number for the current installation."""
import logging


def version():
    """
    Print the pyspedas version number.

    Returns
    -------
    None.

    """
    import pkg_resources
    ver = pkg_resources.get_distribution("pyspedas").version
    logging.info("pyspedas version: " + ver)
