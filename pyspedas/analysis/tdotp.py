import logging
import pytplot


def tdotp(variable1, variable2, newname=None):
    """
        Routine to calculate the dot product of two tplot variables 
        containing arrays of vectors and storing the results in a 
        tplot variable

    Input
    -------
        variable1: str
            First tplot variable

        variable2: str
            Second tplot variable

    Parameters
    -----------
        newname: str
            Name of the output variable
            
    Returns
    --------
        Name of the tplot variable
    """
    logging.info("tdotp has been moved to the pytplot.tplot_math module. Please update your imports!")
    logging.info("This version will eventually be removed.")
    pytplot.tplot_math.tdotp(variable1=variable1,variable2=variable2,newname=newname)