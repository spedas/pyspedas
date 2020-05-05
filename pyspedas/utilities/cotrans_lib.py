"""
Functions for coordinate transformations.

Notes
-----
These functions are in cotrans_lib.pro of IDL SPEDAS.

"""
import numpy as np
from datetime import datetime


def get_time_parts(time_in):
    """
    Split time into year, doy, hours, minutes, seconds.fsec.

    Parameters
    ----------
    time_in: list of float
        Time array.

    Returns
    -------
    iyear: array of int
        Year.
    idoy: array of int
        Day of year.
    ih: array of int
        Hours.
    im: array of int
        Minutes.
    isec: array of float
        Seconds and milliseconds.

    """
    tnp = np.vectorize(datetime.utcfromtimestamp)(time_in[:])
    iyear = np.array([tt.year for tt in tnp])
    idoy = np.array([tt.timetuple().tm_yday for tt in tnp])
    ih = np.array([tt.hour for tt in tnp])
    im = np.array([tt.minute for tt in tnp])
    isec = np.array([tt.second + tt.microsecond/1000000.0 for tt in tnp])

    return iyear, idoy, ih, im, isec


def csundir_vect(time_in):
    """
    Calculate the direction of the sun.

    Parameters
    ----------
    time_in: list of float
        Time array.

    Returns
    -------
    gst: list of float
        Greenwich mean sideral time (radians).
    slong: list of float
        Longitude along ecliptic (radians).
    sra: list of float
        Right ascension (radians).
    sdec: list of float
        Declination of the sun (radians).
    obliq: list of float
        Inclination of Earth's axis (radians).

    """
    iyear, idoy, ih, im, isec = get_time_parts(time_in)

    # Julian day and greenwich mean sideral time
    pisd = np.pi / 180.0
    fday = (ih * 3600.0 + im * 60.0 + isec)/86400.0
    jj = 365 * (iyear-1900) + np.fix((iyear-1901)/4) + idoy
    dj = jj - 0.5 + fday
    gst = np.mod(279.690983 + 0.9856473354 * dj + 360.0 * fday + 180.0,
                 360.0) * pisd

    # longitude along ecliptic
    vl = np.mod(279.696678 + 0.9856473354 * dj, 360.0)
    t = dj / 36525.0
    g = np.mod(358.475845 + 0.985600267 * dj, 360.0) * pisd
    slong = (vl + (1.91946 - 0.004789 * t) * np.sin(g) + 0.020094 *
             np.sin(2.0 * g)) * pisd

    # inclination of Earth's axis
    obliq = (23.45229 - 0.0130125 * t) * pisd
    sob = np.sin(obliq)
    cob = np.cos(obliq)

    # Aberration due to Earth's motion around the sun (about 0.0056 deg)
    pre = (0.005686 - 0.025e-4 * t) * pisd

    # declination of the sun
    slp = slong - pre
    sind = sob * np.sin(slp)
    cosd = np.sqrt(1.0 - sind**2)
    sc = sind / cosd
    sdec = np.arctan(sc)

    # right ascension of the sun
    sra = np.pi - np.arctan2((cob/sob) * sc, -np.cos(slp)/cosd)

    return gst, slong, sra, sdec, obliq


def tgeigse_vect(time_in, data_in):
    """
    GEI to GSE transformation.

    Parameters
    ----------
    time_in: list of float
        Time array.
    data_in: list of float
        xgei, ygei, zgei cartesian GEI coordinates.

    Returns
    -------
    xgse: list of float
         Cartesian GSE coordinates.
    ygse: list of float
        Cartesian GSE coordinates.
    zgse: list of float
        Cartesian GSE coordinates.

    """
    xgse, ygse, zgse = 0, 0, 0
    d = np.array(data_in)
    xgei, ygei, zgei = d[:, 0], d[:, 1], d[:, 2]

    gst, slong, sra, sdec, obliq = csundir_vect(time_in)

    gs1 = np.cos(sra) * np.cos(sdec)
    gs2 = np.sin(sra) * np.cos(sdec)
    gs3 = np.sin(sdec)

    ge1 = 0.0
    ge2 = -np.sin(obliq)
    ge3 = np.cos(obliq)

    gegs1 = ge2 * gs3 - ge3 * gs2
    gegs2 = ge3 * gs1 - ge1 * gs3
    gegs3 = ge1 * gs2 - ge2 * gs1

    xgse = gs1 * xgei + gs2 * ygei + gs3 * zgei
    ygse = gegs1 * xgei + gegs2 * ygei + gegs3 * zgei
    zgse = ge1 * xgei + ge2 * ygei + ge3 * zgei

    return xgse, ygse, zgse


def subgei2gse(time_in, data_in):
    """
    Transform data from GEI to GSE.

    Parameters
    ----------
    time_in: list of float
        Time array.
    data_in: list of float
        Coordinates in GEI.

    Returns
    -------
    list
        Coordinates in GSE.

    """
    xgse, ygse, zgse = tgeigse_vect(time_in, data_in)

    # If we need a vector, we can use:
    # gse = np.column_stack((xgse, ygse, zgse))

    return [xgse, ygse, zgse]
