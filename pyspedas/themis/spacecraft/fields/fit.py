from pyspedas.themis.load import load


def fit(trange=['2007-03-23', '2007-03-24'],
        probe='c',
        level='l2',
        suffix='',
        get_support_data=False,
        varformat=None,
        varnames=[],
        downloadonly=False,
        notplot=False,
        no_update=False,
        time_clip=False):
    """
    This function loads THEMIS FIT data

    Parameters:
        trange : list of str
            time range of interest [starttime, endtime] with the format
            'YYYY-MM-DD','YYYY-MM-DD'] or to specify more or less than a day
            ['YYYY-MM-DD/hh:mm:ss','YYYY-MM-DD/hh:mm:ss']

        probe: str or list of str
            Spacecraft probe letter(s) ('a', 'b', 'c', 'd' and/or 'e')

        level: str
            Data type; Valid options: 'l1', 'l2'

        suffix: str
            The tplot variable names will be given this suffix.
            By default, no suffix is added.

        get_support_data: bool
            Data with an attribute "VAR_TYPE" with a value of "support_data"
            will be loaded into tplot.  By default, only loads in data with a
            "VAR_TYPE" attribute of "data".

        varformat: str
            The file variable formats to load into tplot.  Wildcard character
            "*" is accepted.  By default, all variables are loaded in.

        varnames: list of str
            List of variable names to load
            (if not specified, all data variables are loaded)

        downloadonly: bool
            Set this flag to download the CDF files, but not load them into
            tplot variables

        notplot: bool
            Return the data in hash tables instead of creating tplot variables

        no_update: bool
            If set, only load data from your local cache

        time_clip: bool
            Time clip the variables to exactly the range specified
            in the trange keyword

    Returns:
        List of tplot variables created.

    """
    return load(instrument='fit', trange=trange, level=level,
                suffix=suffix, get_support_data=get_support_data,
                varformat=varformat, varnames=varnames,
                downloadonly=downloadonly, notplot=notplot,
                probe=probe, time_clip=time_clip, no_update=no_update)


