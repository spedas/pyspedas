import logging
import numpy as np
from geopack.geopack import recalc as geopack_recalc
from pyspedas import cotrans, time_double


def sm_ns_model(time, gsm_pos, sc2NS=False):
    """
    This routine calculates the NS position along the zaxis at a specific x and y location.
    """
    # convert gsm to sm coordinates
    sm_pos = cotrans(time_in=time, data_in=gsm_pos, coord_in='gsm', coord_out='sm')
    zns = gsm_pos[:, 2] - sm_pos[:, 2]
    if not sc2NS:
        return zns
    else:
        sc2NS = gsm_pos[:, 2] - zns
        return sc2NS


def themis_ns_model(time, gsm_pos, sc2NS=False):
    """
    NAME:
        themis_ns_model
    PURPOSE:
        This routine calculates the position along the zaxis at a specific
        x and y location. The themis model is used for this calculation.
        The themis model uses z-sm (converted from z-gsm) for the inner probes
        and the Hammond model for the outer probes.
    INPUT:
        time - string or double format
               double(s)  seconds since 1970
               string(s)  format:  YYYY-MM-DD/hh:mm:ss
        gsm_pos - position vector in GSM coordinates in re (pos[*,3])
    OUTPUT: returns Z displacement of the neutral sheet above or below the XY plane in Re (zgsm of the NS)
            Value is positive if NS is above z=0 gsm plane, negative if below
    KEYWORDS
        sc2NS - if set returns Z displacement from the spacecraft to the neutral sheet
                Value is positive if the NS is northward of the SC location, and negative if below
    NOTES;
        Reference:
        The themis model uses z-sm (converted from z-gsm) for the inner probes
        and the Hammond model (default) for the outer probes. The algorithm can be found
        in ssllib neutralsheet.pro.
    HISTORY:
    """
    # initialize constants and variables
    re = 6378.
    h0 = 8.6   # 10.5 # hinge point of the neutral sheet
    rad = np.pi/180.
    dz2NS = np.zeros(len(time))

    # constants used in hammond model
    H1=8.6
    Y0=20.2
    D=12.2

    # calculate the radial distance
    rdist = np.sqrt(gsm_pos[:,0]**2 + gsm_pos[:,1]**2 + gsm_pos[:,2]**2)

    # Use the sm coordinates for radial distances <= h0  (8.6)
    sm_ind = np.argwhere(rdist <= h0).flatten()
    if len(sm_ind) > 0:
        sm_pos = cotrans(time_in=time[sm_ind], data_in=gsm_pos[sm_ind,:], coord_in='gsm', coord_out='sm')
        dz2NS[sm_ind] = -sm_pos[:, 2]

    # Use the Hammond model for radial distances > h0  (8.6)
    lr_ind = np.argwhere(rdist > h0).flatten()
    if len(lr_ind) > 0:
        # initialize variables
        x = gsm_pos[lr_ind, 0]
        y = gsm_pos[lr_ind, 1]
        z = gsm_pos[lr_ind, 2]
        tilt = np.zeros(len(x))
        # check input time format and convert to doy, hr, min
        for i in range(len(x)):
            # calculate the tilt in degrees
            tilt[i] = geopack_recalc(time_double(time[lr_ind[i]]))

        # hammond model
        iless = np.argwhere(np.abs(y) < Y0).flatten()
        if len(iless) > 0:
            dz2NS[lr_ind[iless]] = ((H1+D)*np.sqrt(1-y[iless]**2/Y0**2)-D)*np.sin(tilt[iless])

        imore = np.argwhere(np.abs(y) >= Y0).flatten()
        if len(imore) > 0:
            dz2NS[lr_ind[imore]] = -D*np.sin(tilt[imore])

    if not sc2NS:
        return gsm_pos[:, 2] - (-dz2NS)
    else:
        return -dz2NS


