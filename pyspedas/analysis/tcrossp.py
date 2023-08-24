
import logging
import pytplot

def tcrossp(v1, v2, newname=None, return_data=False):
    """
    Calculates the cross product of two tplot varibles

    Input
    -------
        v1: str
            First tplot variable

        v2: str
            Second tplot variable

    Parameters
    -----------
        newname: str
            Name of the output variable

        return_data: bool
            Returns the data as an ndarray instead of creating a tplot variable

    Returns
    --------
        Name of the tplot variable
    """
    logging.info("tcrossp has been moved to the pytplot.tplot_math module. Please update your imports!")
    logging.info("This version will eventually be removed.")
    return pytplot.tplot_math.tcrossp(v1=v1, v2=v2, newname=newname,return_data=return_data)