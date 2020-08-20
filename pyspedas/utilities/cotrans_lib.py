"""
Functions for coordinate transformations.

Notes
-----
These functions are in cotrans_lib.pro of IDL SPEDAS.

"""
import numpy as np
from datetime import datetime
from pyspedas import set_igrf_params


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


def cdipdir(time_in=None, iyear=None, idoy=None):
    """
    Compute dipole direction in GEO coordinates.

    Parameters
    ----------
    time_in: float
    iyear: int
    idoy: int

    Returns
    -------
    list of float

    Notes
    -----
    Compute geodipole axis direction from International Geomagnetic Reference
    Field (IGRF-13) model for time interval 1970 to 2020.
    For time out of interval, computation is made for nearest boundary.
    Same as SPEDAS cdipdir.
    """
    if (time_in is None) and (iyear is None) and (idoy is None):
        print("Error: No time was provided.")
        return

    if (iyear is None) or (idoy is None):
        iyear, idoy, ih, im, isec = get_time_parts(time_in)

    # IGRF-13 parameters, 1965-2020.
    minyear, maxyear, ga, ha, dg, dh = set_igrf_params()

    y = iyear - (iyear % 5)
    if y < minyear:
        y = minyear
    elif y > maxyear:
        y = maxyear

    year0 = y
    year1 = y + 5
    g0 = ga[year0]
    h0 = ha[year0]
    maxind = max(ga.keys())
    g = g0
    h = h0

    # Interpolate for dates.
    f2 = (iyear + (idoy-1)/365.25 - year0)/5.
    f1 = 1.0 - f2
    f3 = iyear + (idoy-1)/365.25 - maxind
    nloop = len(g0)
    if year1 <= maxind:
        # years 1970-2020
        g1 = ga[year1]
        h1 = ha[year1]
        for i in range(nloop):
            g[i] = g0[i]*f1 + g1[i]*f2
            h[i] = h0[i]*f1 + h1[i]*f2
    else:
        # years 2020-2025
        for i in range(nloop):
            g[i] = g0[i] + dg[i]*f3
            h[i] = h0[i] + dh[i]*f3

    s = 1.0
    for i in range(2, 15):
        mn = int(i*(i-1.0)/2.0 + 1.0)
        s = int(s*(2.0*i-3.0)/(i-1.0))
        g[mn] *= s
        h[mn] *= s
        g[mn-1] *= s
        h[mn-1] *= s
        p = s
        for j in range(2, i):
            aa = 1.0
            if j == 2:
                aa = 2.0
            p = p * np.sqrt(aa*(i-j+1)/(i+j-2))
            mnn = int(mn + j - 1)
            g[mnn] *= p
            h[mnn] *= p
            g[mnn-1] *= p
            h[mnn-1] *= p

    g10 = -g[1]
    g11 = g[2]
    h11 = h[2]

    sq = g11**2 + h11**2
    sqq = np.sqrt(sq)
    sqr = np.sqrt(g10**2 + sq)
    s10 = -h11/sqq
    c10 = -g11/sqq
    st0 = sqq/sqr
    ct0 = g10/sqr

    stc1 = st0*c10
    sts1 = st0*s10

    d1 = stc1
    d2 = sts1
    d3 = ct0

    return d1, d2, d3