def aen_ns_model(time, gsm_pos, sc2NS=False):
    """
    NAME:
    aen_ns_model

    PURPOSE:  This program is to find the AEN(Analytical Equatorial Neutral) sheet in the
              magnetopause in different time and position

    INPUT:
    time - string or double format
           double(s)  seconds since 1970
           string(s)  format:  YYYY-MM-DD/hh:mm:ss
    gsm_pos - position vector in GSM coordinates in re (pos[*,3])

    OUTPUT: returns Z displacement of the neutral sheet above or below the XY plane in Re (zgsm of the NS)
            Value is positive if NS is above z=0 gsm plane, negative if below

    KEYWORDS
        sc2NS - if set returns Z displacement from the spacecraft to the neutral sheet
                Value is positive if the NS is northward of the SC location, and negative if below

    NOTES:

    References:
    (1) AEN(Analytical Equatorial Neutral):
        Zhu, M. and R.-L. Xu, 1994, A continuous neutral sheet model and a normal
        curved coordinate system in the magnetotail,  Chinese J. Space Science,  14,
        (4)269, (in Chinese).
        Wang, Z.-D. and R.-L. Xu, Neutral Sheet Observed on ISEE Satellite,
        Geophysical Research Letter, 21, (19)2087, 1994.
    (2) Magnetopause model:
        Sibeck, D. G., R. E. Lopez, and E. C. Roelof, Solar wind control of the
        magnetopause shape, location, and motion, J. Grophys. Res., 96, 5489, 1991

    HISTORY:

    """
    # initialize constants
    h0 = 12.6/np.pi

    dz2ns = np.zeros(len(time))

    for i in range(len(time)):
        # calculate the tilt angle
        tt = geopack_recalc(time_double(time[i]))

        # calculate the position of the neutral sheet
        dz2ns[i] = -h0 * np.sin(tt) * np.arctan(gsm_pos[i,0]/5) * (2*np.cos(gsm_pos[i,1]/6))

    if not sc2NS:
        return dz2ns
    else:
        return gsm_pos[:, 2]-dz2ns


def den_ns_model(time, gsm_pos, sc2NS=False):
    """
    NAME:
        den_ns_model
    PURPOSE:
        This program finds the DEN(Displaced Equatorial Neutral) sheet inside
        the magnetopause in different tine and positions. The routine calculates
        the position along the zaxis at a specific location.
    INPUT:
        time - string or double format
               double(s)  seconds since 1970
               string(s)  format:  YYYY-MM-DD/hh:mm:ss
        gsm_pos - position vector in GSM coordinates in re (pos[*,3])
    OUTPUT: returns Z displacement of the neutral sheet above or below the XY plane in Re (zgsm of the NS)
            Value is positive if NS is above z=0 gsm plane, negative if below
    KEYWORDS
        sc2NS - if set returns Z displacement from the spacecraft to the neutral sheet
                Value is positive if the NS is northward of the SC location, and negative if below
    NOTES:
        References:
        (1) DEN(Displaced Equatorial Neutral):
            Xu, R.-L., A Displaced Equatorial Neutral Sheet Surface Observed on ISEE-2
            Satellite,  J. Atmospheric and Terrestrial Phys., 58, 1085, 1991
        (2) Magnetopause model:
            Sibeck, D. G., R. E. Lopez, and R. C. Roelof, Solar wind control of the
            magnetopause shape, location, and motion, J. Grophys. Res., 96, 5489, 1991
        Original Authors of the FORTRAN source code:
        Ronglan XU and Lei LI, Center for Space Sci. and Applied Res.,
        Chinese Academy of Sciences, PO Box 8701, Beijing 100080, China
        E-mail: XURL@SUN.IHEP.AC.CN, XURL@SUN20.CSSAR.AC.CN
        This source code was ported from the original FORTRAN source code into IDL
        The original source code only calculated to 10.05 RE. In this IDL version
        that restriction was increased to 25.
    HISTORY:
    """
    # calculate the position of the neutral sheet along z axis
    H = 25.5
    H1 = 25.05

    dz2ns = np.zeros(len(time))

    for i in range(len(time)):
        done = 0
        xgsm = gsm_pos[i,0]
        ygsm = gsm_pos[i,1]

        # get tilt angle of magnetic pole
        tilt = geopack_recalc(time_double(time[i]))

        if xgsm > -100.:
            d = sd1(tilt, H, H1, xgsm)
            ym21 = ((H1*(H+d))**2) * (1-(xgsm/(H*np.cos(tilt)))**2)
            ym22 = (H+d)**2 - (d-xgsm/np.cos(tilt))**2
            ym2 = ym21/ym22
            if ym2 < 0:
                #ie[i] = 2
                continue
            ym = np.sqrt(ym2)
            xd2 = ((H*np.cos(tilt))**2) * (1-(ygsm/H1)**2)
            if np.abs(ygsm) > H1:
                xd2 = 0
            # find the equatorial region
            xd = np.sqrt(xd2)
            rd = np.sqrt(xd**2+ygsm**2)
            rsm = np.sqrt(xgsm**2+ygsm**2)
            if xgsm > 0 or rsm <= rd:
                dz2ns[i] = -xgsm*np.sin(tilt)/np.cos(tilt)
                done = 1
            if np.abs(ygsm) > ym and done != 1:
                dz2ns[i] = -d*np.sin(tilt)
                done = 1
            if done != 1:
                dz2ns[i] = ((H+d)*np.sqrt(1-(ygsm**2)/ym2)-d)*np.sin(tilt)

    if not sc2NS:
        return dz2ns
    else:
        sc2NS = gsm_pos[:,2] - dz2ns
        return sc2NS


