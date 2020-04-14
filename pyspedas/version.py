
"""
File:
    version.py

Description:
    pySPEDAS version number.

Returns:
    The version number for the current installation.
"""


def version():
    import pkg_resources
    ver = pkg_resources.get_distribution("pyspedas").version
    print("pyspedas version: " + ver)