def cdipdir_vect(time_in=None, iyear=None, idoy=None):
    """
    Compute dipole direction in GEO coordinates.

    Similar to cdipdir but for arrays.

    Parameters
    ----------
    time_in: list of floats
    iyear: list of int
    idoy: list of int

    Returns
    -------
    list of float

    Notes
    -----
    Same as SPEDAS cdipdir_vec.
    """
    if ((time_in is None or not isinstance(time_in, list))
        and (iyear is None or not isinstance(iyear, list))
            and (idoy is None or not isinstance(idoy, list))):
        return cdipdir(time_in, iyear, idoy)

    if (iyear is None) or (idoy is None):
        iyear, idoy, ih, im, isec = get_time_parts(time_in)

    d1 = []
    d2 = []
    d3 = []
    for i in range(len(idoy)):
        _d1, _d2, _d3 = cdipdir(None, iyear[i], idoy[i])
        d1.append(_d1)
        d2.append(_d2)
        d3.append(_d3)

    return np.array(d1), np.array(d2), np.array(d3)


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
    Array of float
        Coordinates in GSE.

    """
    xgse, ygse, zgse = tgeigse_vect(time_in, data_in)

    return np.column_stack([xgse, ygse, zgse])


def tgsegei_vect(time_in, data_in):
    """
    GSE to GEI transformation.

    Parameters
    ----------
    time_in: list of float
        Time array.
    data_in: list of float
        xgei, ygei, zgei cartesian GEI coordinates.

    Returns
    -------
    xgei: list of float
         Cartesian GEI coordinates.
    ygei: list of float
        Cartesian GEI coordinates.
    zgei: list of float
        Cartesian GEI coordinates.

    """
    xgei, ygei, zgei = 0, 0, 0
    d = np.array(data_in)
    xgse, ygse, zgse = d[:, 0], d[:, 1], d[:, 2]

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

    xgei = gs1 * xgse + gegs1 * ygse + ge1 * zgse
    ygei = gs2 * xgse + gegs2 * ygse + ge2 * zgse
    zgei = gs3 * xgse + gegs3 * ygse + ge3 * zgse

    return xgei, ygei, zgei


def subgse2gei(time_in, data_in):
    """
    Transform data from GSE to GEI.

    Parameters
    ----------
    time_in: list of float
        Time array.
    data_in: list of float
        Coordinates in GSE.

    Returns
    -------
    Array of float
        Coordinates in GEI.

    """
    xgei, ygei, zgei = tgsegei_vect(time_in, data_in)

    return np.column_stack([xgei, ygei, zgei])


def tgsegsm_vect(time_in, data_in):
    """
    Transform data from GSE to GSM.

    Parameters
    ----------
    time_in: list of float
        Time array.
    data_in: list of float
        xgse, ygse, zgse cartesian GSE coordinates.

    Returns
    -------
    xgsm: list of float
         Cartesian GSM coordinates.
    ygsm: list of float
        Cartesian GSM coordinates.
    zgsm: list of float
        Cartesian GSM coordinates.

    """
    xgsm, ygsm, zgsm = 0, 0, 0
    d = np.array(data_in)
    xgse, ygse, zgse = d[:, 0], d[:, 1], d[:, 2]

    gd1, gd2, gd3 = cdipdir_vect(time_in)
    gst, slong, sra, sdec, obliq = csundir_vect(time_in)

    gs1 = np.cos(sra) * np.cos(sdec)
    gs2 = np.sin(sra) * np.cos(sdec)
    gs3 = np.sin(sdec)

    sgst = np.sin(gst)
    cgst = np.cos(gst)

    ge1 = 0.0
    ge2 = -np.sin(obliq)
    ge3 = np.cos(obliq)

    gm1 = gd1 * cgst - gd2 * sgst
    gm2 = gd1 * sgst + gd2 * cgst
    gm3 = gd3

    gmgs1 = gm2 * gs3 - gm3 * gs2
    gmgs2 = gm3 * gs1 - gm1 * gs3
    gmgs3 = gm1 * gs2 - gm2 * gs1

    rgmgs = np.sqrt(gmgs1**2 + gmgs2**2 + gmgs3**2)

    cdze = (ge1 * gm1 + ge2 * gm2 + ge3 * gm3)/rgmgs
    sdze = (ge1 * gmgs1 + ge2 * gmgs2 + ge3 * gmgs3)/rgmgs

    xgsm = xgse
    ygsm = cdze * ygse + sdze * zgse
    zgsm = -sdze * ygse + cdze * zgse

    return xgsm, ygsm, zgsm


def subgse2gsm(time_in, data_in):
    """
    Transform data from GSE to GSM.

    Parameters
    ----------
    time_in: list of float
        Time array.
    data_in: list of float
        Coordinates in GSE.

    Returns
    -------
    Array of float
        Coordinates in GSM.

    """
    xgsm, ygsm, zgsm = tgsegsm_vect(time_in, data_in)

    return np.column_stack([xgsm, ygsm, zgsm])


def tgsmgse_vect(time_in, data_in):
    """
    Transform data from GSM to GSE.

    Parameters
    ----------
    time_in: list of float
        Time array.
    data_in: list of float
        xgsm, ygsm, zgsm GSM coordinates.

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
    xgsm, ygsm, zgsm = d[:, 0], d[:, 1], d[:, 2]

    gd1, gd2, gd3 = cdipdir_vect(time_in)
    gst, slong, sra, sdec, obliq = csundir_vect(time_in)

    gs1 = np.cos(sra) * np.cos(sdec)
    gs2 = np.sin(sra) * np.cos(sdec)
    gs3 = np.sin(sdec)

    sgst = np.sin(gst)
    cgst = np.cos(gst)

    ge1 = 0.0
    ge2 = -np.sin(obliq)
    ge3 = np.cos(obliq)

    # Dipole direction in GEI system
    gm1 = gd1 * cgst - gd2 * sgst
    gm2 = gd1 * sgst + gd2 * cgst
    gm3 = gd3

    gmgs1 = gm2 * gs3 - gm3 * gs2
    gmgs2 = gm3 * gs1 - gm1 * gs3
    gmgs3 = gm1 * gs2 - gm2 * gs1

    rgmgs = np.sqrt(gmgs1**2 + gmgs2**2 + gmgs3**2)

    cdze = (ge1 * gm1 + ge2 * gm2 + ge3 * gm3)/rgmgs
    sdze = (ge1 * gmgs1 + ge2 * gmgs2 + ge3 * gmgs3)/rgmgs

    xgse = xgsm
    ygse = cdze * ygsm - sdze * zgsm
    zgse = sdze * ygsm + cdze * zgsm

    return xgse, ygse, zgse