def smpf(xgsm, rmp, im):
    im = 0
    rmp2 = -0.14*xgsm**2 - 18.2*xgsm+217.4
    if rmp2 < 0:
        im = 9999.99
    else:
        rmp = np.sqrt(rmp2)
        if xgsm <= -65:
            rmp = 28.5


def sfa4(aa, bb, cc, dd):
    ndx = 0
    xmin = 0
    xmax = 50
    ndxmax = 3
    dx = 1
    x = xmin
    yy = x**4 + aa*x**3 + bb*x**2 + cc*x + dd

    while ndx <= ndxmax:
        x = x+dx
        if x >= xmax:
            ndx = 0
            return x
        y = x**4 + aa*x**3 + bb*x**2 + cc*x + dd
        ry = y/yy
        if ry < 0:
            x = x-dx
            dx = dx/10.
            ndx = ndx+1
        else:
            yy = y
    return x


def sd1(til, H, H1, xgsm):
    ct = np.cos(til)
    xx = xgsm
    xh = -H*ct
    if xgsm >= xh:
        xx = xh

    # calculate the radius of the cross section
    if xx <= -5.:
        rm = 9*(10-3*xx)/(10-xx)+3
    if xx > -5.:
        rm = np.sqrt(18**2-(xx+5)**2)
    rm2 = rm**2

    # in cross_section areas above and below the neutral
    # sheet
    aa = 4*H-(32*rm2*H**2)/(np.pi**2*H1**2*(H-xx/ct))
    bb = 2*H**2*(3.-8.*rm2/(np.pi**2*H1**2))
    cc = 4*(H**3)
    dd = H**4
    x = sfa4(aa, bb, cc, dd)

    d = x
    if xgsm >= xh:
        fk = -x/np.sqrt(-xh)
        d = -fk*np.sqrt(-xgsm)
    return d


def fairfield_ns_model(time, gsm_pos, sc2NS=False):
    """
    NAME:
    fairfield_NS_model

    PURPOSE:
    This routine calculates the position along the zaxis at a specific
    x and y location. The Fairfield model is used to this calculation.

    INPUT:
    time - string or double format
           double(s)  seconds since 1970
           string(s)  format:  YYYY-MM-DD/hh:mm:ss
    gsm_pos - position vector in GSM coordinates in re (pos[*,3])

    OUTPUT: returns Z displacement of the neutral sheet above or below the XY plane in Re (zgsm of the NS)
            Value is positive if NS is above z=0 gsm plane, negative if below

    KEYWORDS
        sc2NS - if set returns Z displacement from the spacecraft to the neutral sheet
                Value is positive if the NS is northward of the SC location, and negative if below

    NOTES:
    Reference:
    A statistical determination of the shape and position of the
    geomagnetic neutral sheet,  Journal of Geophysical Research,
    Vol. 85, No A2, pages 775-780, February 1, 1980
    Author - D. Fairfield

    HISTORY:
    """

    # constants (in re)
    h0 = 10.5
    y0 = 22.5
    d = 14.

    dz2NS = np.zeros(len(time))
    tilt = np.zeros(len(time))

    for i in range(len(time)):
        # calculate tilt angle of geomagnetic axis
        tilt[i] = geopack_recalc(time_double(time[i]))

    # calculate the position of the neutral sheet along z axis
    y_ge_y0 = np.argwhere(np.abs(gsm_pos[:,0]) >= y0).flatten()
    y_lt_y0 = np.argwhere(np.abs(gsm_pos[:,0]) < y0).flatten()
    if len(y_ge_y0) > 0:
        dz2NS[y_ge_y0] = -d*np.sin(tilt[y_ge_y0])
    if len(y_lt_y0) > 0:
        dz2NS[y_lt_y0] = ((h0 + d) * np.sqrt(1 - gsm_pos[y_lt_y0,0]**2/y0**2) - d)*np.sin(tilt[y_lt_y0])

    if not sc2NS:
        return dz2NS
    else:
        sc2NS = gsm_pos[:, 2] - dz2NS
        return sc2NS

   
