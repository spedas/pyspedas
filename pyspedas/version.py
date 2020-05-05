"""Print the version number for the current installation."""


def version():
    """
    Print the pyspedas version number.

    Returns
    -------
    None.

    """
    import pkg_resources
    ver = pkg_resources.get_distribution("pyspedas").version
    print("pyspedas version: " + ver)
