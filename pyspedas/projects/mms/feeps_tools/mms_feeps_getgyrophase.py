import logging
import numpy as np
from pyspedas.projects import mms
from pyspedas import tinterpol
from pyspedas.projects.mms.feeps_tools.mms_feeps_active_eyes import mms_feeps_active_eyes
from pytplot import get, store, options, time_double


def mms_feeps_getgyrophase(trange=['2017-07-11/22:30', '2017-07-11/22:35'], probe='2', data_rate='brst', level='l2', datatype='electron'):
    """
    Calculates FEEPS gyrophase angles for electron burst data

    Notes: This is intended for use with burst mode data, but the output gyrophase product, 
           mms*_feeps_gyrophase, can be interpolated onto FEEPS burst or survey cadence
           to produce spectra

    Based on the IDL code writen by Drew Turner (10 Oct 2017): mms_feeps_getgyrophase.pro
    """
    mec_vars = mms.mec(trange=trange, probe=probe, data_rate=data_rate)
    if mec_vars is None:
        logging.error('Problem loading MEC data for calculating FEEPS gyrophase angles')

    qeci2sm = get('mms'+probe+'_mec_quat_eci_to_sm', units=False)
    qeci2bcs = get('mms'+probe+'_mec_quat_eci_to_bcs', units=False)
    rsun = get('mms'+probe+'_mec_r_sun_de421_eci', units=False)

    rsunbcs = np.zeros((len(rsun.times), 3))
    rduskbcs = np.zeros((len(rsun.times), 3))
    rdusksm = [0, 1, 0]

    for i in range(len(rsun.times)):
        q = qeci2bcs.y[i, :]
        # Quaternion rotation matrix:
        s = 1 # these quaternions are unit-qs
        R = np.array([[1 - 2*s*(q[2]**2 + q[3]**2), 2*s*(q[1]*q[2] - q[3]*q[0]), 2*s*(q[1]*q[3] + q[2]*q[0])], # ECI to BCS
            [2*s*(q[1]*q[2] + q[3]*q[0]), 1 - 2*s*(q[1]**2 + q[3]**2), 2*s*(q[2]*q[3] - q[1]*q[0])],
            [2*s*(q[1]*q[3] - q[2]*q[0]), 2*s*(q[2]*q[3] + q[1]*q[0]), 1 - 2*s*(q[1]**2 + q[2]**2)]])
        R = R.T
        rsunbcs[i, :] = np.array([R[0,0]*rsun.y[i,0] + R[1,0]*rsun.y[i,1] + R[2,0]*rsun.y[i,2], R[0,1]*rsun.y[i,0] + R[1,1]*rsun.y[i,1] + R[2,1]*rsun.y[i,2], R[0,2]*rsun.y[i,0] + R[1,2]*rsun.y[i,1] + R[2,2]*rsun.y[i,2]])

        # now make second vector for gyroplane reference, dusk direction (+Y in SM)
        q = qeci2sm.y[i, :]
        # Quaternion rotation matrix:
        s = 1 # these quaternions are unit-qs
        R2 = np.array([[1 - 2*s*(q[2]**2 + q[3]**2), 2*s*(q[1]*q[2] - q[3]*q[0]), 2*s*(q[1]*q[3] + q[2]*q[0])], # ECI to SM
        [2*s*(q[1]*q[2] + q[3]*q[0]), 1 - 2*s*(q[1]**2 + q[3]**2), 2*s*(q[2]*q[3] - q[1]*q[0])],
        [2*s*(q[1]*q[3] - q[2]*q[0]), 2*s*(q[2]*q[3] + q[1]*q[0]), 1 - 2*s*(q[1]**2 + q[2]**2)]])
        # going from SM to ECI, so invert R:
        R2 = np.linalg.inv(R2) # SM to ECI
        R2 = R2.T
        rduskeci = [R2[0,0]*rdusksm[0] + R2[1,0]*rdusksm[1] + R2[2,0]*rdusksm[2], R2[0,1]*rdusksm[0] + R2[1,1]*rdusksm[1] + R2[2,1]*rdusksm[2], R2[0,2]*rdusksm[0] + R2[1,2]*rdusksm[1] + R2[2,2]*rdusksm[2]]
        # Now convert to BCS:
        rduskbcs[i, :] = np.array([R[0,0]*rduskeci[0] + R[1,0]*rduskeci[1] + R[2,0]*rduskeci[2], R[0,1]*rduskeci[0] + R[1,1]*rduskeci[1] + R[2,1]*rduskeci[2], R[0,2]*rduskeci[0] + R[1,2]*rduskeci[1] + R[2,2]*rduskeci[2]])
    
    saved = store('mms'+probe+'_mec_r_sun_bcs', data = {'x': rsun.times, 'y': rsunbcs})
    if not saved:
        logging.error('Problem saving r_sun_bcs')

    saved = store('mms'+probe+'_mec_r_dusk_bcs', data = {'x': rsun.times, 'y': rduskbcs})
    if not saved:
        logging.error('Problem saving r_dusk_bcs')

    # Rotation matrices for FEEPS coord system (FCS) into body coordinate system (BCS):
    Ttop = np.array([[1./np.sqrt(2.), -1./np.sqrt(2.), 0], [1./np.sqrt(2.), 1./np.sqrt(2.), 0], [0, 0, 1]]).T
    Tbot = np.array([[-1./np.sqrt(2.), -1./np.sqrt(2.), 0], [-1./np.sqrt(2.), 1./np.sqrt(2.), 0], [0, 0, -1]]).T

    # Telescope vectors in FCS:
    # Electrons
    V1fcs = [0.347, -0.837, 0.423]
    V2fcs = [0.347, -0.837, -0.423]
    V3fcs = [0.837, -0.347, 0.423]
    V4fcs = [0.837, -0.347, -0.423]
    V5fcs = [-0.087, 0.000, 0.996]
    V9fcs = [0.837, 0.347, 0.423]
    V10fcs = [0.837, 0.347, -0.423]
    V11fcs = [0.347, 0.837, 0.423]
    V12fcs = [0.347, 0.837, -0.423]
    # Ions
    V6fcs = [0.104, 0.180, 0.978]
    V7fcs = [0.654, -0.377, 0.656]
    V8fcs = [0.654, -0.377, -0.656]

    # Now telescope vectors in Body Coordinate System:
    #   Factors of -1 account for 180 deg shift between particle velocity and telescope normal direction:
    # Top:
    Vt1bcs = [-1.*(Ttop[0,0]*V1fcs[0] + Ttop[1,0]*V1fcs[1] + Ttop[2,0]*V1fcs[2]), 
            -1.*(Ttop[0,1]*V1fcs[0] + Ttop[1,1]*V1fcs[1] + Ttop[2,1]*V1fcs[2]), 
            -1.*(Ttop[0,2]*V1fcs[0] + Ttop[1,2]*V1fcs[1] + Ttop[2,2]*V1fcs[2])]
    Vt2bcs = [-1.*(Ttop[0,0]*V2fcs[0] + Ttop[1,0]*V2fcs[1] + Ttop[2,0]*V2fcs[2]), 
            -1.*(Ttop[0,1]*V2fcs[0] + Ttop[1,1]*V2fcs[1] + Ttop[2,1]*V2fcs[2]), 
            -1.*(Ttop[0,2]*V2fcs[0] + Ttop[1,2]*V2fcs[1] + Ttop[2,2]*V2fcs[2])]
    Vt3bcs = [-1.*(Ttop[0,0]*V3fcs[0] + Ttop[1,0]*V3fcs[1] + Ttop[2,0]*V3fcs[2]), 
            -1.*(Ttop[0,1]*V3fcs[0] + Ttop[1,1]*V3fcs[1] + Ttop[2,1]*V3fcs[2]), 
            -1.*(Ttop[0,2]*V3fcs[0] + Ttop[1,2]*V3fcs[1] + Ttop[2,2]*V3fcs[2])]
    Vt4bcs = [-1.*(Ttop[0,0]*V4fcs[0] + Ttop[1,0]*V4fcs[1] + Ttop[2,0]*V4fcs[2]), 
            -1.*(Ttop[0,1]*V4fcs[0] + Ttop[1,1]*V4fcs[1] + Ttop[2,1]*V4fcs[2]), 
            -1.*(Ttop[0,2]*V4fcs[0] + Ttop[1,2]*V4fcs[1] + Ttop[2,2]*V4fcs[2])]
    Vt5bcs = [-1.*(Ttop[0,0]*V5fcs[0] + Ttop[1,0]*V5fcs[1] + Ttop[2,0]*V5fcs[2]), 
            -1.*(Ttop[0,1]*V5fcs[0] + Ttop[1,1]*V5fcs[1] + Ttop[2,1]*V5fcs[2]), 
            -1.*( Ttop[0,2]*V5fcs[0] + Ttop[1,2]*V5fcs[1] + Ttop[2,2]*V5fcs[2])]
    Vt6bcs = [-1.*(Ttop[0,0]*V6fcs[0] + Ttop[1,0]*V6fcs[1] + Ttop[2,0]*V6fcs[2]), 
            -1.*(Ttop[0,1]*V6fcs[0] + Ttop[1,1]*V6fcs[1] + Ttop[2,1]*V6fcs[2]), 
            -1.*(Ttop[0,2]*V6fcs[0] + Ttop[1,2]*V6fcs[1] + Ttop[2,2]*V6fcs[2])]
    Vt7bcs = [-1.*(Ttop[0,0]*V7fcs[0] + Ttop[1,0]*V7fcs[1] + Ttop[2,0]*V7fcs[2]), 
            -1.*(Ttop[0,1]*V7fcs[0] + Ttop[1,1]*V7fcs[1] + Ttop[2,1]*V7fcs[2]), 
            -1.*(Ttop[0,2]*V7fcs[0] + Ttop[1,2]*V7fcs[1] + Ttop[2,2]*V7fcs[2])]
    Vt8bcs = [-1.*(Ttop[0,0]*V8fcs[0] + Ttop[1,0]*V8fcs[1] + Ttop[2,0]*V8fcs[2]), 
            -1.*( Ttop[0,1]*V8fcs[0] + Ttop[1,1]*V8fcs[1] + Ttop[2,1]*V8fcs[2]), 
            -1.*(Ttop[0,2]*V8fcs[0] + Ttop[1,2]*V8fcs[1] + Ttop[2,2]*V8fcs[2])]
    Vt9bcs = [-1.*(Ttop[0,0]*V9fcs[0] + Ttop[1,0]*V9fcs[1] + Ttop[2,0]*V9fcs[2]), 
            -1.*(Ttop[0,1]*V9fcs[0] + Ttop[1,1]*V9fcs[1] + Ttop[2,1]*V9fcs[2]), 
            -1.*(Ttop[0,2]*V9fcs[0] + Ttop[1,2]*V9fcs[1] + Ttop[2,2]*V9fcs[2])]
    Vt10bcs = [-1.*(Ttop[0,0]*V10fcs[0] + Ttop[1,0]*V10fcs[1] + Ttop[2,0]*V10fcs[2]), 
            -1.*(Ttop[0,1]*V10fcs[0] + Ttop[1,1]*V10fcs[1] + Ttop[2,1]*V10fcs[2]), 
            -1.*(Ttop[0,2]*V10fcs[0] + Ttop[1,2]*V10fcs[1] + Ttop[2,2]*V10fcs[2])]
    Vt11bcs = [-1.*(Ttop[0,0]*V11fcs[0] + Ttop[1,0]*V11fcs[1] + Ttop[2,0]*V11fcs[2]), 
            -1.*(Ttop[0,1]*V11fcs[0] + Ttop[1,1]*V11fcs[1] + Ttop[2,1]*V11fcs[2]), 
            -1.*(Ttop[0,2]*V11fcs[0] + Ttop[1,2]*V11fcs[1] + Ttop[2,2]*V11fcs[2])]
    Vt12bcs = [-1.*(Ttop[0,0]*V12fcs[0] + Ttop[1,0]*V12fcs[1] + Ttop[2,0]*V12fcs[2]), 
            -1.*(Ttop[0,1]*V12fcs[0] + Ttop[1,1]*V12fcs[1] + Ttop[2,1]*V12fcs[2]), 
            -1.*(Ttop[0,2]*V12fcs[0] + Ttop[1,2]*V12fcs[1] + Ttop[2,2]*V12fcs[2])]
    # Bottom:
    Vb1bcs = [-1.*(Tbot[0,0]*V1fcs[0] + Tbot[1,0]*V1fcs[1] + Tbot[2,0]*V1fcs[2]), 
            -1.*(Tbot[0,1]*V1fcs[0] + Tbot[1,1]*V1fcs[1] + Tbot[2,1]*V1fcs[2]), 
            -1.*(Tbot[0,2]*V1fcs[0] + Tbot[1,2]*V1fcs[1] + Tbot[2,2]*V1fcs[2])]
    Vb2bcs = [-1.*(Tbot[0,0]*V2fcs[0] + Tbot[1,0]*V2fcs[1] + Tbot[2,0]*V2fcs[2]), 
            -1.*(Tbot[0,1]*V2fcs[0] + Tbot[1,1]*V2fcs[1] + Tbot[2,1]*V2fcs[2]), 
            -1.*(Tbot[0,2]*V2fcs[0] + Tbot[1,2]*V2fcs[1] + Tbot[2,2]*V2fcs[2])]
    Vb3bcs = [-1.*(Tbot[0,0]*V3fcs[0] + Tbot[1,0]*V3fcs[1] + Tbot[2,0]*V3fcs[2]), 
            -1.*(Tbot[0,1]*V3fcs[0] + Tbot[1,1]*V3fcs[1] + Tbot[2,1]*V3fcs[2]), 
            -1.*(Tbot[0,2]*V3fcs[0] + Tbot[1,2]*V3fcs[1] + Tbot[2,2]*V3fcs[2])]
    Vb4bcs = [-1.*(Tbot[0,0]*V4fcs[0] + Tbot[1,0]*V4fcs[1] + Tbot[2,0]*V4fcs[2]), 
            -1.*(Tbot[0,1]*V4fcs[0] + Tbot[1,1]*V4fcs[1] + Tbot[2,1]*V4fcs[2]), 
            -1.*(Tbot[0,2]*V4fcs[0] + Tbot[1,2]*V4fcs[1] + Tbot[2,2]*V4fcs[2])]
    Vb5bcs = [-1.*(Tbot[0,0]*V5fcs[0] + Tbot[1,0]*V5fcs[1] + Tbot[2,0]*V5fcs[2]), 
            -1.*(Tbot[0,1]*V5fcs[0] + Tbot[1,1]*V5fcs[1] + Tbot[2,1]*V5fcs[2]), 
            -1.*(Tbot[0,2]*V5fcs[0] + Tbot[1,2]*V5fcs[1] + Tbot[2,2]*V5fcs[2])]
    Vb6bcs = [-1.*(Tbot[0,0]*V6fcs[0] + Tbot[1,0]*V6fcs[1] + Tbot[2,0]*V6fcs[2]), 
            -1.*(Tbot[0,1]*V6fcs[0] + Tbot[1,1]*V6fcs[1] + Tbot[2,1]*V6fcs[2]), 
            -1.*( Tbot[0,2]*V6fcs[0] + Tbot[1,2]*V6fcs[1] + Tbot[2,2]*V6fcs[2])]
    Vb7bcs = [-1.*(Tbot[0,0]*V7fcs[0] + Tbot[1,0]*V7fcs[1] + Tbot[2,0]*V7fcs[2]), 
            -1.*(Tbot[0,1]*V7fcs[0] + Tbot[1,1]*V7fcs[1] + Tbot[2,1]*V7fcs[2]), 
            -1.*(Tbot[0,2]*V7fcs[0] + Tbot[1,2]*V7fcs[1] + Tbot[2,2]*V7fcs[2])]
    Vb8bcs = [-1.*(Tbot[0,0]*V8fcs[0] + Tbot[1,0]*V8fcs[1] + Tbot[2,0]*V8fcs[2]), 
            -1.*(Tbot[0,1]*V8fcs[0] + Tbot[1,1]*V8fcs[1] + Tbot[2,1]*V8fcs[2]), 
            -1.*(Tbot[0,2]*V8fcs[0] + Tbot[1,2]*V8fcs[1] + Tbot[2,2]*V8fcs[2])]
    Vb9bcs = [-1.*(Tbot[0,0]*V9fcs[0] + Tbot[1,0]*V9fcs[1] + Tbot[2,0]*V9fcs[2]), 
            -1.*(Tbot[0,1]*V9fcs[0] + Tbot[1,1]*V9fcs[1] + Tbot[2,1]*V9fcs[2]), 
            -1.*(Tbot[0,2]*V9fcs[0] + Tbot[1,2]*V9fcs[1] + Tbot[2,2]*V9fcs[2])]
    Vb10bcs = [-1.*(Tbot[0,0]*V10fcs[0] + Tbot[1,0]*V10fcs[1] + Tbot[2,0]*V10fcs[2]), 
            -1.*(Tbot[0,1]*V10fcs[0] + Tbot[1,1]*V10fcs[1] + Tbot[2,1]*V10fcs[2]), 
            -1.*(Tbot[0,2]*V10fcs[0] + Tbot[1,2]*V10fcs[1] + Tbot[2,2]*V10fcs[2])]
    Vb11bcs = [-1.*(Tbot[0,0]*V11fcs[0] + Tbot[1,0]*V11fcs[1] + Tbot[2,0]*V11fcs[2]), 
            -1.*(Tbot[0,1]*V11fcs[0] + Tbot[1,1]*V11fcs[1] + Tbot[2,1]*V11fcs[2]), 
            -1.*(Tbot[0,2]*V11fcs[0] + Tbot[1,2]*V11fcs[1] + Tbot[2,2]*V11fcs[2])]
    Vb12bcs = [-1.*(Tbot[0,0]*V12fcs[0] + Tbot[1,0]*V12fcs[1] + Tbot[2,0]*V12fcs[2]), 
            -1.*(Tbot[0,1]*V12fcs[0] + Tbot[1,1]*V12fcs[1] + Tbot[2,1]*V12fcs[2]), 
            -1.*(Tbot[0,2]*V12fcs[0] + Tbot[1,2]*V12fcs[1] + Tbot[2,2]*V12fcs[2])]

    fgm_vars = mms.fgm(trange=[time_double(trange[0])-600, time_double(trange[1])+600], probe=probe, data_rate='srvy')
    if fgm_vars is None:
        logging.error('Problem loading FGM vars for calculating FEEPS gyrophase angles')

    # interpolate the FGM var to the MEC var timestamps
    tinterpol('mms'+probe+'_fgm_b_bcs_srvy_l2_bvec', 'mms'+probe+'_mec_r_sun_bcs', newname='mms'+probe+'_fgm_b_bcs_srvy_l2_bvec_int')

    B = get('mms'+probe+'_fgm_b_bcs_srvy_l2_bvec_int')

    # Now calculate gyrophase
    # Telescope vectors perp to B:
    Tperp = np.zeros((len(rsunbcs[:, 0]), 3, 24))

    # Gyrophase:
    phi = np.zeros((len(rsunbcs[:, 0]), 24))

    for i in range(len(rsunbcs[:, 0])):
        uB = B.y[i,:]/np.sqrt(B.y[i,0]**2 + B.y[i,1]**2 + B.y[i,2]**2)
        # Sun vector perp to B:
        Sperp = np.cross(np.cross(uB, rsunbcs[i, :]/np.sqrt(np.nansum(rsunbcs[i, :]**2))), uB)
        # Dusk vector perp to B:
        Dperp = np.cross(np.cross(uB, rduskbcs[i, :]/np.sqrt(np.nansum(rduskbcs[i, :]**2))), uB)
        Tperp[i, :, 0] = np.cross(np.cross(uB, Vt1bcs), uB)
        Tperp[i, :, 1] = np.cross(np.cross(uB, Vt2bcs), uB)
        Tperp[i, :, 2] = np.cross(np.cross(uB, Vt3bcs), uB)
        Tperp[i, :, 3] = np.cross(np.cross(uB, Vt4bcs), uB)
        Tperp[i, :, 4] = np.cross(np.cross(uB, Vt5bcs), uB)
        Tperp[i, :, 5] = np.cross(np.cross(uB, Vt6bcs), uB)
        Tperp[i, :, 6] = np.cross(np.cross(uB, Vt7bcs), uB)
        Tperp[i, :, 7] = np.cross(np.cross(uB, Vt8bcs), uB)
        Tperp[i, :, 8] = np.cross(np.cross(uB, Vt9bcs), uB)
        Tperp[i, :, 9] = np.cross(np.cross(uB, Vt10bcs), uB)
        Tperp[i, :, 10] = np.cross(np.cross(uB, Vt11bcs), uB)
        Tperp[i, :, 11] = np.cross(np.cross(uB, Vt12bcs), uB)
        Tperp[i, :, 12] = np.cross(np.cross(uB, Vb1bcs), uB)
        Tperp[i, :, 13] = np.cross(np.cross(uB, Vb2bcs), uB)
        Tperp[i, :, 14] = np.cross(np.cross(uB, Vb3bcs), uB)
        Tperp[i, :, 15] = np.cross(np.cross(uB, Vb4bcs), uB)
        Tperp[i, :, 16] = np.cross(np.cross(uB, Vb5bcs), uB)
        Tperp[i, :, 17] = np.cross(np.cross(uB, Vb6bcs), uB)
        Tperp[i, :, 18] = np.cross(np.cross(uB, Vb7bcs), uB)
        Tperp[i, :, 19] = np.cross(np.cross(uB, Vb8bcs), uB)
        Tperp[i, :, 20] = np.cross(np.cross(uB, Vb9bcs), uB)
        Tperp[i, :, 21] = np.cross(np.cross(uB, Vb10bcs), uB)
        Tperp[i, :, 22] = np.cross(np.cross(uB, Vb11bcs), uB)
        Tperp[i, :, 23] = np.cross(np.cross(uB, Vb12bcs), uB)

        for j in range(24):
            th1 = np.arccos(np.nansum(Tperp[i,:,j] * Sperp)/(np.sqrt(np.nansum(Tperp[i,:,j]**2))*np.sqrt(np.nansum(Sperp**2))))
            th2 = np.arccos(np.nansum(Tperp[i,:,j] * Dperp)/(np.sqrt(np.nansum(Tperp[i,:,j]**2))*np.sqrt(np.nansum(Dperp**2))))
            # strip the units
            th1 = th1.value
            th2 = th2.value
            if th1 <= np.pi/2.0 and th2 < np.pi/2:
                phi[i, j] = 2*np.pi - th1
            if th1 < np.pi/2.0 and th2 >= np.pi/2.0:
                phi[i, j] = th1
            if th1 > np.pi/2.0 and th2 <= np.pi/2.0:
                phi[i, j] = 270.0*np.pi/180.0 - th2
            if th1 >= np.pi/2.0 and th2 > np.pi/2.0:
                phi[i, j] = th1
    
    saved = store('mms'+probe+'_epd_feeps_'+data_rate+'_gyrophase', data={'x': rsun.times, 'y': phi*180./np.pi})
    if not saved:
        logging.error('Problem saving gyrophase angles')
        return

    options('mms'+probe+'_epd_feeps_'+data_rate+'_gyrophase', 'yrange', [0, 360.0])

    # Gyrophase always returns on time stamps from MEC data, get those closest to FEEPS time stamps:
    eyes = mms_feeps_active_eyes(trange, probe, data_rate, datatype, level)
    sensor_types = ['top', 'bottom']

    feepst = get('mms'+probe+'_epd_feeps_'+data_rate+'_'+level+'_'+datatype+'_spinsectnum')

    indt = np.zeros(len(feepst.times), dtype='int32')
    gpd = get('mms'+probe+'_epd_feeps_'+data_rate+'_gyrophase')

    for i in range(len(feepst.times)):
        indt[i] = np.argwhere(np.abs(gpd.times - feepst.times[i]) == np.min(np.abs(gpd.times - feepst.times[i]))).flatten()[0]

    # Gyrophase always returns all 24 FEEPS telescopes, downselect based on species:
    iT = np.array([np.array(eyes[sensor_types[0]])-1, np.array(eyes[sensor_types[0]])+11]).flatten().tolist()
    gp_data = np.zeros((len(gpd.times[indt]), len(iT)))

    #return (iT, gp_data, gpd)
    for i in range(len(iT)):
        gp_data[:, i] = gpd.y[indt, iT[i]]
    
    saved = store('mms'+probe+'_epd_feeps_'+data_rate+'_'+level+'_'+datatype+'_gyrophase', data = {'x': gpd.times[indt], 'y': gp_data})

    if saved:
        options('mms'+probe+'_epd_feeps_'+data_rate+'_'+level+'_'+datatype+'_gyrophase', 'yrange', [0.0, 360.0])
        return 'mms'+probe+'_epd_feeps_'+data_rate+'_'+level+'_'+datatype+'_gyrophase'