def subgsm2gse(time_in, data_in):
    """
    Transform data from GSM to GSE.

    Parameters
    ----------
    time_in: list of float
        Time array.
    data_in: list of float
        Coordinates in GSE.

    Returns
    -------
    Array of float
        Coordinates in GSE.

    """
    xgse, ygse, zgse = tgsmgse_vect(time_in, data_in)

    return np.column_stack([xgse, ygse, zgse])


def tgsmsm_vect(time_in, data_in):
    """
    Transform data from GSM to SM.

    Parameters
    ----------
    time_in: list of float
        Time array.
    data_in: list of float
        xgsm, ygsm, zgsm GSM coordinates.

    Returns
    -------
    xsm: list of float
         Cartesian SM coordinates.
    ysm: list of float
        Cartesian SM coordinates.
    zsm: list of float
        Cartesian SM coordinates.

    """
    xsm, ysm, zsm = 0, 0, 0
    d = np.array(data_in)
    xgsm, ygsm, zgsm = d[:, 0], d[:, 1], d[:, 2]

    gd1, gd2, gd3 = cdipdir_vect(time_in)
    gst, slong, sra, sdec, obliq = csundir_vect(time_in)

    gs1 = np.cos(sra) * np.cos(sdec)
    gs2 = np.sin(sra) * np.cos(sdec)
    gs3 = np.sin(sdec)

    sgst = np.sin(gst)
    cgst = np.cos(gst)

    # Direction of the sun in GEO system
    ps1 = gs1 * cgst + gs2 * sgst
    ps2 = -gs1 * sgst + gs2 * cgst
    ps3 = gs3

    # Computation of mu angle
    smu = ps1 * gd1 + ps2 * gd2 + ps3 * gd3
    cmu = np.sqrt(1.0 - smu * smu)

    xsm = cmu * xgsm - smu * zgsm
    ysm = ygsm
    zsm = smu * xgsm + cmu * zgsm

    return xsm, ysm, zsm