def den_fairfield_ns_model(time, gsm_pos, sc2NS=False):
    """
    NAME:
     den_fairfield_ns_model
    PURPOSE:
     This routine calculates the position along the zaxis at a specific
     x and y location.
    INPUT:
     time - string or double format
            double(s)  seconds since 1970
            string(s)  format:  YYYY-MM-DD/hh:mm:ss
     gsm_pos - position vector in GSM coordinates in re (pos[*,3])
    OUTPUT: returns Z displacement of the neutral sheet above or below the XY plane in Re (zgsm of the NS)
            Value is positive if NS is above z=0 gsm plane, negative if below
    KEYWORDS
     sc2NS - if set returns Z displacement from the spacecraft to the neutral sheet
             Value is positive if the NS is northward of the SC location, and negative if below
    HISTORY:
    """
    # initialize constants
    dz2ns = np.zeros(len(time))

    # Use the den model for radial distances <12.re
    rdist = np.sqrt(gsm_pos[:,0]**2 + gsm_pos[:,1]**2 + gsm_pos[:,2]**2)
    sm_ind = np.argwhere(rdist <= 10.).flatten()
    if len(sm_ind) > 0:
        dz2ns[sm_ind] = den_ns_model(time[sm_ind], gsm_pos[sm_ind,:])

    # use the fairfield model for radial distances >12.re
    lr_ind = np.argwhere(rdist > 10.).flatten()
    if len(lr_ind) > 0:
        dz2ns[lr_ind] = fairfield_ns_model(time[lr_ind], gsm_pos[lr_ind,:])

    if not sc2NS:
        return dz2ns
    else:
        sc2NS = gsm_pos[:,2] - dz2ns
        return sc2NS


def lopez_ns_model(time, gsm_pos, kp=None, mlt=None, sc2NS=False):
    """
    NAME:
        lopez_ns_model
    PURPOSE:
        This routine calculates the position along the zaxis at a specific
        x and y location. The Lopez model is used for this calculation.
    INPUT:
        time - string or double format
               double(s)  seconds since 1970
               string(s)  format:  YYYY-MM-DD/hh:mm:ss
        gsm_pos - position vector in GSM coordinates in re (pos[*,3])
        kp - kp index value
        mlt - magnetic local time in degrees (0=midnight)
    OUTPUT: returns Z displacement of the neutral sheet above or below the XY plane in Re (zgsm of the NS)
            Value is positive if NS is above z=0 gsm plane, negative if below
    KEYWORDS
        sc2NS - if set returns Z displacement from the spacecraft to the neutral sheet
                Value is positive if the NS is northward of the SC location, and negative if below
    NOTES:
        Reference:
        The position of the magnetotail neutral sheet in the near-Earth Region,
        Geophysical Research Letters, Vol. 17, No 10, pages 1617-1620, 1990
        Author - Ramon E. Lopez
        The lopez model is best used for distances <8.8 RE
    HISTORY:
    """
    # constants
    rad = np.pi/180.
    if kp is None:
        kp = 0
    if mlt is None:
        mlt = 0.0
    tilt = np.zeros(len(time))

    for i in range(len(time)):
        # calculate tilt angle of geomagnetic axis
        tilt[i] = geopack_recalc(time[i])

    # calculate the position of the neutral sheet along z axis
    rdist = np.sqrt(gsm_pos[:,0]**2 + gsm_pos[:,1]**2 + gsm_pos[:,2]**2)
    mlat = -(0.14*kp + 0.69) * ((np.cos(rad*mlt))**.3333333) * (0.065*(rdist**0.8) - 0.16) * tilt * 180.0/np.pi
    mlat = mlat + tilt * 180.0/np.pi

    # convert magnetic latitude to position
    x, y, z = rthph2xyz(rdist, mlat, mlt)

    if not sc2NS:
        return z
    else:
        sc2NS = gsm_pos[:,2] - z
        return sc2NS


