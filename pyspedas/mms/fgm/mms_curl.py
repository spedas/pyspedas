
import math
import numpy as np
from pytplot import get_data, store_data, options
from pyspedas import tinterpol

def mms_curl(fields=None, positions=None, suffix=''):
    """
    This function applies the curlometer technique to MMS FGM data
    
    Parameters
    ----------
        fields : list of str
            List of tplot variables containing the B-field for each spacecraft 
            (in GSE coordinates)

        positions : list of str
            List of tplot variables containing the S/C position vectors for 
            each spacecraft (also GSE coordinates) 

        suffix: str
            The tplot variable names will be given this suffix.  By default, 
            no suffix is added.

    Notes
    ----------
        The input B-field data and position data are required to be in 
        GSE coordinates
 
        Based on the original mms_curl, written in IDL, by Jonathan Eastwood 

        For more info on this method, see:
          Chanteur, G., Spatial Interpolation for Four Spacecraft: Theory, 
          Chapter 14 of Analysis methods for multi-spacecraft data, G. 
          Paschmann and P. W. Daly (Eds.) ISSI Scientific Report SR-001. 

    Returns
    ----------
        List of tplot variables created

    """
    if fields is None or positions is None:
        print('Error: B-field and spacecraft position keywords required.')
        return

    if len(fields) != 4 or len(positions) != 4:
        print('Error, fields and positions keywords should be specified as 4-element arrays containing the tplot variable name for the field and position variables')
        return
        
    # *********************************************************
    # Magnetic Field
    # *********************************************************
    # interpolate the magnetic field data all onto the same timeline (MMS1):
    # should be in GSE coordinates
    tinterpol(fields[1], fields[0], newname=fields[1] + '_i')
    tinterpol(fields[2], fields[0], newname=fields[2] + '_i')
    tinterpol(fields[3], fields[0], newname=fields[3] + '_i')

    # interpolate the definitive ephemeris onto the magnetic field timeseries
    # should be in GSE coordinates
    tinterpol(positions[0], fields[0], newname=positions[0] + '_i')
    tinterpol(positions[1], fields[0], newname=positions[1] + '_i')
    tinterpol(positions[2], fields[0], newname=positions[2] + '_i')
    tinterpol(positions[3], fields[0], newname=positions[3] + '_i')

    m0 = 4.0*math.pi*1e-7

    mms1_bfield = get_data(fields[0])
    mms2_bfield = get_data(fields[1] + '_i')
    mms3_bfield = get_data(fields[2] + '_i')
    mms4_bfield = get_data(fields[3] + '_i')

    if mms1_bfield is None:
        print('Error, B-field variable is missing: ' + fields[0])
        return
    elif mms2_bfield is None:
        print('Error, B-field variable is missing: ' + fields[1] + '_i')
        return
    elif mms3_bfield is None:
        print('Error, B-field variable is missing: ' + fields[2] + '_i')
        return
    elif mms4_bfield is None:
        print('Error, B-field variable is missing: ' + fields[3] + '_i')
        return

    timesb1, datab1 = mms1_bfield
    timesb2, datab2 = mms2_bfield
    timesb3, datab3 = mms3_bfield
    timesb4, datab4 = mms4_bfield

    # extract the vector
    b1 = datab1[:, 0:3]
    b2 = datab2[:, 0:3]
    b3 = datab3[:, 0:3]
    b4 = datab4[:, 0:3]

    mms1_pos = get_data(positions[0] + '_i')
    mms2_pos = get_data(positions[1] + '_i')
    mms3_pos = get_data(positions[2] + '_i')
    mms4_pos = get_data(positions[3] + '_i')

    if mms1_pos is None:
        print('Error, S/C position variable is missing: ' + positions[0] + '_i')
        return
    elif mms2_pos is None:
        print('Error, S/C position variable is missing: ' + positions[1] + '_i')
        return
    elif mms3_pos is None:
        print('Error, S/C position variable is missing: ' + positions[2] + '_i')
        return
    elif mms4_pos is None:
        print('Error, S/C position variable is missing: ' + positions[3] + '_i')
        return

    timesp1, p1 = mms1_pos
    timesp2, p2 = mms2_pos
    timesp3, p3 = mms3_pos
    timesp4, p4 = mms4_pos

    divb = np.zeros([len(timesb1), 5])
    baryb = np.zeros([len(timesb1), 3])
    baryb2 = np.zeros([len(timesb1), 3])
    baryb3 = np.zeros([len(timesb1), 3])
    baryb4 = np.zeros([len(timesb1), 3])

    jtotal = np.zeros([len(timesb1), 4])
    btotal = np.zeros([len(timesb1), 1])
    jparallel = np.zeros([len(timesb1), 1])
    jperpvec = np.zeros([len(timesb1), 4])
    alphaparallel = np.zeros([len(timesb1), 1])
    alpha = np.zeros([len(timesb1), 1])

    # leave as a loop for now because you have to construct and manipulate a matrix for each time step.
    for i, time in enumerate(timesb1):
        p12 = p2[i, 0:3]-p1[i, 0:3]
        p13 = p3[i, 0:3]-p1[i, 0:3]
        p14 = p4[i, 0:3]-p1[i, 0:3]

        k2 = np.cross(p13, p14)*(1/(np.matmul(p12, np.transpose(np.cross(p13, p14)))))
        k3 = np.cross(p12, p14)*(1/(np.matmul(p13, np.transpose(np.cross(p12, p14)))))
        k4 = np.cross(p12, p13)*(1/(np.matmul(p14, np.transpose(np.cross(p12, p13)))))

        k1 = 0-k4-k3-k2

        curlmag = np.cross(k1, b1[i, :])+np.cross(k2, b2[i, :])+np.cross(k3, b3[i, :])+np.cross(k4, b4[i, :])
        divergence = np.matmul(b1[i, :], k1) + np.matmul(b2[i, :], k2) + np.matmul(b3[i, :], k3) + np.matmul(b4[i, :], k4)

        gradbx = b1[i, 0]*k1 + b2[i, 0]*k2 + b3[i, 0]*k3 + b4[i, 0]*k4
        gradby = b1[i, 1]*k1 + b2[i, 1]*k2 + b3[i, 1]*k3 + b4[i, 1]*k4
        gradbz = b1[i, 2]*k1 + b2[i, 2]*k2 + b3[i, 2]*k3 + b4[i, 2]*k4

        barycentre = (p1[i, 0:3] + p2[i, 0:3] + p3[i, 0:3] + p4[i, 0:3])/4.0

        # and here is the field at the barycentre (calculate 4 ways)
        baryb[i, 0] = b1[i, 0] + np.sum(gradbx*(barycentre-p1[i, 0:3]))
        baryb[i, 1] = b1[i, 1] + np.sum(gradby*(barycentre-p1[i, 0:3]))
        baryb[i, 2] = b1[i, 2] + np.sum(gradbz*(barycentre-p1[i, 0:3]))

        baryb2[i, 0] = b2[i, 0] + np.sum(gradbx*(barycentre-p2[i, 0:3]))
        baryb2[i, 1] = b2[i, 1] + np.sum(gradby*(barycentre-p2[i, 0:3]))
        baryb2[i, 2] = b2[i, 2] + np.sum(gradbz*(barycentre-p2[i, 0:3]))

        baryb3[i, 0] = b3[i, 0] + np.sum(gradbx*(barycentre-p3[i, 0:3]))
        baryb3[i, 1] = b3[i, 1] + np.sum(gradby*(barycentre-p3[i, 0:3]))
        baryb3[i, 2] = b3[i, 2] + np.sum(gradbz*(barycentre-p3[i, 0:3]))

        baryb4[i, 0] = b4[i, 0] + np.sum(gradbx*(barycentre-p4[i, 0:3]))
        baryb4[i, 1] = b4[i, 1] + np.sum(gradby*(barycentre-p4[i, 0:3]))
        baryb4[i, 2] = b4[i, 2] + np.sum(gradbz*(barycentre-p4[i, 0:3]))

        # (these above all agree so this is the magnetic field at the barycentre)
        divb[i, 0] = time
        divb[i, 1] = divergence
        divb[i, 2] = curlmag[0]
        divb[i, 3] = curlmag[1]
        divb[i, 4] = curlmag[2]

        # the cross product of the calculated curl and the sample field times 1e-21 (SI), divided by m0

        # curl is in nT/km, nT/km*1e-12 = T/m
        # field is in nT, nT*1e-9 = T
        # j is curl B / m0 (curl B = m0*j)
        # use the magnetic field at the barycentre

        # compute the current components and total specifically
        jtotal[i, 0:3] = 1e-12*divb[i, 2:5]/m0
        jtotal[i, 3] = np.sqrt(jtotal[i, 0]**2+jtotal[i, 1]**2+jtotal[i, 2]**2)

        # compute the parallel and perpendicular components of the current
        btotal[i] = np.sqrt(np.dot(baryb[i, 0:3], baryb[i, 0:3]))

        # parallel is J.B/|B|
        jparallel[i] = np.dot(jtotal[i, 0:3], baryb[i, 0:3])/btotal[i]
        jparallel[i] = jparallel[i][0]

        # perp is J - J// B/|B| (components and total perpendicular current)
        jperpvec[i, 0:3] = jtotal[i, 0:3] - (jparallel[i]*baryb[i, 0:3])/btotal[i]
        jperpvec[i, 3] = np.sqrt(jperpvec[i, 0]**2 + jperpvec[i, 1]**2 + jperpvec[i, 2]**2)

        # alpha parameter
        alphaparallel[i] = np.abs(jparallel[i])/(1e-9*btotal[i])
        alpha[i] = np.abs(jtotal[i, 3])/(1e-9*btotal[i])

    # create the output variables
    store_data('baryb' + suffix, data={'x': timesb1, 'y': baryb})
    store_data('curlB' + suffix, data={'x': timesb1, 'y': divb[:, 2:5]})
    store_data('divB' + suffix, data={'x': timesb1, 'y': divb[:, 1]})
    store_data('jtotal' + suffix, data={'x': timesb1, 'y': jtotal[:, 0:3]})
    store_data('jpar' + suffix, data={'x': timesb1, 'y': jparallel})
    store_data('jperp' + suffix, data={'x': timesb1, 'y': jperpvec[:, 0:3]})
    store_data('alpha' + suffix, data={'x': timesb1, 'y': alpha})
    store_data('alphaparallel' + suffix, data={'x': timesb1, 'y': alphaparallel})

    # set some options
    options('baryb' + suffix, 'ytitle', 'baryb')
    options('baryb' + suffix, 'ysubtitle', '[nT]')
    options('divB' + suffix, 'ytitle', 'div(B)')
    options('divB' + suffix, 'ysubtitle', '[nT/km]')
    options('curlB' + suffix, 'ytitle', 'curl(B)')
    options('curlB' + suffix, 'ysubtitle', '[nT/km]')
    options('curlB' + suffix, 'Color', ['b', 'g', 'r'])
    options('curlB' + suffix, 'legend_names', ['delBx', 'delBy', 'delBz'])
    options('jtotal' + suffix, 'ytitle', 'J')
    options('jtotal' + suffix, 'ysubtitle', '[A/m^2]')
    options('jtotal' + suffix, 'Color', ['b', 'g', 'r'])
    options('jtotal' + suffix, 'legend_names', ['Jx', 'Jy', 'Jz'])
    options('jperp' + suffix, 'ytitle', 'Jperp')
    options('jperp' + suffix, 'ysubtitle', '[A/m^2]')
    options('jperp' + suffix, 'Color', ['b', 'g', 'r'])
    options('jperp' + suffix, 'legend_names', ['Jperpx', 'Jperpy', 'Jperpz'])
    options('jpar' + suffix, 'ytitle', 'Jparallel')
    options('jpar' + suffix, 'ysubtitle', '[A/m^2]')

    return ['baryb', 'curlB', 'divB', 'jtotal', 'jpar', 'jperp', 'alpha', 'alphaparallel']