def subgsm2sm(time_in, data_in):
    """
    Transform data from GSM to SM.

    Parameters
    ----------
    time_in: list of float
        Time array.
    data_in: list of float
        Coordinates in GSM.

    Returns
    -------
    Array of float
        Coordinates in SM.

    """
    xsm, ysm, zsm = tgsmgse_vect(time_in, data_in)

    return np.column_stack([xsm, ysm, zsm])


def tsmgsm_vect(time_in, data_in):
    """
    Transform data from SM to GSM.

    Parameters
    ----------
    time_in: list of float
        Time array.
    data_in: list of float
        xsm, ysm, zsm SM coordinates.

    Returns
    -------
    xsm: list of float
         GSM coordinates.
    ysm: list of float
         GSM coordinates.
    zsm: list of float
         GSM coordinates.

    """
    xgsm, ygsm, zgsm = 0, 0, 0
    d = np.array(data_in)
    xsm, ysm, zsm = d[:, 0], d[:, 1], d[:, 2]

    gd1, gd2, gd3 = cdipdir_vect(time_in)
    gst, slong, sra, sdec, obliq = csundir_vect(time_in)

    gs1 = np.cos(sra) * np.cos(sdec)
    gs2 = np.sin(sra) * np.cos(sdec)
    gs3 = np.sin(sdec)

    sgst = np.sin(gst)
    cgst = np.cos(gst)

    # Direction of the sun in GEO system
    ps1 = gs1 * cgst + gs2 * sgst
    ps2 = -gs1 * sgst + gs2 * cgst
    ps3 = gs3

    # Computation of mu angle
    smu = ps1 * gd1 + ps2 * gd2 + ps3 * gd3
    cmu = np.sqrt(1.0 - smu * smu)

    xgsm = cmu * xsm + smu * zsm
    ygsm = ysm
    zgsm = -smu * xsm + cmu * zsm

    return xgsm, ygsm, zgsm


def subsm2gsm(time_in, data_in):
    """
    Transform data from SM to GSM.

    Parameters
    ----------
    time_in: list of float
        Time array.
    data_in: list of float
        Coordinates in SM.

    Returns
    -------
    Array of float
        Coordinates in GSM.

    """
    xgsm, ygsm, zgsm = tsmgsm_vect(time_in, data_in)

    return np.column_stack([xgsm, ygsm, zgsm])


def subgei2geo(time_in, data_in):
    """
    Transform data from GEI to GEO.

    Parameters
    ----------
    time_in: list of float
        Time array.
    data_in: list of float
        Coordinates in GEI.

    Returns
    -------
    Array of float
        Coordinates in GEO.

    """
    xgeo, ygeo, zgeo = 0, 0, 0
    d = np.array(data_in)
    xgei, ygei, zgei = d[:, 0], d[:, 1], d[:, 2]
    gst, slong, sra, sdec, obliq = csundir_vect(time_in)

    sgst = np.sin(gst)
    cgst = np.cos(gst)

    xgeo = cgst * xgei + sgst * ygei
    ygeo = -sgst * xgei + cgst * ygei
    zgeo = zgei

    return np.column_stack([xgeo, ygeo, zgeo])


def subgeo2gei(time_in, data_in):
    """
    Transform data from GEO to GEI.

    Parameters
    ----------
    time_in: list of float
        Time array.
    data_in: list of float
        Coordinates in GEO.

    Returns
    -------
    Array of float
        Coordinates in GEI.

    """
    xgei, ygei, zgei = 0, 0, 0
    d = np.array(data_in)
    xgeo, ygeo, zgeo = d[:, 0], d[:, 1], d[:, 2]
    gst, slong, sra, sdec, obliq = csundir_vect(time_in)

    sgst = np.sin(gst)
    cgst = np.cos(gst)

    xgei = cgst * xgeo - sgst * ygeo
    ygei = sgst * xgeo + cgst * ygeo
    zgei = zgeo

    return [xgei, ygei, zgei]


