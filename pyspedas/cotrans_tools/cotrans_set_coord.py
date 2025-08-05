import logging
from pyspedas.pytplot import set_coords


def cotrans_set_coord(name, coord):
    logging.info("cotrans_set_coord is now a wrapper forpyspedas.pytplot).  This version will eventually be removed.")
    return set_coords(name,coord)
