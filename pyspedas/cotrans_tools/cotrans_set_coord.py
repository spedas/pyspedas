import logging
from pytplot import set_coords


def cotrans_set_coord(name, coord):
    logging.info("cotrans_set_coord is now a wrapper for pytplot.set_coords().  This version will eventually be removed.")
    return set_coords(name,coord)