def subgeo2mag(time_in, data_in):
    """
    Transform data from GEO to MAG.

    Parameters
    ----------
    time_in: list of float
        Time array.
    data_in: list of float
        Coordinates in GEO.

    Returns
    -------
    Array of float
        Coordinates in MAG.

    Notes
    -----
    Adapted from spedas IDL file geo2mag.pro.

    """
    d = np.array(data_in)

    # Step 1. Transform SM to GEO: SM -> GSM -> GSE -> GEI -> GEO
    n = len(time_in)
    sm = np.zeros((n, 3), float)
    sm[:, 2] = 1.0
    gsm = subsm2gsm(time_in, sm)
    gse = subgsm2gse(time_in, gsm)
    gei = subgse2gei(time_in, gse)
    geo = subgei2geo(time_in, gei)
    mag = geo  # the output

    # Step 2. Transform cartesian to spherical.
    x2y2 = geo[:, 0]**2 + geo[:, 1]**2
    # r = np.sqrt(x2y2 + geo[:, 2]**2)
    theta = np.arctan2(geo[:, 2], np.sqrt(x2y2))  # lat
    phi = np.arctan2(geo[:, 1], geo[:, 0])  # long

    for i in range(n):
        # Step 3. Apply rotations.
        mlong = np.zeros((3, 3), float)
        mlong[0, 0] = np.cos(phi[i])
        mlong[0, 1] = np.sin(phi[i])
        mlong[1, 0] = -np.sin(phi[i])
        mlong[1, 1] = np.cos(phi[i])
        mlong[2, 2] = 1.0
        out = mlong @ d[i]

        mlat = np.zeros((3, 3), float)
        mlat[0, 0] = np.cos(np.pi/2.0 - theta[i])
        mlat[0, 2] = -np.sin(np.pi/2.0 - theta[i])
        mlat[2, 0] = np.sin(np.pi/2.0 - theta[i])
        mlat[2, 2] = np.cos(np.pi/2.0 - theta[i])
        mlat[1, 1] = 1.0
        mag[i] = mlat @ out

    return mag


def submag2geo(time_in, data_in):
    """
    Transform data from MAG to GEO.

    Parameters
    ----------
    time_in: list of float
        Time array.
    data_in: list of float
        Coordinates in MAG.

    Returns
    -------
    Array of float
        Coordinates in GEO.

    Notes
    -----
    Adapted from spedas IDL file mag2geo.pro.

    """
    d = np.array(data_in)

    # Step 1. Transform SM to GEO: SM -> GSM -> GSE -> GEI -> GEO
    n = len(time_in)
    sm = np.zeros((n, 3), float)
    sm[:, 2] = 1.0
    gsm = subsm2gsm(time_in, sm)
    gse = subgsm2gse(time_in, gsm)
    gei = subgse2gei(time_in, gse)
    geo = subgei2geo(time_in, gei)

    # Step 2. Transform cartesian to spherical.
    x2y2 = geo[:, 0]**2 + geo[:, 1]**2
    # r = np.sqrt(x2y2 + geo[:, 2]**2)
    theta = np.arctan2(geo[:, 2], np.sqrt(x2y2))  # lat
    phi = np.arctan2(geo[:, 1], geo[:, 0])  # long

    for i in range(n):
        # Step 3. Apply rotations.
        glat = np.zeros((3, 3), float)
        glat[0, 0] = np.cos(np.pi/2.0 - theta[i])
        glat[0, 2] = np.sin(np.pi/2.0 - theta[i])
        glat[2, 0] = -np.sin(np.pi/2.0 - theta[i])
        glat[2, 2] = np.cos(np.pi/2.0 - theta[i])
        glat[1, 1] = 1.0
        out = glat @ d[i]

        glong = np.zeros((3, 3), float)
        glong[0, 0] = np.cos(phi[i])
        glong[0, 1] = -np.sin(phi[i])
        glong[1, 0] = np.sin(phi[i])
        glong[1, 1] = np.cos(phi[i])
        glong[2, 2] = 1.0
        geo[i] = glong @ out

    return geo
