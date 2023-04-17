import logging
import pytplot

def tkm2re(name, km=False, newname=None, suffix=''):
    """
    Converts a tplot variable to Re or Km

    Input
    ------
        name: str or list of str
            Names of tplot variables to convert

    Parameters
    -----------
        km: bool
            Flag to convert Re to Km

        newname: str or list of str
            Output variable names; if not set, the names of the
            input variables are used + '_re' or '_km'

        suffix: str
            Specify to append a suffix to each variable 
            (only valid if newname is not specified)

    Returns
    --------
        List of the tplot variables created

    """
    logging.info("tkm2re has been moved to the pytplot.tplot_math module. Please update your imports!")
    logging.info("This version will eventually be removed.")
    return pytplot.tplot_math.tkm2re(name=name,km=km,newname=newname,suffix=suffix)
