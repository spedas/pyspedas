"""
Transform datetimes from string to decimal.

Examples
--------
time_float()
time_float(['2017-06-29 23:59:59.1234', '2017-12-01 00:15:21.1234'])
time_double()

Notes
-----
Similar to time_double.pro in IDL SPEDAS.

"""
import pytplot
import logging

def time_float(str_time=None):
    """
    Transform a list of datetimes from string to decimal.

    Parameters
    ----------
    str_time : str/list of str, optional
        Input times. The default is None.

    Returns
    -------
    list of float
        Output times as floats.

    """
    logging.info("time_float has been moved to the pytplot package. Please update your imports!")
    logging.info("This version will eventually be removed.")
    return pytplot.time_float(str_time=str_time)

def time_double(str_time=None):
    """
    Transform a list of datetimes from string to decimal.

    Same as time_float.

    Parameters
    ----------
    str_time : str/list of str, optional
        Input times. The default is None.

    Returns
    -------
    list of float
        Output times as floats.

    """
    logging.info("time_double has been moved to the pytplot package. Please update your imports!")
    logging.info("This version will eventually be removed.")
    return pytplot.time_float(str_time=str_time)