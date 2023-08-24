import logging
from pytplot import get_coords

def cotrans_get_coord(name):
    logging.info("cotrans_get_coord is now a wrapper for pytplot.get_coords().  This version will eventually be removed.")
    return get_coords(name)
