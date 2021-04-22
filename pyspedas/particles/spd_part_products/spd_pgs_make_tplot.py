
import numpy as np
from pytplot import store_data, options

def spd_pgs_make_tplot(name, x=None, y=None, z=None, units='', ylog=False, zlog=True, colorbar='jet'):
    """


    """

    if not isinstance(x, np.ndarray) or not isinstance(y, np.ndarray) or not isinstance(z, np.ndarray) :
        print('Error, must specify x, y and z parameters')
        return

    store_data(name, data={'x': x, 'y': z, 'v': y})
    options(name, 'ylog', ylog)
    options(name, 'zlog', zlog)
    options(name, 'Spec', True)
    options(name, 'Colormap', colorbar)