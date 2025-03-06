import numpy as np
import pytplot

def xyz_to_polar(data, co_latitude=False):
    """
    Convert cartesian coordinates to polar coordinates.

    Parameters
    ----------
    x : numpy.ndarray
        x-component of the vector
    y : numpy.ndarray
        y-component of the vector
    z : numpy.ndarray
        z-component of the vector

    Returns
    -------
    r : numpy.ndarray
        radial component of the vector
    theta : numpy.ndarray
        polar angle of the vector
    phi : numpy.ndarray
        azimuthal angle of the vector
    """

    make_tvars=False
    if isinstance(data, str):
        make_tvars = True
        name_in = data
        d=pytplot.get_data(name_in)
        data = d.y

    x = data[:, 0]
    y = data[:, 1]
    z = data[:, 2]
    out = np.zeros(data.shape)
    out[:, 0] = np.sqrt(x**2 + y**2 + z**2)
    out[:, 1] = np.arccos(z/out[:, 0])*180.0/np.pi
    out[:, 2] = np.arctan2(y, x)*180.0/np.pi
    if not co_latitude:
        out[:, 1] = 90.0 - out[:, 1]

    if make_tvars:
        pytplot.store_data(name_in+'_mag', data={'x':d.times, 'y':out[:,0]})
        pytplot.store_data(name_in + '_th', data={'x': d.times, 'y': out[:, 1]})
        pytplot.store_data(name_in + '_phi', data={'x': d.times, 'y': out[:, 2]})
        return
    else:
        return out
