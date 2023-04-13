import pytplot
import logging

def data_exists(tvar):
    """
    Checks if a tplot variable exists
    """
    logging.info("data_exists has been moved to the pytplot package.  Please update your imports!")
    logging.info("This version will eventually be removed.")
    return pytplot.data_exists(tvar=tvar)
