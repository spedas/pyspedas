# -*- coding: utf-8 -*-
"""
File:
    cotrans_lib.py

Description:
    Functions for coordinate transformations.

"""
import numpy as np
from datetime import datetime


def get_time_parts(time_in):
    """
        Splits time into year, doy, hours, minutes, seconds.fsec
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
    Calculates the direction of the sun

    input  : iyear : year (1901-2099)
            idoy : day of the year (1 for january 1)
            ih,im,isec : hours, minutes, seconds U.T.

    output : gst      greenwich mean sideral time (radians)
              slong    longitude along ecliptic (radians)
              sra      right ascension (radians)
              sdec     declination of the sun (radians)
              obliq    inclination of Earth's axis (radians)
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
        GEI to GSE transformation

        input : xgei, ygei, zgei cartesian gei coordinates
        output: xgse, ygse, zgse cartesian gse coordinates
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
    transforms data from GEI to GSE

    Note:
    The corresponding IDL function works with:
    iyear, idoy, ih, im, isec = get_time_parts(time_in)
    """

    xgse, ygse, zgse = tgeigse_vect(time_in, data_in)

    # If we need a vector, we can use:
    # gse = np.column_stack((xgse, ygse, zgse))

    return [xgse, ygse, zgse]