def rthph2xyz(r,th,ph):
    """
    Helper function for the lopez model
    converts spherical to cartesian coordinates
    NOTE: th,ph in degrees, and th is latitude (not colatitude) (i.e. [-90->90])
    """
    FLAG=6.8792E+28
    FLAG98=0.98*FLAG
    PI=3.1415926535898

    thrad=th*PI/180.
    phrad=ph*PI/180.
    sth=np.sin(thrad)
    cth=np.cos(thrad)
    sph=np.sin(phrad)
    cph=np.cos(phrad)
    x=r*cth*cph
    y=r*cth*sph
    z=r*sth

    iflags=np.argwhere((r > FLAG98) | (th > FLAG98) | (ph > FLAG98)).flatten()
    if (len(iflags) > 0):
        x[iflags]=FLAG
        y[iflags]=FLAG
        z[iflags]=FLAG

    return x,y,z


def neutral_sheet(time, pos, kp=None, model='themis', mlt=None, in_coord='gsm', sc2NS=False):
    """
    Calculate the distance to the neutral sheet for a given time and position.

    Parameters
    ----------
    time : datetime
        Time of interest.
    pos : array_like
        Position of interest.
    kp : array_like, optional
        Kp index.
    model : str, optional
        Neutral sheet model to use.
    mlt : array_like, optional
        Magnetic local time.
    in_coord : str, optional
        Coordinate system of the input position.
    sc2NS : Bool, optional
        Flag to return spacecraft to neutral sheet distance.

    Returns
    -------
    distance2NS : array_like
        Distance to the neutral sheet.

    """

    time = np.array(time)

    # validate and initialize parameters if not set
    if model is None:
        model = 'themis'
    else:
        model = model.lower()
    models = ['sm', 'themis', 'aen', 'den', 'fairfield', 'den_fairfield', 'lopez']
    if model not in models:
        logging.error('An invalid neutral sheet model name was used. Valid entries include: ')
        logging.error(models)
        return

    # check input coordinate system, convert to gsm if needed
    if in_coord is None:
        in_coord = 'gsm'
    else:
        in_coord = in_coord.lower()
    if in_coord == 'gsm':
        gsm_pos = pos
    else:
        gsm_pos = cotrans(time_in=time, data_in=pos, coord_in=in_coord, coord_out='gsm')

    # call the appropriate neutral sheet model
    if model == 'sm':
        distance2NS = sm_ns_model(time, gsm_pos, sc2NS=sc2NS)
    elif model == 'themis':
        distance2NS = themis_ns_model(time, gsm_pos, sc2NS=sc2NS)
    elif model == 'aen':
        distance2NS = aen_ns_model(time, gsm_pos, sc2NS=sc2NS)
    elif model == 'den':
        distance2NS = den_ns_model(time, gsm_pos, sc2NS=sc2NS)
    elif model == 'fairfield':
        distance2NS = fairfield_ns_model(time, gsm_pos, sc2NS=sc2NS)
    elif model == 'den_fairfield':
        distance2NS = den_fairfield_ns_model(time, gsm_pos, sc2NS=sc2NS)
    elif model == 'lopez':
        distance2NS = lopez_ns_model(time, gsm_pos, kp=kp, mlt=mlt, sc2NS=sc2NS)
    else:
        logging.error('Invalid neutral sheet model.')
        logging.error('Valid models are: [sm, themis, aen, den, fairfield, den_fairfield, lopez]')
        return

    return distance2NS
