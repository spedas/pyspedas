import logging
import pytplot

def tnormalize(variable, newname=None, return_data=False):
    """
    Normalize all the vectors stored in a tplot variable

    Input
    ----------
        variable: str or np.ndarray
            tplot variable (or numpy array) containing the vectors to be normalized

    Parameters
    ----------
        newname: str
            name of the output variable; default: variable_normalized

        return_data: bool
            return the normalized vectors instead of creating a tplot variable
    
    Returns
    ----------

        name of the tplot variable created or normalized vectors if return_data
        is set

    """
    logging.info("tnormalize has been moved to the pytplot.tplot_math module. Please update your imports!")
    logging.info("This version will eventually be removed.")
    return pytplot.tplot_math.tnormalize(variable=variable,newname=newname,return_data=return_data)