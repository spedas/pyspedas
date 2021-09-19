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


def cal_fit(probe='a'):
    """
    Converts raw FIT parameter data into physical quantities.
    Warning: This function is in debug state

    Currently, it assumes that "th?_fit" variable is already loaded

    Parameters:
        probe: a

    Returns:
        th?_fgs tplot variable
    """
    import math
    import numpy as np

    from pytplot import get_data, store_data
    from pyspedas.utilities.download import download
    from pyspedas.themis.config import CONFIG
    from pyspedas.utilities.time_double import time_float_one
    from numpy.linalg import inv

    # Get data from th?_fit variable
    # TODO: Add check of tvar existence
    tvar = 'th' + probe + '_fit'
    d = get_data(tvar)  # NOTE: Indexes are not the same as in SPEDAS, e.g. 27888x2x5

    # calibration parameters
    lv12 = 49.6  # m
    lv34 = 40.4  # m
    lv56 = 5.6  # m
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
                  "Ascale": 1.e0,
                  "Bscale": 1.e0,
                  "Cscale": 1.e0,
                  "theta": 0.0,
                  "sigscale": 1.e0,
                  "Zscale": 1.e0,
                  "units": 'nT'}}
    # establish probe number in cal tables
    sclist = {'a': 0, 'b': 1, 'c': 2, 'd': 3, 'e': 4, 'f': -1}  # for probe 'f' no flatsat FGM cal files
    # TODO: Add processing of probe f
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
    # TODO: Add file check
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

    dprime = d
    dprime.y[:, i, 1] = Bxprime  # vassilis DSL
    dprime.y[:, i, 2] = Byprime  # vassilis DSL
    dprime.y[:, i, 4] = Bzprime  # vassilis DSL

    # Create fgs variable and remove nans
    fgs = dprime.y[:, i, [1, 2, 4]]
    idx = ~np.isnan(fgs[:, 0])
    fgs_data = {'x': d.times[idx], 'y': fgs[idx, :]}

    # Save fgs tplot variable
    tvar = 'th' + probe + '_fgs'
    store_data(tvar, fgs_data)
