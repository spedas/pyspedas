import numpy as np
from pyspedas import get_data, store_data, sphere_to_cart, cart_to_sphere, geodetic_correction
import logging

def cartesian2geodeticpolar(data: str | np.ndarray, inverse=False):
    """
    Converts cartesian positions to geodetic polar coordinates
    
    Assumes cartesian positions are in the GEO coordinate system, and 
    transforms them to geocentric polar coordinates, and then corrects
    the latitude to account for Earth's oblateness. 
    
    Assumes cartesian data of the following form:
    x = data[:, 0]
    y = data[:, 1]
    z = data[:, 2]

    Setting the 'inverse' argument to 'True' computes the inverse transformation,
    where it assumes geodetic polar data of the following form:
    r            = data[:, 0]
    lat_geod_deg = data[:, 1]
    lon_deg      = data[:, 2]

    Latitude and longitude are assumed and reported in degrees.

    Parameters
    ----------
    data : str or ndarray
        Positional data in cartesian coordinates (meters), where the 
        first dimension are the records and the second dimension is 
        are the x, y, and z (GEO) position components. If `inverse` 
        is set to True, assumes position components are radius (in meters),
        latitude, and longitude (in degrees). If `data` passed as a 
        string, loads positional data from tplot variable, using `data`
        as the tplot variable name. 
    inverse : bool
        Indicates whether or not to use the inverse transformation. If
        False, converts cartesian positions to geodetic polar 
        positions. If True, converts geodetic polar positions to cartesian
        positions.

    Returns
    -------
    ndarray or None
        Positions in geodetic polar coordinates (inverse=False) or positions
        in cartesian coordinates (inverse=True). If loading data from 
        tplot variable, saves transformed position data to tplot variable and
        returns nothing.

    Examples
    --------
    Convert cartesian coordinates to geodetic polar coordinates:
    >>> import numpy as np
    >>> coord_geodeticpolar = cartesian2geodeticpolar(data=np.array([1,0,1]))
    >>> print(coord_geodeticpolar)
    [[ 1.41421356 45.19242142  0.        ]]

    Convert cartesian coordinates to geodetic polar coordinates using a tplot variable:
    >>> import numpy as np
    >>> from pyspedas import store_data, get_data
    >>> name_in = 'position_cartesian'
    >>> store_data(name_in, data={'x':np.array([0,1]),'y':np.array([[1,0,1],[1,1,0]])})
    >>> coord_geodeticpolar = cartesian2geodeticpolar(name_in)
    >>> print((get_data(name_in + '_geodeticpolar')).y)
    [[ 1.41421356 45.19242142  0.        ]
     [ 1.41421356  0.         45.        ]]

    Convert geodetic polar coordinates to cartesian coordinates:
    >>> import numpy as np
    >>> coord_cartesian = cartesian2geodeticpolar(data=np.array([1.41421356,45.19242142,0.0]),inverse=True)
    >>> print(coord_cartesian)
    [[1. 0. 1.]]

    Convert geodetic polar coordinates to cartesian coordinates using a tplot variable:
    >>> import numpy as np
    >>> from pyspedas import store_data, get_data
    >>> name_in = 'position_geodeticpolar'
    >>> store_data(name_in, data={'x':np.array([0,1]),'y':np.array([[1.41421356,45.19242142,0.0],[1.41421356,0.0,45.0]])})
    >>> coord_geodeticpolar = cartesian2geodeticpolar(name_in,inverse=True)
    >>> print( (get_data(name_in + '_cartesian')).y )
    [[1. 0. 1.]
     [1. 1. 0.]]
    """
    make_tvars = False

    name_in = None
    coord_data = data
    if isinstance(data, str):
        # load data from tplot:
        make_tvars = True
        name_in = data
        d = get_data(data)
        coord_data = d.y

    ndim = len(coord_data.shape)
    if ndim != 2:
        if ndim == 1:
            if coord_data.shape[0] == 3:
                logging.warning('Data is 1 dimensional; assuming single record of input coordinates. Output will be 2 dimensional...')
                coord_data = np.reshape(coord_data,(1,3)) 
            else:
                raise ValueError("Data must have 3 elements if 1 dimensional.")
        else:
            raise ValueError(f"Input coordinates have invalid number dimensions: {ndim}")

    out = np.zeros(coord_data.shape)
    name_out = None
    if not inverse:
        if name_in is not None:
            name_out = name_in + '_geodeticpolar'
        # Assume cartesian XYZ, convert to geodetic polar
        x_cart = coord_data[:, 0]
        y_cart = coord_data[:, 1]
        z_cart = coord_data[:, 2]

        r, lat_geoc_deg, lon_deg = cart_to_sphere(x_cart, y_cart, z_cart)
        lat_geod_deg = geodetic_correction(lat_geoc_deg)

        out[:,0] = r
        out[:,1] = lat_geod_deg
        out[:,2] = lon_deg
    else:
        if name_in is not None:
            name_out = name_in + '_cartesian'
        # Assume geodetic polar R, Lat, Lon, return cartesian XYZ
        r            = coord_data[:, 0]
        lat_geod_deg = coord_data[:, 1]
        lon_deg      = coord_data[:, 2]

        lat_geoc_deg = geodetic_correction(lat_geod_deg,inverse=True)
        x_cart, y_cart, z_cart = sphere_to_cart(r, lat_geoc_deg, lon_deg)

        out[:,0] = x_cart
        out[:,1] = y_cart
        out[:,2] = z_cart

    if make_tvars and name_out is not None:
        if not store_data(name_out, data={'x': d.times, 'y':out}):
            raise ValueError(f"Variable {name_out} failed to save!")
        return
    else:
        return out
    