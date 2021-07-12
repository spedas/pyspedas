
import logging
from pytplot import store_data, options

logging.captureWarnings(True)
logging.basicConfig(format='%(asctime)s: %(message)s', datefmt='%d-%b-%y %H:%M:%S', level=logging.INFO)

def spd_pgs_moments_tplot(moments, x=None, prefix='', suffix=''):
    """
    Creates tplot variables from moments dictionaries

    Input:
        moments: dict
            Dictionary containing moments values returned by moments_3d

    Parameters:
        x: numpy.ndarray
            The x-axis (time) values

        prefix: str
            Name prefix for the output variables

        suffix: str
            Name suffix for the output variables

    Returns:
        List of tplot variables created.
    """

    if x is None:
        logging.error('Error, no x-values specified')
        return

    if not isinstance(moments, dict):
        logging.error('Error, the "moments" variable must be a hash table containing the moments')
        return


    for key in moments.keys():
        store_data(prefix + '_' + key + suffix, data={'x': x, 'y': moments[key]})

    options(prefix + '_density' + suffix, 'ysubtitle', '[1/cc]')
    options(prefix + '_velocity' + suffix, 'yrange', [-800, 800])
    options(prefix + '_flux' + suffix, 'yrange', [-1e8, 1e8])

    return [prefix + '_' + key + suffix for key in moments.keys()]