def cal_fit(probe='a', no_cal=False):
    """
    Converts raw FIT parameter data into physical quantities.
    Warning: This function is in debug state

    Currently, it assumes that "th?_fit" variable is already loaded

    Parameters:
        probe: str
            Spacecraft probe letter ('a', 'b', 'c', 'd' and/or 'e')
        no_cal: bool
            If ture do not apply boom shortening factor or Ex offset defaults

    Returns:
        th?_fgs tplot variable
    """
    import math
    import numpy as np
    import logging

    from pytplot import get_data, store_data, tplot_names, options
    from pyspedas.utilities.download import download
    from pyspedas.themis.config import CONFIG
    from pyspedas.utilities.time_double import time_float_one
    from copy import deepcopy
    from numpy.linalg import inv

    if probe == 'f':
        logging.warning(f"Probe f is not supported. Please use IDL version of 'thm_cal_fit' in SPEDAS.")
        return

    # calibration parameters
    lv12 = 49.6  # m
    lv34 = 40.4  # m
    lv56 = 5.6  # m

    # This values provide better agreement with IDL
    lv12 = 49.599997
    lv34 = 40.400003
    lv56 = 5.59999981

    # calibration table
    cpar = {"e12": {"cal_par_time": '2002-01-01/00:00:00',
                    "Ascale": -15000.0 / (lv12 * 2. ** 15.),
                    "Bscale": -15000.0 / (lv12 * 2. ** 15.),
                    "Cscale": -15000.0 / (lv12 * 2. ** 15.),
                    "theta": 0.0,
                    "sigscale": 15000. / (lv12 * 2. ** 15.),
                    "Zscale": -15000. / (lv56 * 2. ** 15.),
                    "units": 'mV/m'},
            "e34": {"cal_par_time": '2002-01-01/00:00:00',
                    "Ascale": -15000.0 / (lv34 * 2. ** 15.),
                    "Bscale": -15000.0 / (lv34 * 2. ** 15.),
                    "Cscale": -15000.0 / (lv34 * 2. ** 15.),
                    "theta": 0.0,
                    "sigscale": 15000. / (lv34 * 2. ** 15.),
                    "Zscale": -15000. / (lv56 * 2. ** 15.),
                    "units": 'mV/m'},
            "b": {"cal_par_time": '2002-01-01/00:00:00',
                  "Ascale": 1.,
                  "Bscale": 1.,
                  "Cscale": 1.,
                  "theta": 0.0,
                  "sigscale": 1.,
                  "Zscale": 1.,
                  "units": 'nT'}}

    # tplot options
    color_str = ['blue', 'green', 'red']
    color_str2 = ['magenta', 'blue', 'cyan', 'green', 'orange']
    b_str = ['Bx', 'By', 'Bz']
    e_str = ['Ex', 'Ey', 'Ez']
    b_units = cpar['b']['units']
    e_units = cpar['e12']['units']
    b_units_str = f'[{b_units}]'
    e_units_str = f'[{e_units}]'
    b_data_att = {'units': b_units, 'cal_par_time': cpar['b']['cal_par_time'], 'data_type': 'calibrated',
                  'coord_sys': 'dsl'}
    b_data_att_sigma = {'units': b_units}
    e_data_att = {'units': e_units, 'cal_par_time': cpar['e12']['cal_par_time'], 'data_type': 'calibrated',
                  'coord_sys': 'dsl'}
    e_data_att_sigma = {'units': e_units}

    b_opt_dict = {'legend_names': b_str, 'ysubtitle': b_units_str, 'color': color_str, 'alpha': 1}
    e_opt_dict = {'legend_names': e_str, 'ysubtitle': e_units_str, 'color': color_str, 'alpha': 1}

    # if tplot does not show 5th legend name, update tplot
    b_opt_dict2 = {'legend_names': ['A', 'B', 'C', 'Sig', '<Bz>'],
                   'ysubtitle': b_units_str, 'color': color_str2, 'alpha': 1}
    e_opt_dict2 = {'legend_names': ['A', 'B', 'C', 'Sig', '<Ez>'],
                   'ysubtitle': e_units_str, 'color': color_str2, 'alpha': 1}

    # Get list of tplot variables
    tnames = tplot_names(True)  # True for quiet output

    # Get data from th?_fit variable
    tvar = 'th' + probe + '_fit'

    # B-field fit (FGM) processing

    if tvar not in tnames:
        logging.warning(f"Variable {tvar} is not found")
        return

    # Using deep copy to create an independent instance
    d = deepcopy(get_data(tvar))  # NOTE: Indexes are not the same as in SPEDAS, e.g. 27888x2x5

    # establish probe number in cal tables
    sclist = {'a': 0, 'b': 1, 'c': 2, 'd': 3, 'e': 4, 'f': -1}  # for probe 'f' no flatsat FGM cal files
    scn = sclist[probe]

    #  Rotation vectors
    rotBxy_angles = [29.95, 29.95, 29.95, 29.95,
                     29.95]  # vassilis 6/2/2007: deg to rotate FIT on spin plane to match DSL on 5/4
    rotBxy = rotBxy_angles[scn]  # vassilis 4/28: probably should be part of CAL table as well...
    cs = math.cos(rotBxy * math.pi / 180)  # vassilis
    sn = math.sin(rotBxy * math.pi / 180)  # vassilis

    adc2nT = 50000. / 2. ** 24  # vassilis 2007 - 04 - 03

    # B - field fit(FGM)
    i = 1

    d.y[:, i, 0] = cpar['b']['Ascale'] * d.y[:, i, 0] * adc2nT  # vassilis
    d.y[:, i, 1] = cpar['b']['Bscale'] * d.y[:, i, 1] * adc2nT  # vassilis
    d.y[:, i, 2] = cpar['b']['Cscale'] * d.y[:, i, 2] * adc2nT  # vassilis
    d.y[:, i, 3] = cpar['b']['sigscale'] * d.y[:, i, 3] * adc2nT  # vassilis
    d.y[:, i, 4] = cpar['b']['Zscale'] * d.y[:, i, 4] * adc2nT  # vassilis

    # Calculating Bzoffset using thx+'/l1/fgm/0000/'+thx+'_fgmcal.txt'
    thx = 'th' + probe
    remote_name = thx + '/l1/fgm/0000/' + thx + '_fgmcal.txt'
    calfile = download(remote_file=remote_name,
                       remote_path=CONFIG['remote_data_dir'],
                       local_path=CONFIG['local_data_dir'],
                       no_download=False)
    if not calfile:
        # This code should never be executed
        logging.warning(f"Calibration file {thx}_fgmcal.txt is not found")
        return

    caldata = np.loadtxt(calfile[0], converters={0: time_float_one})
    # TODO: In SPEDAS we checks if data is already calibrated
    # Limit to the time of interest
    caltime = caldata[:, 0]
    t1 = np.nonzero(caltime < d.times.min())[0]  # left time
    t2 = np.nonzero(caltime <= d.times.max())[0]  # right time

    Bzoffset = np.zeros(d.times.shape)
    if t1.size + t2.size > 1:  # Time range exist in the file
        tidx = np.arange(t1[-1], t2[-1] + 1)
        caltime = caltime[tidx]
        offi = caldata[tidx, 1:4]  # col 1-3
        cali = caldata[tidx, 4:13]  # col 4-13
        # spinperii = caldata[tidx, 13]  # col 14 not in use
        flipxz = -1 * np.fliplr(np.identity(3))
        # SPEDAS: offi2 = invert(transpose([cali[istart, 0:2], cali[istart, 3:5], cali[istart, 6:8]]) ## flipxz)##offi[istart, *]
        for t in range(0, caltime.size):
            offi2 = inv(np.c_[cali[t, 0:3], cali[t, 3:6], cali[t, 6:9]].T @ flipxz) @ offi[t, :]
            tidx = d.times >= caltime[t]
            Bzoffset[tidx] = offi2[2]  # last element

    Bxprime = cs * d.y[:, i, 1] + sn * d.y[:, i, 2]
    Byprime = -sn * d.y[:, i, 1] + cs * d.y[:, i, 2]
    Bzprime = -d.y[:, i, 4] - Bzoffset  # vassilis 4/28 (SUBTRACTING offset from spinaxis POSITIVE direction)

    # d is a namedtuple and does not support direct copy by value
    dprime = deepcopy(d)
    dprime.y[:, i, 1] = Bxprime  # vassilis DSL
    dprime.y[:, i, 2] = Byprime  # vassilis DSL
    dprime.y[:, i, 4] = Bzprime  # vassilis DSL

    # Create fgs variable and remove nans
    fgs = dprime.y[:, i, [1, 2, 4]]
    idx = ~np.isnan(fgs[:, 0])
    fgs_data = {'x': d.times[idx], 'y': fgs[idx, :]}

    # Save fgs tplot variable
    tvar = 'th' + probe + '_fgs'
    store_data(tvar, fgs_data, attr_dict=b_data_att)
    options(tvar, opt_dict=b_opt_dict)

    # Save fgs_sigma variable
    fit_sigma_data = {'x': d.times[idx], 'y': d.y[idx, i, 3]}
    tvar = 'th' + probe + '_fgs_sigma'
    store_data(tvar, fit_sigma_data, attr_dict=b_data_att_sigma)
    options(tvar, opt_dict=b_opt_dict)

    # Save bfit variable
    bfit_data = {'x': d.times[:], 'y': d.y[:, i, :].squeeze()}
    tvar = 'th' + probe + '_fit_bfit'
    store_data(tvar, bfit_data, attr_dict=b_data_att)
    options(tvar, opt_dict=b_opt_dict2)

    # E-field fit (EFI) processing

    # Get data from th?_fit_code variable
    tvar = 'th' + probe + '_fit_code'
    d_code = None  # Blank variable, if d_code is not used

    if tvar in tnames:
        i = 0
        d_code = get_data(tvar)
        e12_ss = (d_code.y[:, i] == int("e1", 16)) | (d_code.y[:, i] == int("e5", 16))
        e34_ss = (d_code.y[:, i] == int("e3", 16)) | (d_code.y[:, i] == int("e7", 16))
    else:
        # Default values (if no code)
        ne12 = d.times.size
        e12_ss = np.ones(ne12, dtype=bool)  # create an index arrays
        e34_ss = np.zeros(ne12, dtype=bool)

    # Save 'efs' datatype before "hard wired" calibrations.
    # An EFI-style calibration is performed below.
    i = 0
    efs = d.y[:, i, [1, 2, 4]]
    # Locate samples with non-NaN data values.  Save the indices in
    # efsx_good, then at the end of calibration, pull the "good"
    # indices out of the calibrated efs[] array to make the thx_efs
    # tplot variable.
    efsx_good = ~np.isnan(efs[:, 0])

    if np.any(efsx_good):
        if np.any(e34_ss):  # rotate efs 90 degrees if necessary, if e34 was used in spinfit
            tmp = d.y[e34_ss, i, :]  # Apply logical arrays
            # TODO: there should be a better way to combine indexes
            efs[e34_ss, :] = tmp[:, [2, 1, 4]]  # Apply dimension selection
            efs[e34_ss, 0] = -efs[e34_ss, 0]

    efsz = d.y[:, i, 4]  # save Ez separately, for possibility that it's the SC potential

    # Use cpar to calibrate
    if np.any(e12_ss):
        d.y[e12_ss, i, 0] = cpar["e12"]["Ascale"] * d.y[e12_ss, i, 0]
        d.y[e12_ss, i, 1] = cpar["e12"]["Bscale"] * d.y[e12_ss, i, 1]
        d.y[e12_ss, i, 2] = cpar["e12"]["Cscale"] * d.y[e12_ss, i, 2]
        d.y[e12_ss, i, 3] = cpar["e12"]["sigscale"] * d.y[e12_ss, i, 3]
        d.y[e12_ss, i, 4] = cpar["e12"]["Zscale"] * d.y[e12_ss, i, 4]
    if np.any(e34_ss):
        d.y[e34_ss, i, 0] = cpar["e34"]["Ascale"] * d.y[e34_ss, i, 0]
        d.y[e34_ss, i, 1] = cpar["e34"]["Bscale"] * d.y[e34_ss, i, 1]
        d.y[e34_ss, i, 2] = cpar["e34"]["Cscale"] * d.y[e34_ss, i, 2]
        d.y[e34_ss, i, 3] = cpar["e34"]["sigscale"] * d.y[e34_ss, i, 3]
        d.y[e34_ss, i, 4] = cpar["e34"]["Zscale"] * d.y[e34_ss, i, 4]

    # save fit_efit variable
    fit_efit_data = {'x': d.times, 'y': d.y[:, i, :]}
    tvar = 'th' + probe + '_fit_efit'
    store_data(tvar, fit_efit_data, attr_dict=e_data_att)
    options(tvar, opt_dict=e_opt_dict2)

    # thx_efs and thx_efs_sigma,
    # Calibrate efs data by applying E12 calibration factors, not despinning, then applying despun (spin-dependent)
    # calibration factors from E12 (the spin-independent offset is subtracted on-board):

    # Load calibration file, e.g. tha/l1/eff/0000/tha_efi_calib_params.txt
    remote_name = thx + '/l1/eff/0000/' + thx + '_efi_calib_params.txt'
    eficalfile = download(remote_file=remote_name,
                          remote_path=CONFIG['remote_data_dir'],
                          local_path=CONFIG['local_data_dir'],
                          no_download=False)

    if not eficalfile:
        # This code should never be executed
        logging.warning(f"Calibration file {thx}_efi_calib_params.txt is not found")
        return

    colnums = {"time": [0], "edc_offset": [14, 15, 16], "edc_gain": [17, 18, 19],
               "BOOM_LENGTH": [26, 27, 28], "BOOM_SHORTING_FACTOR": [29, 30, 31],
               "DSC_OFFSET": [32, 33, 34]}  # List of columns to be loaded
    collist = list()
    [collist.extend(cnum) for cnum in colnums.values()]
    collist.sort()  # ensurer that the list of columns is sorted
    eficaltxt = np.loadtxt(eficalfile[0], skiprows=1, max_rows=1, converters={0: time_float_one}, usecols=collist)
    eficaldata = {"time": eficaltxt[0], "gain": eficaltxt[4:7], "offset": eficaltxt[1:4],
                  "boom_length": eficaltxt[7:10], "boom_shorting_factor": eficaltxt[10:13],
                  "dsc_offset": eficaltxt[13:16]}

    # Boom
    exx = eficaldata["boom_length"]
    if not no_cal:
        exx *= eficaldata["boom_shorting_factor"]

    # Calibrate E field
    # Calibrate Ex and Ey spinfits that are derived from E12 only!
    if np.any(e12_ss):
        efs[e12_ss, 0:2] = -1000. * eficaldata["gain"][0] * efs[e12_ss, 0:2] / exx[0]
    if np.any(e34_ss):
        efs[e34_ss, 0:2] = -1000. * eficaldata["gain"][1] * efs[e34_ss, 0:2] / exx[1]
    # Calibrate Ez spinfit by itself:
    efs[:, 2] = -1000. * eficaldata["gain"][2] * efs[:, 2] / exx[2]

    # DC Offset
    if not no_cal:
        efs -= eficaldata["dsc_offset"]

    # Here, if the fit_code is 'e5'x (229) then efs[*,2] contains the spacecraft potential, so set all of those values
    # to Nan, jmm, 19-Apr-2010
    # Or if the fit_code is 'e7'x (231), this will also be including the SC potential, jmm,22-oct-2010
    if d_code is not None:
        sc_port = (d_code.y[:, i] == int("e5", 16)) | (d_code.y[:, i] == int("e7", 16))
        if np.any(sc_port):
            efs[sc_port, 2] = np.nan

    # save efs variable
    efs_data = {'x': d.times[efsx_good], 'y': efs[efsx_good, :]}  # efs[efsx_good,*]
    tvar = 'th' + probe + '_efs'
    store_data(tvar, efs_data, attr_dict=e_data_att)
    options(tvar, opt_dict=e_opt_dict)

    # save efs_sigma variable
    efs_sigma_data = {'x': d.times[efsx_good], 'y': d.y[efsx_good, i, 3]}  # d.y[efsx_good, 3, idx]
    tvar = 'th' + probe + '_efs_sigma'
    store_data(tvar, efs_sigma_data, attr_dict=e_data_att_sigma)
    options(tvar, opt_dict=e_opt_dict)

    # save efs_0
    efs_0_data = deepcopy(efs)
    efs_0_data[:, 2] = 0
    efs_0 = {'x': d.times[efsx_good], 'y': efs_0_data[efsx_good, :]}
    tvar = 'th' + probe + '_efs_0'
    store_data(tvar, efs_0, attr_dict=e_data_att_sigma)
    options(tvar, opt_dict=e_opt_dict)

    # calculate efs_dot0
    Ez = (efs[:, 0] * fgs[:, 0] + efs[:, 1] * fgs[:, 1]) / (-1 * fgs[:, 2])
    angle = np.arccos(fgs[:, 2] / np.sqrt(np.sum(fgs ** 2, axis=1))) * 180 / np.pi
    angle80 = angle > 80
    if np.any(angle80):
        Ez[angle80] = np.NaN
    efx_dot0_data = deepcopy(efs)
    efx_dot0_data[:, 2] = Ez

    # save efs_dot0
    efs_dot0 = {'x': d.times[efsx_good], 'y': efx_dot0_data[efsx_good, :]}
    tvar = 'th' + probe + '_efs_dot0'
    store_data(tvar, efs_dot0, attr_dict=e_data_att_sigma)
    options(tvar, opt_dict=e_opt_dict)
