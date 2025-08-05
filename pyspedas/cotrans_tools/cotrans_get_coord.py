import logging
from pyspedas.pytplot import get_coords

def cotrans_get_coord(name):
    logging.info("cotrans_get_coord is now a wrapper forpyspedas.pytplot).  This version will eventually be removed.")
    return get_coords(name)
