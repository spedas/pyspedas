import numpy as np
from pyspedas import get_data, store_data, sphere_to_cart, cart_to_sphere, geodetic_correction

def cartesian2geodeticpolar(data: str | np.ndarray, inverse=False):
    """
    Get positional data from tplot variable, then convert data coordinates to 
    geodetic polar coordinates

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
    """
    make_tvars = False
    # Get data:
    if isinstance(data, str):
        make_tvars = True
        name_in = data
        d = get_data(name_in)
        data = d.y

    out = np.zeros(data.shape)
    if not inverse:
        # Assume cartesian XYZ, convert to geodetic polar
        x_cart = data[:, 0]
        y_cart = data[:, 1]
        z_cart = data[:, 2]

        r, lat_geoc_deg, lon_deg = cart_to_sphere(x_cart, y_cart, z_cart)
        lat_geod_deg = geodetic_correction(lat_geoc_deg)

        out[:,0] = r
        out[:,1] = lat_geod_deg
        out[:,2] = lon_deg
        
        if make_tvars:
            store_data(name_in + '_geodeticpolar', data={'x': d.times, 'y':out})
            return
        else:
            return out
    else:
        # Assume geodetic polar R, Lat, Lon, return cartesian XYZ
        r = data[:, 0]
        lat_geod_deg = data[:, 1]
        lon_deg = data[:, 2]

        lat_geoc_deg = geodetic_correction(lat_geod_deg,inverse=True)
        x_cart, y_cart, z_cart = sphere_to_cart(r, lat_geoc_deg, lon_deg)

        out[:,0] = x_cart
        out[:,1] = y_cart
        out[:,2] = z_cart

        if make_tvars:
            store_data(name_in + '_cartesian', data={'x':d.times, 'y':out})
            return
        else:
            return out
    