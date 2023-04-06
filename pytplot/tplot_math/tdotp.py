import logging
from pytplot import get_data, store_data


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

    data1 = get_data(variable1, xarray=True)
    data2 = get_data(variable2, xarray=True)

    if data1 is None:
        logging.error('Variable not found: ' + variable1)
        return

    if data2 is None:
        logging.error('Variable not found: ' + variable2)
        return

    if newname is None:
        newname = variable1 + '_dot_' + variable2

    # calculate the dot product
    out = data1.dot(data2, dims='v_dim')

    # save the output
    saved = store_data(newname, data={'x': data1.time.values, 'y': out.values})

    if saved is not None:
        return newname
