
from pyspedas.mms.feeps.mms_feeps_active_eyes import mms_feeps_active_eyes
from pyspedas import mms_load_fgm
from pyspedas import data_exists
from pytplot import get_data, store_data
import numpy as np
import math

def mms_feeps_pitch_angles(trange=None, probe='1', level='l2', data_rate='srvy', datatype='electron', suffix=''):
    """
    Generates a tplot variable containing the FEEPS pitch angles for each telescope from magnetic field data.

    Parameters:
        trange : list of str
            time range of interest [starttime, endtime] with the format 
            'YYYY-MM-DD','YYYY-MM-DD'] or to specify more or less than a day 
            ['YYYY-MM-DD/hh:mm:ss','YYYY-MM-DD/hh:mm:ss']

        probe: str
            probe #, e.g., '4' for MMS4

        level: str
            data level, e.g., 'l2'

        data_rate: str
            instrument data rate, e.g., 'srvy' or 'brst'

        datatype: str
            'electron' or 'ion'

        suffix: str
            suffix of the loaded data

    Returns:
        Tuple: (tplot variable created, hash table used by PAD routine)
    """

    # get the times from the currently loaded FEEPS data
    pa_variable = get_data('mms'+probe+'_epd_feeps_'+data_rate+'_'+level+'_'+datatype+'_pitch_angle'+suffix)

    if pa_variable is None:
        print('Error reading pitch angle variable')
        return

    times = pa_variable[0]
    pa_data = pa_variable[1]

    if times is not None:
        if trange is None:
            trange = [float(times.min()), float(times.max())]

    eyes = mms_feeps_active_eyes(trange, probe, data_rate, datatype, level)

    # need the B-field data
    mms_load_fgm(trange=trange, probe=probe, data_rate=data_rate, varformat='*_b_bcs_*')

    btimes, Bbcs = get_data('mms'+probe+'_fgm_b_bcs_'+data_rate+'_l2')

    idx_maps = None

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

    if datatype == 'electron':
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
    
            if data_rate == 'srvy':
                # the following 2 hash tables map TOP/BOTTOM telescope #s to index of the PA array created above
                top_tele_idx_map = {}
                bot_tele_idx_map = {}
                top_tele_idx_map[1] = 0
                top_tele_idx_map[2] = 1
                top_tele_idx_map[3] = 2
                top_tele_idx_map[4] = 3
                top_tele_idx_map[5] = 4
                top_tele_idx_map[9] = 5
                top_tele_idx_map[10] = 6
                top_tele_idx_map[11] = 7
                top_tele_idx_map[12] = 8
                bot_tele_idx_map[1] = 9
                bot_tele_idx_map[2] = 10
                bot_tele_idx_map[3] = 11
                bot_tele_idx_map[4] = 12
                bot_tele_idx_map[5] = 13
                bot_tele_idx_map[9] = 14
                bot_tele_idx_map[10] = 15
                bot_tele_idx_map[11] = 16
                bot_tele_idx_map[12] = 17

                top_idxs = []
                bot_idxs = []

                # PAs for only active eyes
                new_pas = np.empty([len(btimes), len(eyes['top'])+len(eyes['bottom'])]) # pitch angles for each eye at eaceh time

                for top_idx, top_eye in enumerate(eyes['top']):
                    new_pas[:, top_idx] = pas[:, top_tele_idx_map[top_eye]]
                    top_idxs.append(top_idx)

                for bot_idx, bot_eye in enumerate(eyes['bottom']):
                    new_pas[:, bot_idx+len(eyes['top'])] = pas[:, bot_tele_idx_map[bot_eye]]
                    bot_idxs.append(bot_idx+len(eyes['top']))

                idx_maps = {'electron-top': top_idxs, 'electron-bottom': bot_idxs}

            else:
                new_pas = pas

    elif datatype == 'ion':
        pas = np.empty([len(btimes), 6]) # pitch angles for each eye at each time

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

        # the following 2 hash tables map TOP/BOTTOM telescope #s to index of the PA array created above
        top_tele_idx_map = {}
        bot_tele_idx_map = {}
        top_tele_idx_map[6] = 0
        top_tele_idx_map[7] = 1
        top_tele_idx_map[8] = 2
        bot_tele_idx_map[6] = 3
        bot_tele_idx_map[7] = 4
        bot_tele_idx_map[8] = 5

        top_idxs = []
        bot_idxs = []

        # PAs for only active eyes
        new_pas = np.empty([len(btimes), len(eyes['top'])+len(eyes['bottom'])]) # pitch angles for each eye at eaceh time

        for top_idx, top_eye in enumerate(eyes['top']):
            new_pas[:, top_idx] = pas[:, top_tele_idx_map[top_eye]]
            top_idxs.append(top_idx)

        for bot_idx, bot_eye in enumerate(eyes['bottom']):
            new_pas[:, bot_idx+len(eyes['top'])] = pas[:, bot_tele_idx_map[bot_eye]]
            bot_idxs.append(bot_idx+len(eyes['top']))

        idx_maps = {'ion-top': top_idxs, 'ion-bottom': bot_idxs}


    outvar = 'mms'+probe+'_epd_feeps_'+data_rate+'_'+level+'_'+datatype+'_pa'+suffix

    if data_exists(outvar): # kludge for bug when the PAs were previously calculated
        return (outvar, idx_maps)

    store_data(outvar, data={'x': btimes, 'y': new_pas})

    # interpolate to the PA time stamps
    outdata = get_data(outvar, xarray=True)
    outdata_interpolated = outdata.interp({'time': times})

    store_data(outvar, data={'x': times, 'y': outdata_interpolated.values})

    return (outvar, idx_maps)
