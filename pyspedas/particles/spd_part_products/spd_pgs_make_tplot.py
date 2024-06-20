import logging
import numpy as np
from pytplot import store_data, options

from pyspedas.particles.spd_units_string import spd_units_string


def spd_pgs_make_tplot(name, x=None, y=None, z=None, units='', ylog=False, zlog=True, colorbar='spedas', ytitle=None, ysubtitle=''):
    """
    Create tplot variable with standard spectrogram settings

    Parameters
    ----------
        name: str
            Name of the new tplot variable to create

        x: numpy.ndarray
            X-axis values (time)

        y: numpy.ndarray
            Y-axis values

        z: numpy.ndarray
            Z-axis values (data)

        units: str
            Units string to store in the metadata

        ylog: bool
            Set the y-axis to log scale (default: False)

        zlog: bool
            Set the z-axis to log scale (default: True)

        colorbar: str
            PyTplot 'Colormap' option (default: 'spedas')

    Returns
    -------
    str
        String containing new variable name

    """

    if not isinstance(x, np.ndarray) or not isinstance(y, np.ndarray) or not isinstance(z, np.ndarray) :
        logging.error('Error, must specify x, y and z parameters')
        return

    if ytitle is None:
        ytitle = name

    store_data(name, data={'x': x, 'y': z, 'v': y})
    options(name, 'ylog', ylog)
    options(name, 'zlog', zlog)
    options(name, 'Spec', True)
    options(name, 'ytitle', ytitle)
    options(name, 'ysubtitle', ysubtitle)
    options(name, 'ztitle', spd_units_string(units, units_only=True))
    options(name, 'Colormap', colorbar)
    return name
