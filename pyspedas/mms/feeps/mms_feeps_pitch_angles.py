
from pyspedas.mms.feeps.mms_feeps_active_eyes import mms_feeps_active_eyes
from pyspedas import mms_load_fgm
from pytplot import get_data, store_data
import numpy as np
import math

def mms_feeps_pitch_angles(trange=None, probe='1', level='l2', data_rate='srvy', datatype='electron', suffix=''):
    """
    This function calculates the FEEPS pitch angles from the B-field data

    Returns:
        List of tplot variables created.
    """

    # get the times from the currently loaded FEEPS data
    times, pa_data = get_data('mms'+probe+'_epd_feeps_'+data_rate+'_'+level+'_'+datatype+'_pitch_angle'+suffix)

    if times is not None:
        if trange is None:
            trange = [float(times.min()), float(times.max())]

    eyes = mms_feeps_active_eyes(trange, probe, data_rate, datatype, level)

    # need the B-field data
    mms_load_fgm(trange=trange, probe=probe, data_rate=data_rate)

    btimes, Bbcs = get_data('mms'+probe+'_fgm_b_bcs_srvy_l2')


    nbins = 13 # number of pitch angle bins; 10 deg = 17 bins, 15 deg = 13 bins
    dpa = 180.0/nbins # delta-pitch angle for each bin

    # Rotation matrices for FEEPS coord system (FCS) into body coordinate system (BCS):
    Ttop = [[1./np.sqrt(2.), -1./np.sqrt(2.), 0], [1./np.sqrt(2.), 1./np.sqrt(2.), 0], [0, 0, 1]]
    Tbot = [[-1./np.sqrt(2.), -1./np.sqrt(2.), 0], [-1./np.sqrt(2.), 1./np.sqrt(2.), 0], [0, 0, -1]]

    # Telescope vectors in FCS:
    V1fcs = [0.347, -0.837, 0.423]
    V2fcs = [0.347, -0.837, -0.423]
    V3fcs = [0.837, -0.347, 0.423]
    V4fcs = [0.837, -0.347, -0.423]
    V5fcs = [-0.087, 0.000, 0.996]
    V6fcs = [0.104, 0.180, 0.978]
    V7fcs = [0.654, -0.377, 0.656]
    V8fcs = [0.654, -0.377, -0.656]
    V9fcs = [0.837, 0.347, 0.423]
    V10fcs = [0.837, 0.347, -0.423]
    V11fcs = [0.347, 0.837, 0.423]
    V12fcs = [0.347, 0.837, -0.423]

    if datatype is 'electron':
        pas = np.empty([len(btimes), 18]) # pitch angles for each eye at eaceh time

        # Telescope vectors in Body Coordinate System:
        #   Factors of -1 account for 180 deg shift between particle velocity and telescope normal direction:
        # Top:
        Vt1bcs = [-1.*(Ttop[0][0]*V1fcs[0] + Ttop[0][1]*V1fcs[1] + Ttop[0][2]*V1fcs[2]), 
          -1.*(Ttop[1][0]*V1fcs[0] + Ttop[1][1]*V1fcs[1] + Ttop[1][2]*V1fcs[2]), 
          -1.*(Ttop[2][0]*V1fcs[0] + Ttop[2][1]*V1fcs[1] + Ttop[2][2]*V1fcs[2])]
        Vt2bcs = [-1.*(Ttop[0][0]*V2fcs[0] + Ttop[0][1]*V2fcs[1] + Ttop[0][2]*V2fcs[2]), 
          -1.*(Ttop[1][0]*V2fcs[0] + Ttop[1][1]*V2fcs[1] + Ttop[1][2]*V2fcs[2]), 
          -1.*(Ttop[2][0]*V2fcs[0] + Ttop[2][1]*V2fcs[1] + Ttop[2][2]*V2fcs[2])]
        Vt3bcs = [-1.*(Ttop[0][0]*V3fcs[0] + Ttop[0][1]*V3fcs[1] + Ttop[0][2]*V3fcs[2]), 
          -1.*(Ttop[1][0]*V3fcs[0] + Ttop[1][1]*V3fcs[1] + Ttop[1][2]*V3fcs[2]), 
          -1.*(Ttop[2][0]*V3fcs[0] + Ttop[2][1]*V3fcs[1] + Ttop[2][2]*V3fcs[2])]
        Vt4bcs = [-1.*(Ttop[0][0]*V4fcs[0] + Ttop[0][1]*V4fcs[1] + Ttop[0][2]*V4fcs[2]), 
          -1.*(Ttop[1][0]*V4fcs[0] + Ttop[1][1]*V4fcs[1] + Ttop[1][2]*V4fcs[2]), 
          -1.*(Ttop[2][0]*V4fcs[0] + Ttop[2][1]*V4fcs[1] + Ttop[2][2]*V4fcs[2])]
        Vt5bcs = [-1.*(Ttop[0][0]*V5fcs[0] + Ttop[0][1]*V5fcs[1] + Ttop[0][2]*V5fcs[2]), 
          -1.*(Ttop[1][0]*V5fcs[0] + Ttop[1][1]*V5fcs[1] + Ttop[1][2]*V5fcs[2]), 
          -1.*( Ttop[2][0]*V5fcs[0] + Ttop[2][1]*V5fcs[1] + Ttop[2][2]*V5fcs[2])]
        Vt9bcs = [-1.*(Ttop[0][0]*V9fcs[0] + Ttop[0][1]*V9fcs[1] + Ttop[0][2]*V9fcs[2]), 
          -1.*(Ttop[1][0]*V9fcs[0] + Ttop[1][1]*V9fcs[1] + Ttop[1][2]*V9fcs[2]), 
          -1.*(Ttop[2][0]*V9fcs[0] + Ttop[2][1]*V9fcs[1] + Ttop[2][2]*V9fcs[2])]
        Vt10bcs = [-1.*(Ttop[0][0]*V10fcs[0] + Ttop[0][1]*V10fcs[1] + Ttop[0][2]*V10fcs[2]), 
          -1.*(Ttop[1][0]*V10fcs[0] + Ttop[1][1]*V10fcs[1] + Ttop[1][2]*V10fcs[2]), 
          -1.*(Ttop[2][0]*V10fcs[0] + Ttop[2][1]*V10fcs[1] + Ttop[2][2]*V10fcs[2])]
        Vt11bcs = [-1.*(Ttop[0][0]*V11fcs[0] + Ttop[0][1]*V11fcs[1] + Ttop[0][2]*V11fcs[2]), 
          -1.*(Ttop[1][0]*V11fcs[0] + Ttop[1][1]*V11fcs[1] + Ttop[1][2]*V11fcs[2]), 
          -1.*(Ttop[2][0]*V11fcs[0] + Ttop[2][1]*V11fcs[1] + Ttop[2][2]*V11fcs[2])]
        Vt12bcs = [-1.*(Ttop[0][0]*V12fcs[0] + Ttop[0][1]*V12fcs[1] + Ttop[0][2]*V12fcs[2]), 
          -1.*(Ttop[1][0]*V12fcs[0] + Ttop[1][1]*V12fcs[1] + Ttop[1][2]*V12fcs[2]), 
          -1.*(Ttop[2][0]*V12fcs[0] + Ttop[2][1]*V12fcs[1] + Ttop[2][2]*V12fcs[2])]
        # Bottom:
        Vb1bcs = [-1.*(Tbot[0][0]*V1fcs[0] + Tbot[0][1]*V1fcs[1] + Tbot[0][2]*V1fcs[2]), 
          -1.*(Tbot[1][0]*V1fcs[0] + Tbot[1][1]*V1fcs[1] + Tbot[1][2]*V1fcs[2]), 
          -1.*(Tbot[2][0]*V1fcs[0] + Tbot[2][1]*V1fcs[1] + Tbot[2][2]*V1fcs[2])]
        Vb2bcs = [-1.*(Tbot[0][0]*V2fcs[0] + Tbot[0][1]*V2fcs[1] + Tbot[0][2]*V2fcs[2]), 
          -1.*(Tbot[1][0]*V2fcs[0] + Tbot[1][1]*V2fcs[1] + Tbot[1][2]*V2fcs[2]), 
          -1.*(Tbot[2][0]*V2fcs[0] + Tbot[2][1]*V2fcs[1] + Tbot[2][2]*V2fcs[2])]
        Vb3bcs = [-1.*(Tbot[0][0]*V3fcs[0] + Tbot[0][1]*V3fcs[1] + Tbot[0][2]*V3fcs[2]), 
          -1.*(Tbot[1][0]*V3fcs[0] + Tbot[1][1]*V3fcs[1] + Tbot[1][2]*V3fcs[2]), 
          -1.*(Tbot[2][0]*V3fcs[0] + Tbot[2][1]*V3fcs[1] + Tbot[2][2]*V3fcs[2])]
        Vb4bcs = [-1.*(Tbot[0][0]*V4fcs[0] + Tbot[0][1]*V4fcs[1] + Tbot[0][2]*V4fcs[2]), 
          -1.*(Tbot[1][0]*V4fcs[0] + Tbot[1][1]*V4fcs[1] + Tbot[1][2]*V4fcs[2]), 
          -1.*(Tbot[2][0]*V4fcs[0] + Tbot[2][1]*V4fcs[1] + Tbot[2][2]*V4fcs[2])]
        Vb5bcs = [-1.*(Tbot[0][0]*V5fcs[0] + Tbot[0][1]*V5fcs[1] + Tbot[0][2]*V5fcs[2]), 
          -1.*(Tbot[1][0]*V5fcs[0] + Tbot[1][1]*V5fcs[1] + Tbot[1][2]*V5fcs[2]), 
          -1.*(Tbot[2][0]*V5fcs[0] + Tbot[2][1]*V5fcs[1] + Tbot[2][2]*V5fcs[2])]
        Vb9bcs = [-1.*(Tbot[0][0]*V9fcs[0] + Tbot[0][1]*V9fcs[1] + Tbot[0][2]*V9fcs[2]), 
          -1.*(Tbot[1][0]*V9fcs[0] + Tbot[1][1]*V9fcs[1] + Tbot[1][2]*V9fcs[2]), 
          -1.*(Tbot[2][0]*V9fcs[0] + Tbot[2][1]*V9fcs[1] + Tbot[2][2]*V9fcs[2])]
        Vb10bcs = [-1.*(Tbot[0][0]*V10fcs[0] + Tbot[0][1]*V10fcs[1] + Tbot[0][2]*V10fcs[2]), 
          -1.*(Tbot[1][0]*V10fcs[0] + Tbot[1][1]*V10fcs[1] + Tbot[1][2]*V10fcs[2]), 
          -1.*(Tbot[2][0]*V10fcs[0] + Tbot[2][1]*V10fcs[1] + Tbot[2][2]*V10fcs[2])]
        Vb11bcs = [-1.*(Tbot[0][0]*V11fcs[0] + Tbot[0][1]*V11fcs[1] + Tbot[0][2]*V11fcs[2]), 
          -1.*(Tbot[1][0]*V11fcs[0] + Tbot[1][1]*V11fcs[1] + Tbot[1][2]*V11fcs[2]), 
          -1.*(Tbot[2][0]*V11fcs[0] + Tbot[2][1]*V11fcs[1] + Tbot[2][2]*V11fcs[2])]
        Vb12bcs = [-1.*(Tbot[0][0]*V12fcs[0] + Tbot[0][1]*V12fcs[1] + Tbot[0][2]*V12fcs[2]), 
          -1.*(Tbot[1][0]*V12fcs[0] + Tbot[1][1]*V12fcs[1] + Tbot[1][2]*V12fcs[2]), 
          -1.*(Tbot[2][0]*V12fcs[0] + Tbot[2][1]*V12fcs[1] + Tbot[2][2]*V12fcs[2])]

        for i in range(0, 18):
            if i == 0:
                Vbcs = Vt1bcs
            if i == 1:
                Vbcs = Vt2bcs
            if i == 2:
                Vbcs = Vt3bcs
            if i == 3:
                Vbcs = Vt4bcs
            if i == 4:
                Vbcs = Vt5bcs
            if i == 5:
                Vbcs = Vt9bcs
            if i == 6:
                Vbcs = Vt10bcs
            if i == 7:
                Vbcs = Vt11bcs
            if i == 8:
                Vbcs = Vt12bcs
            if i == 9:
                Vbcs = Vb1bcs
            if i == 10:
                Vbcs = Vb2bcs
            if i == 11:
                Vbcs = Vb3bcs
            if i == 12:
                Vbcs = Vb4bcs
            if i == 13:
                Vbcs = Vb5bcs
            if i == 14:
                Vbcs = Vb9bcs
            if i == 15:
                Vbcs = Vb10bcs
            if i == 16:
                Vbcs = Vb11bcs
            if i == 17:
                Vbcs = Vb12bcs
            pas[:, i] = 180./math.pi*np.arccos((Vbcs[0]*Bbcs[:, 0] + Vbcs[1]*Bbcs[:, 1] + Vbcs[2]*Bbcs[:, 2])/(np.sqrt(Vbcs[0]**2+Vbcs[1]**2+Vbcs[2]**2) * np.sqrt(Bbcs[:, 0]**2+Bbcs[:, 1]**2+Bbcs[:, 2]**2)))
    elif datatype == 'ion':
        pas = np.empty([len(btimes), 6]) # pitch angles for each eye at eaceh time

        # Telescope vectors in Body Coordinate System:
        #   Factors of -1 account for 180 deg shift between particle velocity and telescope normal direction:
        # Top:
        Vt6bcs = [-1.*(Ttop[0][0]*V6fcs[0] + Ttop[0][1]*V6fcs[1] + Ttop[0][2]*V6fcs[2]), 
          -1.*(Ttop[1][0]*V6fcs[0] + Ttop[1][1]*V6fcs[1] + Ttop[1][2]*V6fcs[2]), 
          -1.*(Ttop[2][0]*V6fcs[0] + Ttop[2][1]*V6fcs[1] + Ttop[2][2]*V6fcs[2])]
        Vt7bcs = [-1.*(Ttop[0][0]*V7fcs[0] + Ttop[0][1]*V7fcs[1] + Ttop[0][2]*V7fcs[2]), 
          -1.*(Ttop[1][0]*V7fcs[0] + Ttop[1][1]*V7fcs[1] + Ttop[1][2]*V7fcs[2]), 
          -1.*(Ttop[2][0]*V7fcs[0] + Ttop[2][1]*V7fcs[1] + Ttop[2][2]*V7fcs[2])]
        Vt8bcs = [-1.*(Ttop[0][0]*V8fcs[0] + Ttop[0][1]*V8fcs[1] + Ttop[0][2]*V8fcs[2]), 
          -1.*( Ttop[1][0]*V8fcs[0] + Ttop[1][1]*V8fcs[1] + Ttop[1][2]*V8fcs[2]), 
          -1.*(Ttop[2][0]*V8fcs[0] + Ttop[2][1]*V8fcs[1] + Ttop[2][2]*V8fcs[2])]
        # Bottom:
        Vb6bcs = [-1.*(Tbot[0][0]*V6fcs[0] + Tbot[0][1]*V6fcs[1] + Tbot[0][2]*V6fcs[2]), 
          -1.*(Tbot[1][0]*V6fcs[0] + Tbot[1][1]*V6fcs[1] + Tbot[1][2]*V6fcs[2]), 
          -1.*( Tbot[2][0]*V6fcs[0] + Tbot[2][1]*V6fcs[1] + Tbot[2][2]*V6fcs[2])]
        Vb7bcs = [-1.*(Tbot[0][0]*V7fcs[0] + Tbot[0][1]*V7fcs[1] + Tbot[0][2]*V7fcs[2]), 
          -1.*(Tbot[1][0]*V7fcs[0] + Tbot[1][1]*V7fcs[1] + Tbot[1][2]*V7fcs[2]), 
          -1.*(Tbot[2][0]*V7fcs[0] + Tbot[2][1]*V7fcs[1] + Tbot[2][2]*V7fcs[2])]
        Vb8bcs = [-1.*(Tbot[0][0]*V8fcs[0] + Tbot[0][1]*V8fcs[1] + Tbot[0][2]*V8fcs[2]), 
          -1.*(Tbot[1][0]*V8fcs[0] + Tbot[1][1]*V8fcs[1] + Tbot[1][2]*V8fcs[2]), 
          -1.*(Tbot[2][0]*V8fcs[0] + Tbot[2][1]*V8fcs[1] + Tbot[2][2]*V8fcs[2])]

        for i in range(0, 6):
            if i == 0:
                Vbcs = Vt6bcs
            if i == 1:
                Vbcs = Vt7bcs
            if i == 2:
                Vbcs = Vt8bcs
            if i == 3:
                Vbcs = Vb6bcs
            if i == 4:
                Vbcs = Vb7bcs
            if i == 5:
                Vbcs = Vb8bcs
            pas[:, i] = 180./math.pi*np.arccos((Vbcs[0]*Bbcs[:, 0] + Vbcs[1]*Bbcs[:, 1] + Vbcs[2]*Bbcs[:, 2])/(np.sqrt(Vbcs[0]**2+Vbcs[1]**2+Vbcs[2]**2) * np.sqrt(Bbcs[:, 0]**2+Bbcs[:, 1]**2+Bbcs[:, 2]**2)))

    outvar = 'mms'+probe+'_epd_feeps_'+data_rate+'_'+level+'_'+datatype+'_pa'+suffix
    store_data(outvar, data={'x': btimes, 'y': pas})
    return outvar
